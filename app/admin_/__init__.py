from flask import Blueprint

bp = Blueprint('admin_', __name__)

from app.admin_ import routes