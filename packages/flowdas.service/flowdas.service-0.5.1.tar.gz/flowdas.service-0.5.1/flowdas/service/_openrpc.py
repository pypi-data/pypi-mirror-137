# Copyright (C) 2021 Flowdas Inc. & Dong-gweon Oh <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typeable import Object, field, JsonSchema
from typeable.typing import List, Union, Dict, Literal, Any


#
# OpenRPC v1.2.6
#


class Contact(Object):
    name: str
    url: str
    email: str


class License(Object):
    name: str = field(required=True)
    url: str


class Info(Object):
    title: str = field(required=True)
    description: str
    termsOfService: str
    contact: Contact
    license: License
    version: str = field(required=True)


class RuntimeExpression(Object):
    pass


class ServerVariable(Object):
    enum: List[str]
    default: str = field(required=True)
    description: str


class Server(Object):
    name: str = field(required=True)
    url: RuntimeExpression = field(required=True)
    summary: str
    description: str
    variables: Dict[str, ServerVariable]


class ExternalDocs(Object):
    description: str
    url: str = field(required=True)


class Tag(Object):
    name: str
    sumary: str
    description: str
    externalDocs: ExternalDocs


class Reference(Object):
    ref: str = field(key='$ref', required=True)


class ContentDescriptor(Object):
    name: str = field(required=True)
    summary: str
    description: str
    required: bool = False
    schema: Union[JsonSchema, Reference] = field(required=True)
    deprecated: bool = False


class Error(Object):
    code: int = field(required=True)
    message: str = field(required=True)
    data: Any


class Link(Object):
    name: str
    description: str
    summary: str
    method: str
    params: Dict[str, Union[RuntimeExpression, Any]]
    server: Server


class Example(Object):
    name: str
    summary: str
    description: str
    value: Any
    externalValue: str


class ExamplePairing(Object):
    name: str
    description: str
    summary: str
    params: List[Union[Example, Reference]]
    result: Union[Example, Reference]


class Method(Object):
    name: str = field(required=True)
    tags: List[Union[Tag, Reference]]
    summary: str
    description: str
    externalDocs: ExternalDocs
    params: List[Union[ContentDescriptor, Reference]] = field(required=True)
    result: Union[ContentDescriptor, Reference] = field(required=True)
    deprecated: bool = False
    servers: List[Server]
    errors: List[Union[Error, Reference]]
    links: List[Union[Link, Reference]]
    paramStructure: Literal['by-name', 'by-position', 'either']
    examples: List[ExamplePairing]


class Components(Object):
    contentDescriptors: Dict[str, ContentDescriptor]
    schemas: Dict[str, Union[JsonSchema, Reference]]
    examples: Dict[str, Example]
    links: Dict[str, Link]
    errors: Dict[str, Error]
    examplePairingObjects: Dict[str, ExamplePairing]
    tags: Dict[str, Tag]


class Document(Object, jsonschema='https://raw.githubusercontent.com/open-rpc/meta-schema/master/schema.json'):
    openrpc: str = field(required=True)
    info: Info = field(required=True)
    servers: List[Server]  # TODO: default server
    methods: List[Union[Method, Reference]] = field(required=True)
    components: Components
    externalDocs: ExternalDocs
