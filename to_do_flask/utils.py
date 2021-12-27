import json
from typing import Dict
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app, Response


def handle_errors(e: Exception):
    return {'error': str(e)}


def handle_db_errors(e: SQLAlchemyError):
    current_app.db.session.remove()
    return {
        'error': e.__class__.__name__,
        'description': str(e)
    }


def bytes_to_json(data: Response) -> Dict:
    return json.loads(data.data.decode('utf-8'))
