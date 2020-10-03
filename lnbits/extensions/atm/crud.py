from datetime import datetime
from typing import List, Optional, Union
from lnbits.db import open_ext_db
from lnbits.helpers import urlsafe_short_hash

from .models import atmLink
import ecdsa
from hashlib import sha256


def create_atm_link(
    *,
    wallet_id: str,
    amount: int,
    used: int,
) -> ATMLink:

    with open_ext_db("atm") as db:

        link_id = urlsafe_short_hash()
        private_key = urlsafe_short_hash()
        db.execute(
            """
            INSERT INTO atm_link (
                id,
                wallet,
                private_key, 
                amount,
                used
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                link_id,
                wallet_id,
                private_key,
                amount,
                used,
            ),
        )
    return get_atm_link(link_id, 0)


def get_atm_link(link_id: str, hash_id=None, num=0) -> Optional[ATMLink]:
    with open_ext_db("atm") as db:
        row = db.fetchone("SELECT * FROM atm_link WHERE id = ?", (link_id,))
    if hash_id:
        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(link_id), curve=ecdsa.SECP256k1, hashfunc=sha256)
        if not vk.verify(bytes.fromhex(row[3]), hash_id):
            return None

    return ATMLink(**row) if row else None


def get_atm_links(wallet_ids: Union[str, List[str]]) -> List[ATMLink]:
    if isinstance(wallet_ids, str):
        wallet_ids = [wallet_ids]

    with open_ext_db("atm") as db:
        q = ",".join(["?"] * len(wallet_ids))
        rows = db.fetchall(f"SELECT * FROM atm_link WHERE wallet IN ({q})", (*wallet_ids,))

    return [ATMLink.from_row(row) for row in rows]


def update_atm_link(link_id: str, **kwargs) -> Optional[ATMLink]:
    q = ", ".join([f"{field[0]} = ?" for field in kwargs.items()])
    with open_ext_db("atm") as db:
        db.execute(f"UPDATE atm_link SET {q} WHERE id = ?", (*kwargs.values(), link_id))
        row = db.fetchone("SELECT * FROM atm_link WHERE id = ?", (link_id,))

    return ATMLink.from_row(row) if row else None


def delete_atm_link(link_id: str) -> None:
    with open_ext_db("atm") as db:
        db.execute("DELETE FROM atm_link WHERE id = ?", (link_id,))