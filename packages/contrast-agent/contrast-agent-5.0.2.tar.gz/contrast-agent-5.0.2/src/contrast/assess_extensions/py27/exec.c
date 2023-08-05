/*
 * Copyright © 2022 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <funchook.h>

#include <contrast/assess/patches.h>
#include <contrast/assess/propagate.h>
#include <contrast/assess/utils.h>

/* Don't need to hook PyRun_String since it's just a macro that calls this */
PyAPI_FUNC(PyObject *) (*PyRun_StringFlags_orig)(
    const char *str, int start, PyObject *, PyObject *, PyCompilerFlags *);
unaryfunc PyUnicode_AsUTF8String_orig;

/* The exec statement calls PyRun_StringFlags under the hood if the argument
 * to exec is a str or unicode object. These should be the only kinds of types
 * that we care about for implementing this rule. The catch is that
 * PyRun_StringFlags does not take a PyObject * as an argument, but instead
 * takes the underlying char * which corresponds to a str or unicode object.
 * Since this is the only available hook point we have for the exec statement,
 * we need to maintain a mapping between Python objects and the underlying
 * char buffers.
 */
PyAPI_FUNC(PyObject *) PyRun_StringFlags_new(
    const char *str,
    int start,
    PyObject *globals,
    PyObject *locals,
    PyCompilerFlags *flags) {
    /* This is safe, any errors will be handled inside this call */
    apply_exec_hook(str);
    return PyRun_StringFlags_orig(str, start, globals, locals, flags);
}

/* If the argument to the exec statement is a unicode object, the interpreter
 * will first encode it into UTF-8 before passing the underlying buffer to
 * PyRun_StringFlags. This function does not call any of our existing encode
 * propagators so we need to add a new one here in order to make sure that we
 * can see tracked strings at the call to PyRun_StringFlags.
 */
PyObject *PyUnicode_AsUTF8String_new(PyObject *unicode) {
    PyObject *result = PyUnicode_AsUTF8String_orig(unicode);
    PyObject *args = PyTuple_Pack(1, unicode);

    if (result == NULL)
        goto cleanup_and_exit;

    call_string_propagator("propagate_unicode_encode", unicode, result, args, NULL);

cleanup_and_exit:
    Py_XDECREF(args);
    return result;
}

int apply_exec_patches(funchook_t *funchook) {
    PyRun_StringFlags_orig = PyRun_StringFlags;
    PyUnicode_AsUTF8String_orig = PyUnicode_AsUTF8String;

    funchook_prep_wrapper(funchook, &PyRun_StringFlags_orig, PyRun_StringFlags_new);
    funchook_prep_wrapper(
        funchook, &PyUnicode_AsUTF8String_orig, PyUnicode_AsUTF8String_new);

    return 0;
}
