from flask import Blueprint

from .handling import your_endpoint
from .utils import render_template


def init_routes(bp: Blueprint):
    @bp.route("/")
    def index():
        return render_template("index.html")


    @bp.route("/your-endpoint", methods=["GET", "POST"])
    def endpoint():
        return your_endpoint.handle_request()
