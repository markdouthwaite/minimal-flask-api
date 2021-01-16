from flask import Blueprint, Response


errors = Blueprint("errors", __name__)


@errors.app_errorhandler(Exception)
def server_error(error):
    return Response(f"Oops, got an error! {error}", status=500)
