from flask import jsonify
from marshmallow.exceptions import ValidationError
from core import app
from core.apis.assignments import student_assignments_resources, teacher_assignments_resources
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')


@app.route('/')
def ready():
    response = jsonify({
        'status': 'ready',
        'time': helpers.get_utc_now()
    })
    return response


@app.errorhandler(FyleError)
def handle_fyle_error(err):
    return jsonify(error=err.__class__.__name__, message=err.message), err.status_code


@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify(error=err.__class__.__name__, message=err.messages), 400


@app.errorhandler(IntegrityError)
def handle_integrity_error(err):
    return jsonify(error=err.__class__.__name__, message=str(err.orig)), 400


@app.errorhandler(HTTPException)
def handle_http_exception(err):
    return jsonify(error=err.__class__.__name__, message=str(err)), err.code


@app.errorhandler(Exception)
def handle_generic_error(err):
    app.logger.exception(err)
    return jsonify(error=err.__class__.__name__, message=str(err)), 500
