class NoTokenFoundException(Exception):
    pass


class AuthFailedException(Exception):
    pass


error_code_map = {
    200: "Ok.",
    400: "Bad Request.",
    401: "Unauthorized. Please make sure that the HTTP API is enabled and supply a Bearer token via the Authorization header.",
    403: "Forbidden. Please make sure that the HTTP API is enabled and supply a valid Bearer token via the Authorization header.",
    404: "Not Found.",
    500: "Internal Server Error."
}

