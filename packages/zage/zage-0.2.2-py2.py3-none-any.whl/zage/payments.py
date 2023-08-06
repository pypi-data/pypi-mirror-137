import json
import requests
import base64
from uuid import uuid4


def create_headers(public_key, secret_key):
    auth = f"{public_key}:{secret_key}"
    encoded = base64.b64encode(str.encode(auth)).decode("utf-8")
    return {
        "Authorization": f"Basic {encoded}",
        "Idempotency-key": str(uuid4()),
    }


class Payments:
    def create_token(
        amount,
        on_success_endpoint,
        user_id=None,
        metadata=None,
        transfers=None,
    ):
        from . import public_key, secret_key, base_url, sandbox_url

        if not secret_key or not public_key:
            raise ValueError("You must specify your secret and public keys.")

        url_base = (
            sandbox_url
            if secret_key.startswith("sandbox")
            and public_key.startswith("sandbox")
            else base_url
        )

        headers = create_headers(public_key, secret_key)
        data = {"amount": amount, "webhook": on_success_endpoint}

        if metadata:
            if isinstance(metadata, dict):
                data["metadata"] = json.dumps(metadata)
            elif isinstance(metadata, str):
                data["metadata"] = metadata
            else:
                data["metadata"] = str(metadata)
        if user_id:
            data["userId"] = user_id

        if transfers:
            if isinstance(transfers, list):
                data["transfers"] = transfers
            else:
                print("Improperly specified transfers, please reconcile")
        try:
            url = url_base + "payments"
            r = requests.post(url, data=json.dumps(data), headers=headers)
            r.raise_for_status()
            obj = dict(r.json())
            return obj.get("paymentTokenId")
        except requests.exceptions.Timeout:
            return Payments.create_token(
                amount,
                on_success_endpoint,
                user_id=user_id,
                metadata=metadata,
                transfers=transfers,
            )
        except requests.exceptions.HTTPError as err:
            raise TypeError(err)
        except requests.exceptions.ConnectionError as errc:
            raise ConnectionRefusedError(errc)
        except Exception:
            raise ValueError(
                "Unable to create payment token. Please try again."
            )

    def refund_payment(payment_id):
        from . import secret_key, public_key, base_url, sandbox_url

        if not secret_key or not public_key:
            raise ValueError("You must specify your secret and public keys.")

        url_base = (
            sandbox_url
            if secret_key.startswith("sandbox")
            and public_key.startswith("sandbox")
            else base_url
        )

        headers = create_headers(public_key, secret_key)

        try:
            request_url = url_base + "payments/" + payment_id + "/refund"
            r = requests.post(request_url, headers=headers)
            return r.status_code == 200
        except requests.exceptions.Timeout:
            return Payments.refund_payment(payment_id)
        except requests.exceptions.HTTPError as err:
            raise TypeError(err)
        except requests.exceptions.ConnectionError as errc:
            raise ConnectionRefusedError(errc)
        except Exception:
            raise ValueError("Unable to refund payment. Please try again.")
