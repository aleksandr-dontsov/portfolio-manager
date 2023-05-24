class PortmanError(Exception):
    """Base class for exceptions in Portfolio Manager App."""

    def __init__(self, status: int, detail: str):
        self.status = status
        self.detail = detail
        super().__init__(detail)

    def __str__(self):
        return self.detail


def make_error_response(status: int, detail: str):
    return {"status": status, "detail": detail}, status
