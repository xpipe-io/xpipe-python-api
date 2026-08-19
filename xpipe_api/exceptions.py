class NoTokenFoundException(Exception):
    pass


class AuthFailedException(Exception):
    pass


error_code_map = {
    200: "Ok.",
    400: "Bad Request.",
    401: "Unauthorized. Please make sure that the HTTP API is enabled in the settings menu and that the authentication is correctly configured.",
    403: "Forbidden. Please make sure that the HTTP API is enabled in the settings menu and that the authentication is correctly configured.",
    404: "Not Found.",
    500: "Internal Server Error."
}

