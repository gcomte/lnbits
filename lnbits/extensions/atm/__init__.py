from quart import Blueprint


atm_ext: Blueprint = Blueprint("atm", __name__, static_folder="static", template_folder="templates")


from .views_api import *  # noqa
from .views import *  # noqa
