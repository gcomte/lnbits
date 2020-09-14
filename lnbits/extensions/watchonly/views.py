from flask import g, abort, render_template
from http import HTTPStatus

from lnbits.decorators import check_user_exists, validate_uuids

from lnbits.extensions.watchonly import watchonly_ext
from .crud import get_payment


@watchonly_ext.route("/")
@validate_uuids(["usr"], required=True)
@check_user_exists()
def index():
    return render_template("watchonly/index.html", user=g.user)


@watchonly_ext.route("/<payment_id>")
def display(payment_id):
    link = get_payment(payment_id) or abort(HTTPStatus.NOT_FOUND, "Pay link does not exist.")

    return render_template("watchonly/display.html", link=link)