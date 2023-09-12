"""
This file (test_config.py) contains the unit tests for the config classes.

These tests checks configuration parameters.
"""


def test_development_config(app):
    app.config.from_object("app.components.config.DevelopmentConfig")
    assert app.config["DEBUG"]
    assert not app.config["TESTING"]


def test_testing_config(app):
    app.config.from_object("app.components.config.TestingConfig")
    assert not app.config["DEBUG"]
    assert app.config["TESTING"]
