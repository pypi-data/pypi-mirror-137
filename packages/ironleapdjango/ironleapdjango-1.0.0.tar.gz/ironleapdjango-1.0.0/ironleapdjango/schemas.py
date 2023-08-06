from datetime import datetime
import jsonpickle

class BaseModel(object):
    def to_dictionary(self):
        dictionary = dict()

        # Loop through all properties in this model
        for name in self.__dict__:
            value = getattr(self, name)
            if isinstance(value, list):
                # Loop through each item
                dictionary[name] = list()
                for item in value:
                    dictionary[name].append(item.to_dictionary() if isinstance(item, BaseModel) else item)
            elif isinstance(value, dict):
                # Loop through each item
                dictionary[name] = dict()
                for key in value:
                    dictionary[name][key] = value[key].to_dictionary() if isinstance(value[key], BaseModel) else value[key]
            elif isinstance(value, datetime):
                dictionary[name] = value.isoformat().to_dictionary() if isinstance(value, BaseModel) else value.isoformat()
            else:
                dictionary[name] = value.to_dictionary() if isinstance(value, BaseModel) else value
        # Return the result
        return dictionary

class APIEvent(BaseModel):
    def __init__(
        self,
        request = None,
        response = None,
        company_id = None,
        metadata = None
    ):
        self.request = request
        self.response = response
        self.company_id = company_id
        self.metadata = metadata

class APIRequest(BaseModel):
    def __init__(
        self,
        time = None,
        uri = None,
        verb = None,
        headers = None,
        body = None,
        transfer_encoding = None
    ):
        self.time = time
        self.uri = uri
        self.verb = verb
        self.headers = headers
        self.body = body
        self.transfer_encoding = transfer_encoding

class APIResponse(BaseModel):
    def __init__(
        self,
        time = None,
        status = None,
        headers = None,
        body = None,
        transfer_encoding = None
    ):
        self.time = time
        self.status = status
        self.headers = headers
        self.body = body
        self.transfer_encoding = transfer_encoding


def json_serialize(obj):
    """JSON Serialization of a given object.
    Args:
        obj (object): The object to serialise.
    Returns:
        str: The JSON serialized string of the object.
    """
    if obj is None:
        return None

    # Resolve any Names if it's one of our objects that needs to have this called on
    if isinstance(obj, list):
        value = list()
        for item in obj:
            if isinstance(item, BaseModel):
                value.append(item.to_dictionary())
            else:
                value.append(item)
        obj = value
    else:
        if isinstance(obj, BaseModel):
            obj = obj.to_dictionary()

    return jsonpickle.encode(obj, False)
