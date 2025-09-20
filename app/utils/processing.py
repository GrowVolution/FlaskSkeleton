from flask import request, render_template
from werkzeug.exceptions import NotFound

from ..utils import random_code
from ..socket import default_handlers, no_handler
from utils.debugger import log, exception


def context_processor():
    return dict()


def before_request():
    method = request.method.upper()
    path = request.path
    ip = request.remote_addr
    agent = request.headers.get("User-Agent")
    agent = agent if agent else "no-agent"

    log("request", f"{method:4} '{path:48}' from {ip:15} via ({agent}).")


def after_request(response):
    return response


def handle_app_error(error):
    if isinstance(error, NotFound):
        return render_template("404.html"), 404

    eid = random_code()
    exception(error, f"Handling app request failed ({eid}).")
    return render_template("error.html"), 501


def socket_event_handler(data: dict):
    event = data["event"]
    payload = data.get("payload")
    log("request", f"Socket event: {event} - With data: {payload}")

    handler = default_handlers.get(event, no_handler)
    return handler(payload)


def handle_socket_error(error):
    eid = random_code()
    exception(error, f"Handling socket event failed ({eid}).")

    return { "error": "Error while handling socket event." }
