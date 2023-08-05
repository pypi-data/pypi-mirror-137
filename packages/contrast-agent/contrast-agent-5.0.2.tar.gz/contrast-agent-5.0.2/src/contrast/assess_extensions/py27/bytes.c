/*
 * Copyright © 2022 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* THIS FILE WAS AUTOMATICALLY GENERATED BY HOOKSPY */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/patches.h>
#include <contrast/assess/propagate.h>
#include <contrast/assess/scope.h>
#include <contrast/assess/utils.h>

typedef PyObject *(*fastcall_func)(PyObject *, PyObject *const *, Py_ssize_t);
typedef PyObject *(*fastcall_kwargs_func)(
    PyObject *, PyObject *const *, Py_ssize_t, PyObject *);

#define BYTES_ENCODE_OFFSET 37
#define BYTES_DECODE_OFFSET 38
#define BYTES_REPLACE_OFFSET 19
#define BYTES_SPLIT_OFFSET 1
#define BYTES_RSPLIT_OFFSET 2
#define BYTES_JOIN_OFFSET 0
#define BYTES_CAPITALIZE_OFFSET 12
#define BYTES_TITLE_OFFSET 28
#define BYTES_CENTER_OFFSET 31
#define BYTES_EXPANDTABS_OFFSET 39
#define BYTES_PARTITION_OFFSET 15
#define BYTES_LJUST_OFFSET 29
#define BYTES_LOWER_OFFSET 3
#define BYTES_LSTRIP_OFFSET 18
#define BYTES_RJUST_OFFSET 30
#define BYTES_RSTRIP_OFFSET 22
#define BYTES_RPARTITION_OFFSET 23
#define BYTES_SPLITLINES_OFFSET 40
#define BYTES_STRIP_OFFSET 25
#define BYTES_SWAPCASE_OFFSET 26
#define BYTES_TRANSLATE_OFFSET 27
#define BYTES_UPPER_OFFSET 4
#define BYTES_ZFILL_OFFSET 32

ternaryfunc bytes_encode_orig;
ternaryfunc bytes_decode_orig;
binaryfunc bytes_replace_orig;
binaryfunc bytes_split_orig;
binaryfunc bytes_rsplit_orig;
binaryfunc bytes_join_orig;
unaryfunc bytes_capitalize_orig;
unaryfunc bytes_title_orig;
binaryfunc bytes_center_orig;
binaryfunc bytes_expandtabs_orig;
binaryfunc bytes_partition_orig;
binaryfunc bytes_ljust_orig;
unaryfunc bytes_lower_orig;
binaryfunc bytes_lstrip_orig;
binaryfunc bytes_rjust_orig;
binaryfunc bytes_rstrip_orig;
binaryfunc bytes_rpartition_orig;
binaryfunc bytes_splitlines_orig;
binaryfunc bytes_strip_orig;
unaryfunc bytes_swapcase_orig;
binaryfunc bytes_translate_orig;
unaryfunc bytes_upper_orig;
binaryfunc bytes_zfill_orig;

HOOK_TERNARYFUNC(bytes_encode);
HOOK_TERNARYFUNC(bytes_decode);
HOOK_BINARYFUNC(bytes_replace);
HOOK_BINARYFUNC(bytes_split);
HOOK_BINARYFUNC(bytes_rsplit);
PyObject *bytes_join_new(PyObject *self, PyObject *args) {
    PyObject *list = PySequence_List(args);

    /* If this fails for any reason, just call the original function and get
     * out of here.
     */
    if (list == NULL) {
        PyErr_Clear();
        return bytes_join_orig((PyObject *)self, args);
    }

    /* In Py36+ we also hook an internal function that is called by this
     * function in order to propagate fstring formatting. We still want to have
     * a separate hook for join so that the events are reported differently.
     * This means that we need to go into scope when calling the original
     * function here so that we don't propagate twice.
     */
    enter_propagation_scope();
    PyObject *result = bytes_join_orig((PyObject *)self, list);
    exit_propagation_scope();

    PyObject *prop_args = PyTuple_Pack(1, list);

    if (prop_args == NULL || result == NULL)
        goto cleanup_and_exit;

    call_string_propagator(
        "propagate_bytes_join", (PyObject *)self, result, prop_args, NULL);

cleanup_and_exit:
    Py_XDECREF(list);
    Py_XDECREF(prop_args);
    return result;
}

HOOK_UNARYFUNC(bytes_capitalize);
HOOK_UNARYFUNC(bytes_title);
HOOK_BINARYFUNC(bytes_center);
HOOK_BINARYFUNC(bytes_expandtabs);
HOOK_BINARYFUNC(bytes_partition);
HOOK_BINARYFUNC(bytes_ljust);
HOOK_UNARYFUNC(bytes_lower);
HOOK_BINARYFUNC(bytes_lstrip);
HOOK_BINARYFUNC(bytes_rjust);
HOOK_BINARYFUNC(bytes_rstrip);
HOOK_BINARYFUNC(bytes_rpartition);
HOOK_BINARYFUNC(bytes_splitlines);
HOOK_BINARYFUNC(bytes_strip);
HOOK_UNARYFUNC(bytes_swapcase);
HOOK_BINARYFUNC(bytes_translate);
HOOK_UNARYFUNC(bytes_upper);
HOOK_BINARYFUNC(bytes_zfill);

CREATE_HOOK_METHOD(PyBytes_Type, bytes_encode, 37)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_decode, 38)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_replace, 19)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_split, 1)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_rsplit, 2)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_join, 0)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_capitalize, 12)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_title, 28)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_center, 31)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_expandtabs, 39)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_partition, 15)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_ljust, 29)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_lower, 3)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_lstrip, 18)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_rjust, 30)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_rstrip, 22)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_rpartition, 23)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_splitlines, 40)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_strip, 25)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_swapcase, 26)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_translate, 27)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_upper, 4)
CREATE_HOOK_METHOD(PyBytes_Type, bytes_zfill, 32)

static PyMethodDef methods[] = {
    {"apply_encode_hook", apply_bytes_encode_hook, METH_O, "Enable bytes.encode hook"},
    {"apply_decode_hook", apply_bytes_decode_hook, METH_O, "Enable bytes.decode hook"},
    {"apply_replace_hook",
     apply_bytes_replace_hook,
     METH_O,
     "Enable bytes.replace hook"},
    {"apply_split_hook", apply_bytes_split_hook, METH_O, "Enable bytes.split hook"},
    {"apply_rsplit_hook", apply_bytes_rsplit_hook, METH_O, "Enable bytes.rsplit hook"},
    {"apply_join_hook", apply_bytes_join_hook, METH_O, "Enable bytes.join hook"},
    {"apply_capitalize_hook",
     apply_bytes_capitalize_hook,
     METH_O,
     "Enable bytes.capitalize hook"},
    {"apply_title_hook", apply_bytes_title_hook, METH_O, "Enable bytes.title hook"},
    {"apply_center_hook", apply_bytes_center_hook, METH_O, "Enable bytes.center hook"},
    {"apply_expandtabs_hook",
     apply_bytes_expandtabs_hook,
     METH_O,
     "Enable bytes.expandtabs hook"},
    {"apply_partition_hook",
     apply_bytes_partition_hook,
     METH_O,
     "Enable bytes.partition hook"},
    {"apply_ljust_hook", apply_bytes_ljust_hook, METH_O, "Enable bytes.ljust hook"},
    {"apply_lower_hook", apply_bytes_lower_hook, METH_O, "Enable bytes.lower hook"},
    {"apply_lstrip_hook", apply_bytes_lstrip_hook, METH_O, "Enable bytes.lstrip hook"},
    {"apply_rjust_hook", apply_bytes_rjust_hook, METH_O, "Enable bytes.rjust hook"},
    {"apply_rstrip_hook", apply_bytes_rstrip_hook, METH_O, "Enable bytes.rstrip hook"},
    {"apply_rpartition_hook",
     apply_bytes_rpartition_hook,
     METH_O,
     "Enable bytes.rpartition hook"},
    {"apply_splitlines_hook",
     apply_bytes_splitlines_hook,
     METH_O,
     "Enable bytes.splitlines hook"},
    {"apply_strip_hook", apply_bytes_strip_hook, METH_O, "Enable bytes.strip hook"},
    {"apply_swapcase_hook",
     apply_bytes_swapcase_hook,
     METH_O,
     "Enable bytes.swapcase hook"},
    {"apply_translate_hook",
     apply_bytes_translate_hook,
     METH_O,
     "Enable bytes.translate hook"},
    {"apply_upper_hook", apply_bytes_upper_hook, METH_O, "Enable bytes.upper hook"},
    {"apply_zfill_hook", apply_bytes_zfill_hook, METH_O, "Enable bytes.zfill hook"},
    {NULL, NULL, 0, NULL},
};

PyObject *create_bytes_hook_module(PyObject *self, PyObject *arg) {
    return Py_InitModule("bytes_hooks", methods);
}
