# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
class ContrastServiceException(Exception):
    def __init__(self):
        message = "Unable to connect or send messages to Contrast Service."
        super().__init__(message)
