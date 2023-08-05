/*
 * Copyright © 2022 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */

#ifndef _ASSESS_THREADLOCAL_STORAGE_H_
#define _ASSESS_THREADLOCAL_STORAGE_H_
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/scope.h>

#ifndef USE_CONTEXTVARS

/* Everything we need stored per-thread. Rather than try to use or implement
 *generic thread-local storage, we include exactly all the data we need here for
 *efficiency.
 **/
typedef struct thread_storage {
    thread_scope_t *scope;
} thread_storage_t;

PyObject *create_thread_storage(PyObject *, PyObject *);
PyObject *destroy_thread_storage(PyObject *, PyObject *);

thread_storage_t *get_thread_storage(void);

#endif /* use contextvars */

#endif /* _ASSESS_THREADLOCAL_STORAGE_H_ */
