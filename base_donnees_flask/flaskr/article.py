from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("article", __name__)


@bp.route("/")
def index():
    """Show all the articles, most recent first."""
    db = get_db()
    articles = db.execute(
        "SELECT article_id, category_id, publisher_id, words_count"
        " FROM article"
        " ORDER BY created_at_ts DESC"
    ).fetchall()
    return render_template("article/index.html", articles=articles)
