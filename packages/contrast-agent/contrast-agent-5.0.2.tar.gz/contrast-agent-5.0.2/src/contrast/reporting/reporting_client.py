# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.settings_state import SettingsState
from contrast.reporting import RequestAudit
from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


class ReportingClient(object):
    def __init__(self):
        self.settings = SettingsState()
        self.request_audit = (
            RequestAudit(self.settings.config)
            if self.settings.config.is_request_audit_enabled
            else None
        )

        if self.request_audit:
            self.request_audit.prepare_dirs()

    def send_messages(self, messages):
        for message in messages:
            response = self.send_message(message)

            if self.request_audit:
                self.request_audit.audit(message, response)

    def send_message(self, msg):
        logger.debug("Will send ContrastUI msg later on.")
        response = {}
        return response
