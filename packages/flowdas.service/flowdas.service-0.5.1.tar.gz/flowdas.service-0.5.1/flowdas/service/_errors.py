# Copyright (C) 2021 Flowdas Inc. & Dong-gweon Oh <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import falcon


class JSONRPCParseError(falcon.HTTPBadRequest):
    def __init__(self, data):
        super().__init__(code=-32700, title='Parse error', description=data)


class JSONRPCInvalidRequestError(falcon.HTTPBadRequest):
    def __init__(self, location):
        super().__init__(code=-32600, title='Invalid Request', description=location)


class JSONRPCMethodNotFoundError(falcon.HTTPBadRequest):
    def __init__(self):
        super().__init__(code=-32601, title='Method not found')


class JSONRPCInvalidParamsError(falcon.HTTPBadRequest):
    def __init__(self, location):
        super().__init__(code=-32602, title='Invalid params', description=location)


class JSONRPCInternalError(falcon.HTTPInternalServerError):
    def __init__(self):
        super().__init__(code=-32603, title='Internal error')


class HTTPUnsupportedMediaType(falcon.HTTPUnsupportedMediaType):
    def __init__(self):
        super().__init__(code=-32000)


class HTTPLengthRequired(falcon.HTTPLengthRequired):  # pragma: no cover
    def __init__(self):
        super().__init__(code=-32001)


class HTTPPayloadTooLarge(falcon.HTTPPayloadTooLarge):
    def __init__(self):
        super().__init__(code=-32002)
