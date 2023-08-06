# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

from types import FunctionType

from .payload_auth import PayloadAuth


class HubCapability:

    _wellknown_payload_identifier: str = None
    _friendly_name: str = None
    _description: str = None
    _payload_auth: PayloadAuth = None

    _task: FunctionType = None

    _rpc_type = None

    def __init__(self, wellknown_payload_identifier: str, task: FunctionType, friendly_name: str, description: str, payload_auth: PayloadAuth):
        self._wellknown_payload_identifier = wellknown_payload_identifier
        self._friendly_name = friendly_name
        self._description = description
        self._payload_auth = payload_auth

        self._task = task

    @property
    def wellknown_payload_identifier(self) -> str:
        return self._wellknown_payload_identifier

    @property
    def friendly_name(self) -> str:
        return self._friendly_name

    @property
    def description(self) -> str:
        return self._description

    @property
    def payload_auth(self) -> PayloadAuth:
        return self._payload_auth

    @property
    def task(self) -> FunctionType:
        return self._task
