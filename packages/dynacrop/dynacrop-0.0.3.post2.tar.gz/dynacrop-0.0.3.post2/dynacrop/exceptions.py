class AuthenticationError(Exception):
    def __init__(self):
        super().__init__("Wrong or missing API key.")


class APIKeyNotSupplied(Exception):
    def __init__(self):
        super().__init__("API key not supplied.")


class HandlingResponseError(Exception):
    def __init__(self):
        super().__init__("""There was a unexpected problem processing the
        request.""")


class APIObjectNotFound(Exception):
    def __init__(self, url):
        super().__init__(f"API Object on {url} not found.")


class APIRequestNotValid(Exception):
    def __init__(self, error):
        super().__init__(f"API request is not valid: {error}.")


class UnexpectedServerError(Exception):
    def __init__(self):
        super().__init__("API encoutered unexpected "
                         "problems when processing the request.")


class ServiceNotImplementedError(Exception):
    def __init__(self):
        super().__init__("API does not recognize the requested service.")


class BadGatewayError(Exception):
    def __init__(self):
        super().__init__("API recieved an invalid response \
            from the upstream server.")


class ServiceUnavailableError(Exception):
    def __init__(self):
        super().__init__("DynaCrop API is temporarily unavailable.\
            Please try again later.")


class InvalidLayerSuppliedError(Exception):
    def __init__(self):
        super().__init__("The supplied layer is in invalid format. \
            Use constants.Layer instead.")


class PolygonNotReadyForProcessingError(Exception):
    def __init__(self, status):
        super().__init__(f"The polygon is not yet ready for processing. \
            Polygon status: {status}.")


class InvalidRenderingTypeError(Exception):
    def __init__(self, id, rendering_type):
        super().__init__(f"The processing request with id {id} is \
            of different type: {rendering_type}.")


class NotInAllowedResultTypesError(Exception):
    def __init__(self, rendering_type, allowed_result_types):
        super().__init__(f"Invalid result type for {rendering_type}. \
            Allowed result types are: \
            {[art.value for art in allowed_result_types]}.")


class InvalidResultSuppliedError(Exception):
    def __init__(self):
        super().__init__("The supplied result type is in invalid format. \
        Use constants.Result instead.")


class RequestHasNoData(Exception):
    def __init__(self, id):
        super().__init__(f"The request with id={id} has no data.")


class MissingID(Exception):
    def __init__(self, id):
        super().__init__("The object has no id.")


class IncorrectDateFormatError(Exception):
    def __init__(self):
        super().__init__("""Date from or date to are in incorrect format. Must
        be string of only date in ISO 8601""")
