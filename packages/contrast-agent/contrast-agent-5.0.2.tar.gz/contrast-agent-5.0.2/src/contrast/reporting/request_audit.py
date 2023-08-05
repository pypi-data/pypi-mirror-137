# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from datetime import datetime
import json
from pathlib import Path
from os import path
from contrast import AGENT_CURR_WORKING_DIR
from contrast.extern import structlog as logging
from contrast.api.utils import get_message_name
from contrast.utils.decorators import fail_safely

logger = logging.getLogger("contrast")


class RequestAudit(object):
    SUB_DIRS = ("requests", "responses")

    def __init__(self, config):
        self.config = config
        self.messages_path = ""

    @fail_safely("Unable to prepare request_audit dirs")
    def prepare_dirs(self):
        # grab config request audit path, or the default, write /messages dir
        # create requests/response subdirs under message
        parent_path = self.config.get("api.request_audit.path")

        parent_path = path.join(AGENT_CURR_WORKING_DIR, parent_path.strip("/"))
        if "messages" in parent_path:
            self.messages_path = parent_path
        else:
            self.messages_path = path.join(parent_path, "messages")

        for sub_dir in self.SUB_DIRS:
            sub_path = path.join(self.messages_path, sub_dir)
            Path(sub_path).mkdir(parents=True, exist_ok=True)

        logger.debug(f"Created request_audit dirs in %s", self.messages_path)

    def audit(self, msg, response):
        if self.config.get("api.request_audit.requests"):
            msg_name = get_message_name(msg)
            self.write_data(msg, "requests", msg_name)

        if self.config.get("api.request_audit.responses"):
            response_name = get_message_name(response)
            self.write_data(response, "responses", response_name)

    @fail_safely("Unable to write request audit data")
    def write_data(self, msg, msg_type, msg_name):
        now = datetime.now()
        epoch = now.timestamp()
        day = now.strftime("%Y%m%d")
        time = f"{day}-{epoch}"

        file_name = f"{time}-{msg_name}-teamserver.json"
        file_path = path.join(self.messages_path, msg_type, file_name)
        data = str(msg)  # this will be replaced by future tickets with msg data

        with Path(file_path).open("w", encoding="UTF-8") as target:
            json.dump(data, target)

    def write_response(self, response):
        pass
