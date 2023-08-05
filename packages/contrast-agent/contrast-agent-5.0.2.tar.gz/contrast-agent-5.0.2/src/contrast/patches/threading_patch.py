# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys
import contrast
from contrast.extern.wrapt import register_post_import_hook
from contrast.agent.policy import patch_manager
from contrast.assess_extensions import cs_str
from contrast.utils.patch_utils import build_and_apply_patch

from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


START_METHOD = "start"
BOOTSTRAP_METHOD = "_bootstrap_inner"


def build_start_patch(orig_func, _):
    def start(__cs_self, *args, **kwargs):
        context = contrast.CS__CONTEXT_TRACKER.current()

        try:
            # TODO: PYT-1766 Remove the no cover pragma after we delete the get_thread_scope code
            # These 2 if statements are tested by test_inherit_parent_scope
            if cs_str.USE_CONTEXTVARS:  # pragma: no cover
                # Save the scope of the current active contextvars.Context to copy to the new thread
                __cs_self.cs__parent_scope = cs_str.get_current_scope()
            else:  # pragma: no cover
                # Save the scope of the current (creating) thread to copy to new thread
                __cs_self.cs__parent_scope = cs_str.get_thread_scope()
            # This is used to ensure that a child thread always runs with the parent
            # thread's request context even if the parent thread has exited as long as
            # the parent thread is in request context.
            __cs_self.cs__parent_context = context
        except Exception:
            logger.exception("Failed to instrument thread start")

        return orig_func(__cs_self, *args, **kwargs)

    return start


def build_bootstrap_inner_patch(orig_func, _):
    def _bootstrap_inner(__cs_self, *args, **kwargs):  # pragma: no cover
        # The new thread inherits the scope from the thread that created it
        try:
            if cs_str.USE_CONTEXTVARS:
                cs_str.set_exact_scope(__cs_self.cs__parent_scope)
            else:
                cs_str.create_thread_storage(__cs_self.cs__parent_scope)
        except Exception:
            logger.exception("Failed to initialize thread storage")

        with contrast.CS__CONTEXT_TRACKER.lifespan(__cs_self.cs__parent_context):
            # Ensure child thread still runs with the same parent request context
            # even if the parent thread has already exited as long as
            # the parent thread is in request context.
            result = orig_func(__cs_self, *args, **kwargs)

        try:
            if not cs_str.USE_CONTEXTVARS:
                cs_str.destroy_thread_storage()
        except Exception:
            logger.exception("Failed to tear down thread storage")

        # We expect result to be None, but this is done for consistency/safety
        return result

    return _bootstrap_inner


def patch_threading(threading_module):
    build_and_apply_patch(threading_module.Thread, START_METHOD, build_start_patch)
    # This instruments the method that actually runs inside the system thread
    build_and_apply_patch(
        threading_module.Thread, BOOTSTRAP_METHOD, build_bootstrap_inner_patch
    )


def register_patches():
    register_post_import_hook(patch_threading, "threading")


def reverse_patches():
    threading = sys.modules.get("threading")
    if not threading:
        return

    patch_manager.reverse_patches_by_owner(threading.Thread)
