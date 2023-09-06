from app.components.application import application
from flask import current_app


def check():
    try:
        current_app.logger.info("Check service health")
        application.get_publisher().ping()
        return {"message": "The service is healthy"}, 200
    except Exception as error:
        return {"message": "The service is unhealthy", "error": error}, 503
