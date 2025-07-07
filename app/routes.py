from flask import Blueprint, jsonify
from app import db
from app.models import Menu

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return jsonify({ "status": "ok" })

@bp.route('/menu')
def menu():
    today = Menu.query.first()
    if today:
        body = { "today_special": today.name }
        status = 200
    else:
        body = { "error": "Sorry, the service is not available today." }
        status = 404
    return jsonify(body), status
