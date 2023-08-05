# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.api.dtm_pb2 import (
    Activity,
    AgentStartup,
    ApplicationCreate,
    ApplicationUpdate,
    Poll,
    ServerActivity,
)


def get_message_name(msg):
    if isinstance(msg, Activity):
        name = "activity_application"

    elif isinstance(msg, AgentStartup):
        name = "agent_startup"

    elif isinstance(msg, ApplicationCreate):
        name = "applications_create"

    elif isinstance(msg, ApplicationUpdate):
        name = "update_application"

    elif isinstance(msg, ServerActivity):
        name = "activity_server"

    elif isinstance(msg, Poll):
        name = "applications_heartbeat"

    return name
