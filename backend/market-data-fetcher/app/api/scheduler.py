from app.components.application import application
from flask import current_app


def resume():
    try:
        current_app.logger.info("Resume scheduler")
        application.get_scheduler().resume()
        return {"message": "Successfully resumed scheduler"}, 200
    except Exception as error:
        return {"message": "Unable to resume scheduler", "error": error}, 500


def pause():
    try:
        current_app.logger.info("Pause scheduler")
        application.get_scheduler().pause()
        return {"message": "Successfully pause scheduler"}, 200
    except Exception as error:
        return {"message": "Unable to pause scheduler", "error": error}, 500
