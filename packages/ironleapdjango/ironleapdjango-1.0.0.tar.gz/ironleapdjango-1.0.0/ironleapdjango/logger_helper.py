from .masks import MaskData
from .parse_body import ParseBody
from .schemas import json_serialize
from django.http import HttpRequest, HttpResponse
import json
import base64
import re
import copy
import uuid



class LoggerHelper:
    def __init__(self):
        self.regex_http_ = re.compile(r'^HTTP_.+$')
        self.regex_content_type = re.compile(r'^CONTENT_TYPE$')
        self.regex_content_length = re.compile(r'^CONTENT_LENGTH$')
        self.mask_helper = MaskData()
        self.parse_body = ParseBody()

    @classmethod
    def flatten_to_string(cls, value):
        if type(value) == str:
            return value
        if value is None:
            return ''
        return json_serialize(value)

    @classmethod
    def mapper(cls, response, key):
        return copy.deepcopy(response[key])

    def parse_request_headers(self, request, middleware_settings, debug):
        req_headers = {}
        regex_http_start = re.compile('^HTTP_')
        try:
            for header in request.META:
                if self.regex_http_.match(header) or self.regex_content_type.match(
                        header) or self.regex_content_length.match(header):
                    normalized_header = regex_http_start.sub('', header)
                    normalized_header = normalized_header.replace('_', '-')
                    req_headers[normalized_header] = request.META[header]
            req_headers = self.mask_helper.mask_headers(req_headers, middleware_settings.get('REQUEST_HEADER_MASKS'))
        except Exception as inst:
            if debug:
                print("error encountered while copying request header")
                print(inst)
            req_headers = {}

        if debug:
            print("about to print what is in meta %d " % len(request.META))
            for x in request.META:
                print(x, ':', request.META[x])
            print("about to print headers %d " % len(req_headers))
            for x in req_headers:
                print(x, ':', req_headers[x])

        req_headers = {k: self.flatten_to_string(v) for k, v in req_headers.items()}
        return req_headers

    def prepare_request_body(self, request, req_headers, log_body, middleware_settings):
        req_body = None
        req_body_transfer_encoding = None
        if log_body and request._il_body:
            if isinstance(request._il_body, str):
                req_body, req_body_transfer_encoding = self.parse_body.parse_string_body(request._il_body,
                                                                                         self.parse_body.transform_headers(
                                                                                             req_headers),
                                                                                         middleware_settings.get(
                                                                                             'REQUEST_BODY_MASKS'))
            else:
                req_body, req_body_transfer_encoding = self.parse_body.parse_bytes_body(request._il_body,
                                                                                        self.parse_body.transform_headers(
                                                                                            req_headers),
                                                                                        middleware_settings.get(
                                                                                            'REQUEST_BODY_MASKS'))
        return req_body, req_body_transfer_encoding

    def parse_response_headers(self, response, middleware_settings):
        # a little hacky, using _headers, which is intended as a private variable.
        # From Django 3.2 onwards, headers is available however
        headers = response._headers if hasattr(response, '_headers') else response.headers
        rsp_headers = {k: self.mapper(response, k) for k, v in headers.items()}
        return self.mask_helper.mask_headers(rsp_headers, middleware_settings.get('RESPONSE_HEADER_MASKS'))

    def prepare_response_body(self, response, rsp_headers, log_body, middleware_settings):
        rsp_body = None
        rsp_body_transfer_encoding = None
        if log_body and isinstance(response, HttpResponse) and response.content:
            if isinstance(response.content, str):
                rsp_body, rsp_body_transfer_encoding = self.parse_body.parse_string_body(response.content,
                                                                                         self.parse_body.transform_headers(
                                                                                             rsp_headers),
                                                                                         middleware_settings.get(
                                                                                             'RESPONSE_BODY_MASKS'))
            else:
                rsp_body, rsp_body_transfer_encoding = self.parse_body.parse_bytes_body(response.content,
                                                                                        self.parse_body.transform_headers(
                                                                                            rsp_headers),
                                                                                        middleware_settings.get(
                                                                                            'RESPONSE_BODY_MASKS'))
        return rsp_body, rsp_body_transfer_encoding

    @classmethod
    def request_url(cls, request):
        return request.scheme + "://" + request.get_host() + request.get_full_path()

    @classmethod
    def get_company_id(cls, middleware_settings, request, response, debug):
        company_id = None
        try:
            identify_company = middleware_settings.get('IDENTIFY_COMPANY', None)
            if identify_company is not None:
                company_id = identify_company(request, response)
        except:
            if debug:
                print("can not execute identify_company function, please check iron leap settings.")
        return company_id

    @classmethod
    def get_metadata(cls, middleware_settings, request, response, debug):
        metadata = None
        try:
            get_metadata = middleware_settings.get('GET_METADATA', None)
            if get_metadata is not None:
                metadata = get_metadata(request, response)
        except:
            if debug:
                print("can not execute get_metadata function, please check iron leap settings.")
        return metadata

    @classmethod
    def skip_event(cls, request, response, middleware_settings, debug):
        try:
            skip_event = middleware_settings.get('SKIP', None)
            if skip_event is not None:
                if skip_event(request, response):
                    return response
        except:
            if debug:
                print("Having difficulty executing skip_event function. Please check iron leap settings.")
            return None

    @classmethod
    def mask_event(cls, event, middleware_settings, debug):
        try:
            mask_event_model = middleware_settings.get('MASK_EVENT_MODEL', None)
            if mask_event_model is not None:
                event = mask_event_model(event)
        except:
            if debug:
                print("Can not execute mask_event_model function. Please check iron leap settings.")
        return event
