/*
 * Copyright © 2022 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <assert.h>
#include <ctype.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>

#include <funchook.h>

#include <contrast/assess/patches.h>
#include <contrast/assess/propagate.h>
#include <contrast/assess/scope.h>
#include <contrast/assess/utils.h>

/*
 * Concat:
 *
 * Combines two strings into a new string
 *
 * Source: Origin/Self
 * Target: Return
 * Action: Append
 */

void (*str_cat_orig)(PyObject **, PyObject *); /* used for PyString_Concat */
binaryfunc str_concat_orig;                    /* used for the sq_concat method */
binaryfunc unicode_cat_orig;                   /* used for PyUnicode_Concat */
binaryfunc unicode_concat_orig;                /* used for sq_concat method */
binaryfunc bytearray_cat_orig;
binaryfunc bytearray_icat_orig;

void str_cat_new(register PyObject **pv, register PyObject *w) {
    PyObject *orig_pv = *pv;
    Py_XINCREF(orig_pv);

    enter_propagation_scope();
    str_cat_orig(pv, w);
    exit_propagation_scope();

    if (*pv == NULL) {
        Py_XDECREF(orig_pv);
        return;
    }

    propagate_concat(orig_pv, w, *pv, "propagate_bytes_concat");

    Py_XDECREF(orig_pv);
}

PyObject *str_concat_new(register PyObject *a, register PyObject *b) {
    PyObject *result;

    enter_propagation_scope();
    result = str_concat_orig(a, b);
    exit_propagation_scope();

    if (result == NULL)
        return result;

    propagate_concat(a, b, result, "propagate_bytes_concat");

    return result;
}

PyObject *unicode_cat_new(PyObject *l, PyObject *r) {
    PyObject *result;

    enter_propagation_scope();
    result = unicode_cat_orig(l, r);
    exit_propagation_scope();

    if (result == NULL)
        return result;

    propagate_concat(l, r, result, "propagate_unicode_concat");

    return result;
}

PyObject *unicode_concat_new(PyObject *l, PyObject *r) {
    PyObject *result;

    enter_propagation_scope();
    result = unicode_concat_orig(l, r);
    exit_propagation_scope();

    if (result == NULL)
        return result;

    propagate_concat(l, r, result, "propagate_unicode_concat");

    return result;
}

PyObject *bytearray_cat_new(PyObject *l, PyObject *r) {
    PyObject *result;

    enter_propagation_scope();
    result = bytearray_cat_orig(l, r);
    exit_propagation_scope();

    if (result == NULL)
        return result;

    propagate_concat(l, r, result, "propagate_bytearray_concat");

    return result;
}

/* in-place concatenation */
PyObject *bytearray_icat_new(PyObject *self, PyObject *other) {
    PyObject *result;

    enter_propagation_scope();
    result = bytearray_icat_orig(self, other);
    exit_propagation_scope();

    if (result == NULL)
        return result;

    propagate_concat(self, other, result, "propagate_bytearray_concat");

    return result;
}

/* apply our patch */
int apply_cat_patch(funchook_t *funchook) {
    str_cat_orig = PyString_Concat;
    str_concat_orig = PyString_Type.tp_as_sequence->sq_concat;
    unicode_cat_orig = PyUnicode_Concat;
    unicode_concat_orig = PyUnicode_Concat;
    bytearray_cat_orig = PyByteArray_Type.tp_as_sequence->sq_concat;
    bytearray_icat_orig = PyByteArray_Type.tp_as_sequence->sq_inplace_concat;

    funchook_prep_wrapper(funchook, &str_cat_orig, str_cat_new);
    funchook_prep_wrapper(funchook, &str_concat_orig, str_concat_new);
    funchook_prep_wrapper(funchook, &bytearray_cat_orig, bytearray_cat_new);
    funchook_prep_wrapper(funchook, &bytearray_icat_orig, bytearray_icat_new);
    funchook_prep_wrapper(funchook, &unicode_concat_orig, unicode_concat_new);
    PyUnicode_Type.tp_as_sequence->sq_concat = unicode_cat_new;

    return 0;
}
