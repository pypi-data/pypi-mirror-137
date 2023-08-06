#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Tradologics Python SDK
# https://tradologics.com
#
# Copyright Tradologics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import requests
from . import __version__


_SANDBOX_URL = "https://api.tradologics.com/v1/sandbox"

_TOKEN = None


def set_token(token):
    global _TOKEN
    _TOKEN = f'Bearer {token}'


def tradehook(kind: str, strategy: callable, **kwargs):
    """
    authorization required

    Parameters
    ----------
    kind : available kinds: ["bar", "order", "order_{YOUR_STATUS}  (example: "order_filled")", "position",
    "position_expire", "price", "price_expire", "error"]
    strategy : callback
    kwargs : payload

    Returns
    -------
    json obj
    """

    url = f'{_SANDBOX_URL}/{kind.replace("_", "/")}'
    headers = {'Authorization': _TOKEN, 'TGX-CLIENT': f'python-sdk/{__version__}'}
    result = requests.get(url, data=json.dumps(kwargs), headers=headers)
    strategy(kind.split('_')[0], result.json())


def bar(strategy: callable, **kwargs):
    """ shorthand for tradehook(bar, ...) """
    tradehook("bar", strategy, **kwargs)


def monitor(kind: str, strategy: callable, **kwargs):
    """ generic monitor wrapper """
    tradehook(kind, strategy, **kwargs)


def monitor_expired(kind: str, strategy: callable, **kwargs):
    """ generic monitor expired wrapper """
    tradehook(f"{kind}_expire", strategy, **kwargs)


def position_monitor(strategy: callable, **kwargs):
    """ shorthand for tradehook(position, ...) """
    tradehook("position", strategy, **kwargs)


def position_monitor_expired(strategy: callable, **kwargs):
    """ shorthand for tradehook(position_expire, ...) """
    tradehook("position_expire", strategy, **kwargs)


def price_monitor(strategy: callable, **kwargs):
    """ shorthand for tradehook(price, ...) """
    tradehook("price", strategy, **kwargs)


def price_monitor_expired(strategy: callable, **kwargs):
    """ shorthand for tradehook(price_expire, ...) """
    tradehook("price_expire", strategy, **kwargs)


def error(strategy, **kwargs):
    """ shorthand for tradehook(error, ...) """
    tradehook("error", strategy, **kwargs)


def order(kind: str, strategy: callable, **kwargs):
    """ generic order wrapper """
    tradehook(f"order_{kind}", strategy, **kwargs)


def order_received(strategy, **kwargs):
    """ shorthand for tradehook(order_received, ...) """
    tradehook("order_received", strategy, **kwargs)


def order_pending(strategy, **kwargs):
    """ shorthand for tradehook(order_pending, ...) """
    tradehook("order_pending", strategy, **kwargs)


def order_submitted(strategy, **kwargs):
    """ shorthand for tradehook(order_submitted, ...) """
    tradehook("order_submitted", strategy, **kwargs)


def order_sent(strategy, **kwargs):
    """ shorthand for tradehook(order_sent, ...) """
    tradehook("order_sent", strategy, **kwargs)


def order_accepted(strategy, **kwargs):
    """ shorthand for tradehook(order_accepted, ...) """
    tradehook("order_accepted", strategy, **kwargs)


def order_partially_filled(strategy, **kwargs):
    """ shorthand for tradehook(order_partially_filled, ...) """
    tradehook("order_partially_filled", strategy, **kwargs)


def order_filled(strategy, **kwargs):
    """ shorthand for tradehook(order_filled, ...) """
    tradehook("order_filled", strategy, **kwargs)


def order_canceled(strategy, **kwargs):
    """ shorthand for tradehook(order_canceled, ...) """
    tradehook("order_canceled", strategy, **kwargs)


def order_expired(strategy, **kwargs):
    """ shorthand for tradehook(order_expired, ...) """
    tradehook("order_expired", strategy, **kwargs)


def order_pending_cancel(strategy, **kwargs):
    """ shorthand for tradehook(order_pending_cancel, ...) """
    tradehook("order_pending_cancel", strategy, **kwargs)


def order_rejected(strategy, **kwargs):
    """ shorthand for tradehook(order_rejected, ...) """
    tradehook("order_rejected", strategy, **kwargs)
