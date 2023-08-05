/*
 * Copyright © 2022 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/patches.h>
#include <contrast/assess/scope.h>
#include <contrast/assess/threadlocal_storage.h>

/* This function is used for building a map between str and unicode objects and
 * their underlying char * buffers. This enables us to do a reverse lookup
 * based on char * pointers from the hooked exec statement.
 */
static PyObject *get_str_pointer(PyObject *self, PyObject *str) {
    unsigned long ptr_val;

    if (!PyString_Check(str))
        Py_RETURN_NONE;

    /* Get the pointer to the underlying string as an integer value */
    ptr_val = (unsigned long)PyString_AS_STRING(str);
    return PyLong_FromUnsignedLong(ptr_val);
}

static PyMethodDef methods[] = {
    {"initialize",
     (PyCFunction)initialize,
     METH_VARARGS | METH_KEYWORDS,
     "Initialize C extension patcher"},
    {"enable_required_hooks",
     enable_required_hooks,
     METH_O,
     "Hook relevant non-method functions"},
    {"create_unicode_hook_module",
     create_unicode_hook_module,
     METH_NOARGS,
     "Create table of unicode method hook functions"},
    {"create_bytes_hook_module",
     create_bytes_hook_module,
     METH_NOARGS,
     "Create table of bytes method hook functions"},
    {"create_bytearray_hook_module",
     create_bytearray_hook_module,
     METH_NOARGS,
     "Create table of bytearray method hook functions"},
    {"install", install, METH_O, "Install string hooks"},
    {"disable", disable, METH_O, "Remove all hooks"},
    {"set_exact_scope",
     set_exact_scope,
     METH_O,
     "Sets the scope in the thread exactly what you pass to it"},
    {"enter_scope", enter_scope, METH_VARARGS, "Enter given scope"},
    {"exit_scope", exit_scope, METH_VARARGS, "Exit given scope"},
    {"in_scope", in_scope, METH_VARARGS, "Check whether in given scope"},
    {"in_contrast_or_propagation_scope",
     in_contrast_or_propagation_scope,
     METH_NOARGS,
     "Check in propagation (or contrast) scope"},
    /* TODO: PYT-1745 create_thread_storage will need different flags */
    {"create_thread_storage",
     create_thread_storage,
     METH_O,
     "Create thread storage with initial scope and context"},
    {"destroy_thread_storage",
     destroy_thread_storage,
     METH_NOARGS,
     "Teardown storage for thread"},
    {"get_thread_scope", get_thread_scope, METH_NOARGS, "Get scope level for thread"},
    {"set_attr_on_type", set_attr_on_type, METH_VARARGS, "Set attribute on type"},
    {"get_str_pointer", get_str_pointer, METH_O, "Get pointer to underlying string"},
};

PyMODINIT_FUNC initcs_str(void) {
    PyObject *module = Py_InitModule("cs_str", methods);

/*  This will always be false on Python <= 3.6. Added this here to make code maintenance
    slightly easier
*/
#ifdef USE_CONTEXTVARS
    PyModule_AddIntConstant(module, "USE_CONTEXTVARS", 1);
#else
    PyModule_AddIntConstant(module, "USE_CONTEXTVARS", 0);
#endif

    PyModule_AddIntConstant(module, "CONTRAST_SCOPE", CONTRAST_SCOPE);
    PyModule_AddIntConstant(module, "PROPAGATION_SCOPE", PROPAGATION_SCOPE);
    PyModule_AddIntConstant(module, "TRIGGER_SCOPE", TRIGGER_SCOPE);
}
