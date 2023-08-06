# Django Middleware

Send Iron Leap API call data.

## How to install

```shell
pip install ironleapdjango
```

## How to use

In your `settings.py` file in your Django project directory, please add `ironleap.middleware.ironleap_middleware`
to the MIDDLEWARE array. For example:

```
MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'ironleapdjango.middleware.ironleap_middleware'
    ...
]
```

## Configuration options

#### __`APP_KEY`__
(__required__), _string_, provided by Iron Leap.

#### __`IRONLEAP_URL`__
(__required__), _string_, target url collecting events

### Options specific to incoming API calls 

#### __`SKIP`__
(optional) _(request, response) => boolean_, a function that takes a request and a response, and returns true if you want to skip this particular event.

#### __`IDENTIFY_COMPANY`__
(optional) _(request, response) => string_, a function that takes a request and a response, and returns a string that is the company id for this event.

#### __`GET_METADATA`__
(optional) _(request, response) => dictionary_, getMetadata is a function that returns an object that allows you
to add custom metadata that will be associated with the event. The metadata must be a dictionary that can be converted to JSON. For example, you may want to save a VM instance_id, a trace_id, or a tenant_id with the request.

#### __`LOG_BODY`__
(optional) _boolean_, default True, Set to False to remove the HTTP body before sending. If you want more control over which fields are included or not included look at the individual mask method below. 

#### __`MASK_EVENT_MODEL`__
(optional) _(APIEvent) => APIEvent_, a function that takes an APIEvent and returns another APIEvent. Use this if you prefer to write your own mask function than use the string based filter options: REQUEST_BODY_MASKS, REQUEST_HEADER_MASKS, RESPONSE_BODY_MASKS, & RESPONSE_HEADER_MASKS.

#### __`BATCH_SIZE`__
(optional) __int__, default 25, Batch size with which events get sent to Iron Leap.

#### __`EVENT_QUEUE_SIZE`__
(optional) __int__, default 1000, Maximum number of events to hold in queue before sending.

#### __`BATCH_SEND_INTERVAL`__
(optional) __int__, default 2, Number of seconds between sends of batch.

## Example 

```python
def identify_company(req, res):
    # Your custom code that returns a company id string
    return "67890"

def should_skip(req, res):
    # Your custom code that returns true to skip logging
    return "health/probe" in req.path

def mask_event(eventmodel):
    # Your custom code to change or remove any sensitive fields
    if 'password' in eventmodel.response.body:
        eventmodel.response.body['password'] = None
    return eventmodel

def get_metadata(req, res):
    return {
        'datacenter': 'westus',
        'deployment_version': 'v1.2.3',
    }


IRONLEAP_MIDDLEWARE = {
    'APP_KEY': 'app key',
    'IRONLEAP_URL': 'https://analytics.ironleap.io/api/collect'
    'DEBUG': False,
    'LOG_BODY': True,
    'IDENTIFY_COMPANY': identify_company,
    'SKIP': should_skip,
    'MASK_EVENT_MODEL': mask_event,
    'GET_METADATA': get_metadata,
}

```

