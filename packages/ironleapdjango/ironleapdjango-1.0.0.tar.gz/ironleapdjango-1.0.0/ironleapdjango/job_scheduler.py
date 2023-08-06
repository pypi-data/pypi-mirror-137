from datetime import datetime
from .schemas import json_serialize

class JobScheduler:
    def __init__(self):
        pass

    @classmethod
    def exit_handler(cls, scheduler, debug):
        try:
            # Remove job and shut down the scheduler
            scheduler.remove_job('ironleap_events_batch_job')
            scheduler.shutdown()
        except Exception as ex:
            if debug:
                print("Error while closing the queue or scheduler shut down")
                print(str(ex))

    def send_events(self, client, batch_events, debug):
        try:
            if debug:
                print("Sending events to Iron Leap")
            client.post_events_batch(batch_events)
            if debug:
                print("Events sent successfully")
        except Exception as ex:
            if debug:
                print("Error sending event to Iron Leap")
                print(str(ex))

    def batch_events(self, client, events_queue, debug, batch_size):
        batch_events = []
        try:
            while not events_queue.empty():
                batch_events.append(events_queue.get_nowait())
                if len(batch_events) == batch_size:
                    break

            if batch_events:
                batch_response = self.send_events(client, batch_events, debug)
                batch_events[:] = []
                # Set the last time event job ran after sending events
                return batch_response, datetime.utcnow()
            else:
                if debug:
                    print("No events to send")
                # Set the last time event job ran but no message to read from the queue
                return None, datetime.utcnow()
        except Exception as e:
            if debug:
                print("No message to read from the queue")
                print(str(e))
            # Set the last time event job ran when exception occurred while sending event
            return None, datetime.utcnow()
