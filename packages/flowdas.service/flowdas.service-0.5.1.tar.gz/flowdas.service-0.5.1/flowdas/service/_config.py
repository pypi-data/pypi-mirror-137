# Copyright (C) 2021 Flowdas Inc. & Dong-gweon Oh <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typeable import *
from typeable.typing import *


class EndPoint(Object):
    type: str = field(kind=True)


class Uvicorn(Object):
    host: str = '127.0.0.1'
    port: int = 8000
    log_level: str = None
    debug: bool = False


class Config(Object):
    debug: bool = False
    endpoints: List[EndPoint] = field(default_factory=lambda: [{'type': 'console'}, {'type': 'jsonrpc'}])
    uvicorn: Uvicorn = field(default_factory=lambda: {})
    sentry: str = ''
