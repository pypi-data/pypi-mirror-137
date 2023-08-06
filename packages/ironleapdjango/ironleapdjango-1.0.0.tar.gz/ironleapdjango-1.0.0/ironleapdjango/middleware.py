from __future__ import print_function

import django
import logging
import queue
from django.conf import settings
from django.utils import timezone
from io import BytesIO
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from .apiclient import ApiClient
from .job_scheduler import JobScheduler
from .schemas import APIEvent, APIRequest, APIResponse
from .logger_helper import LoggerHelper


class ironleap_middleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.middleware_settings = settings.IRONLEAP_MIDDLEWARE
        self.DEBUG = self.middleware_settings.get('DEBUG', False)
        self.LOG_BODY = self.middleware_settings.get('LOG_BODY', True)
        self.client = ApiClient(self.middleware_settings.get('APP_KEY'), self.middleware_settings.get('IRONLEAP_URL'))
        self.logger_helper = LoggerHelper()
        self.job_scheduler = JobScheduler()
        self.last_updated_time = datetime.utcnow()
        self.last_event_job_run_time = datetime(1970, 1, 1, 0, 0) # Assuming job never ran, set it to epoch start time
        self.scheduler = None
        self.event_queue_size = self.middleware_settings.get('EVENT_QUEUE_SIZE', 1000)
        self.events_queue = queue.Queue(maxsize=self.event_queue_size)
        self.event_batch_size = self.middleware_settings.get('BATCH_SIZE', 25)
        self.batch_send_interval = self.middleware_settings.get('BATCH_SEND_INTERVAL', 2)
        self.is_event_job_scheduled = False

    # Function to schedule send event job in async
    def schedule_event_background_job(self):
        try:
            if not self.scheduler:
                self.scheduler = BackgroundScheduler(daemon=True)
            if not self.scheduler.get_jobs():
                self.scheduler.start()
                self.scheduler.add_job(
                    func=lambda: self.job_scheduler.batch_events(
                        self.client,
                        self.events_queue,
                        self.DEBUG,
                        self.event_batch_size
                    ),
                    trigger=IntervalTrigger(seconds=2),
                    id='ironleap_events_batch_job',
                    name='Schedule events batch job every 2 second',
                    replace_existing=True,
                )
            
                # Avoid passing logging message to the ancestor loggers
                logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)
                logging.getLogger('apscheduler.executors.default').propagate = False

                # Exit handler when exiting the app
                atexit.register(lambda: self.job_scheduler.exit_handler(self.scheduler, self.DEBUG))
        except Exception as ex:
            if self.DEBUG:
                print("Error when scheduling the job")
                print(str(ex))

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Setup response so it can be read from
        req_time = timezone.now()
        try:
            request._il_body = request.body
            request._stream = BytesIO(request.body)
            request._read_started = False
        except:
            request._il_body = None

        if self.DEBUG:
            print("executing get_response")
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        # Safely parse request / response to create event to send to iron leap
        try:
            skip_event_response = self.logger_helper.skip_event(request, response, self.middleware_settings, self.DEBUG)
            if skip_event_response:
                return skip_event_response

            req_headers = self.logger_helper.parse_request_headers(request, self.middleware_settings, self.DEBUG)
            req_body, req_body_transfer_encoding = self.logger_helper.prepare_request_body(request, req_headers, self.LOG_BODY,
                                                                                        self.middleware_settings)
            uri = self.logger_helper.request_url(request)

            rsp_headers = self.logger_helper.parse_response_headers(response, self.middleware_settings)
            rsp_body, rsp_body_transfer_encoding = self.logger_helper.prepare_response_body(response, rsp_headers, self.LOG_BODY,
                                                                                            self.middleware_settings)
            rsp_time = timezone.now()

            company_id = self.logger_helper.get_company_id(self.middleware_settings, request, response, self.DEBUG)
            metadata = self.logger_helper.get_metadata(self.middleware_settings, request, response, self.DEBUG)

            event = APIEvent(
                request=APIRequest(
                    req_time.isoformat(),
                    uri,
                    request.method,
                    req_headers,
                    req_body,
                    req_body_transfer_encoding,
                ),
                response=APIResponse(
                    rsp_time.isoformat(),
                    response.status_code,
                    rsp_headers,
                    rsp_body,
                    rsp_body_transfer_encoding,
                ),
                company_id = company_id,
                metadata = metadata,
            )
            event = self.logger_helper.mask_event(event, self.middleware_settings, self.DEBUG)
        except Exception as ex:
            if self.DEBUG:
                print("Error while constructing event to send")
                print(str(ex))
            return response

        # Try adding event to queue
        try:
            if not self.is_event_job_scheduled and datetime.utcnow() > self.last_event_job_run_time + timedelta(minutes=5):
                try:
                    self.schedule_event_background_job()
                    self.is_event_job_scheduled = True
                    self.last_event_job_run_time = datetime.utcnow()
                except Exception as ex:
                    self.is_event_job_scheduled = False
                    if self.DEBUG:
                        print('Error while starting the event scheduler job in background')
                        print(str(ex))
            if self.DEBUG:
                print("Add APIEvent to the queue")
            self.events_queue.put(event)
        except Exception as ex:
            if self.DEBUG:
                print("Error while adding event to the queue")
                print(str(ex))

        return response
