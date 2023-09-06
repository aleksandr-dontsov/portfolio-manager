from flask import jsonify


class PortfolioManagerError(Exception):
    """Base class for exceptions in PortfolioManager App."""

    def __init__(self, status: int, detail: str):
        self.status = status
        self.detail = detail
        super().__init__(detail)

    def __str__(self):
        return self.detail


def make_error_response(status: int, detail: str):
    return jsonify({"detail": detail}), status
