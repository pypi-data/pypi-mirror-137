import hmac
import hashlib
import json
from typing import Any, Dict, Optional

import requests

from ekata_gateway_processor_helper.constants import (
    EKATA_GATEWAY_PROCESSOR_MAINNET_API_URL,
    EKATA_GATEWAY_PROCESSOR_TESTNET_API_URL
)
from ekata_gateway_processor_helper.exceptions import (
    InvalidAPIKeyException, InvalidArgumentsException,
    InvalidProjectException, NoEnabledCurrencyException
)


def create_payment_form(
        amount: int,
        fiat_currency: str,
        project_id: str,
        api_key: str,
        testnet: bool = False) -> Optional[str]:
    data = {
        'amount_requested': amount,
        'fiat_currency': fiat_currency,
        'project_id': project_id,
        'api_key': api_key
    }
    api_url = EKATA_GATEWAY_PROCESSOR_MAINNET_API_URL \
        if not testnet else EKATA_GATEWAY_PROCESSOR_TESTNET_API_URL
    res = requests.post(f"{api_url}/payment-form/create", json=data)
    if res.status_code == 200:
        data = res.json()
        return data['id']
    if res.status_code == 404:
        content = json.loads(res.content)
        raise InvalidProjectException(message=content['detail'])
    if res.status_code == 400:
        content = json.loads(res.content)
        detail = content['detail']
        if detail == 'API key mismatch':
            raise InvalidAPIKeyException(message=detail)
        if detail == 'Project have no enabled currency':
            raise NoEnabledCurrencyException(message=detail)
    if res.status_code == 422:
        content = json.loads(res.content)
        details = content['detail']
        invalid_args = []
        for detail in details:
            invalid_args.append({
                detail['loc'][1]: detail['msg']
            })
        raise InvalidArgumentsException(arguments=invalid_args)


def verify_payload(payload: Dict[str, Any], signature_secret: str) -> bool:
    message = f"{payload['payment_id']}" + \
        f"{payload['wallet_address']}" + \
        f"{payload['currency_name']}"
    signature = hmac.new(
        signature_secret.encode(),
        message.encode(),
        hashlib.sha256).hexdigest()
    return signature == payload['signature']
