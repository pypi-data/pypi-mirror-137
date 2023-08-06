# Copyright (C) 2021 Flowdas Inc. & Dong-gweon Oh <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import falcon.asgi
from typeable import field
from ._config import EndPoint


class HttpEndPoint(EndPoint, kind='http'):
    _app = None

    uri_template: str = field(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_app().add_route(self.uri_template, self)

    @staticmethod
    def get_app():
        if HttpEndPoint._app is None:
            HttpEndPoint._app = falcon.asgi.App(cors_enable=True)
        return HttpEndPoint._app
