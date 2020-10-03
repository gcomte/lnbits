from quart import url_for
from lnurl import Lnurl, LnurlWithdrawResponse, encode as lnurl_encode
from sqlite3 import Row
from typing import NamedTuple
import shortuuid  # type: ignore


class ATMLink(NamedTuple):
    id: str
    wallet: str
    title: str
    key: str
    amount: int
    used: int