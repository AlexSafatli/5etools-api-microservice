from http import HTTPStatus

from flask import Flask, jsonify
from marshmallow.exceptions import ValidationError

from fetools.config import Config
from fetools.extensions import cors, ma
from fetools.views import blueprint


def create_app(config_object=Config):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    ma.init_app(app)
    cors.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blueprint)


def register_errorhandlers(app):
    """Register error handlers."""
    @app.errorhandler(403)
    def handle_forbidden(error):
        return jsonify({'description': error.description}), error.code

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({'description': error.description}), error.code

    @app.errorhandler(422)
    def handle_unprocessable_entity(error):
        response = {
            'description': 'Input failed validation.',
            'errors': error.exc.messages,
        }
        return jsonify(response), HTTPStatus.BAD_REQUEST

    # Catch webargs validation errors and return them in JSON format
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        response = {
            'description': 'Input failed validation.',
            'errors': error.messages,
        }
        return jsonify(response), HTTPStatus.BAD_REQUEST
