/*
 * Copyright © 2022 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <pthread.h>

#include <contrast/assess/logging.h>
#include <contrast/assess/scope.h>

#ifndef USE_CONTEXTVARS

#include <contrast/assess/threadlocal_storage.h>

static pthread_key_t thread_key;
static pthread_once_t once_key = PTHREAD_ONCE_INIT;

static inline void init_thread_key(void) {
    (void)pthread_key_create(&thread_key, NULL);
}

/*
 * Create and initialize thread storage for the current thread.
 * If it already exists, returns it immediately.
 * Returns the newly created or retrieved thread storage object or NULL on
 * failure.
 */
static thread_storage_t *init_thread_storage(
    const thread_scope_t *initial_scope, PyObject *initial_context) {
    thread_storage_t *storage;

    pthread_once(&once_key, init_thread_key);

    /* Thread storage has already been initialized, so do nothing */
    if ((storage = pthread_getspecific(thread_key)) != NULL) {
        return storage;
    }

    if ((storage = malloc(sizeof(*storage))) == NULL) {
        log_error("Failed to allocate storage for thread");
        return NULL;
    }

    if (!init_thread_scope(&(storage->scope), initial_scope)) {
        log_error("Failed to initialize thread scope");
        free(storage);
        return NULL;
    }

    pthread_setspecific(thread_key, storage);

    return storage;
}

/*
 * Gets the thread storage object associated with the current thread. If none
 * exists, creates one with default values. Returns NULL on failure.
 */
thread_storage_t *get_thread_storage() {
    static const thread_scope_t zero_scope; /* implicitly initialized to 0s */

    /* If storage is not initialized for this thread at the time this is called,
       it indicates that we are in a thread that existed before we added
       instrumentation. This means that there was no storage, so we just
       initialize with zeroes.
    */
    return init_thread_storage(&zero_scope, NULL);
}

PyObject *create_thread_storage(PyObject *self, PyObject *initial_scope) {
    thread_scope_t scope;

    /* TODO: PYT-1745 this may need to parse "iiiO" with the final arg being a
       RequestContext to be sent to init_thread_storage (instead of NULL)
    */
    if (!PyArg_ParseTuple(
            initial_scope,
            "iii",
            &scope.contrast_scope,
            &scope.propagation_scope,
            &scope.trigger_scope)) {
        PyErr_Format(PyExc_RuntimeError, "Failed to parse storage args from tuple");
        return NULL;
    }

    init_thread_storage(&scope, NULL);

    Py_RETURN_NONE;
}

PyObject *destroy_thread_storage(PyObject *self, PyObject *ignored) {
    thread_storage_t *storage;

    log_debug("destroy thread storage");

    storage = pthread_getspecific(thread_key);
    if (storage != NULL) {
        pthread_setspecific(thread_key, NULL);
        destroy_scope(storage->scope);
        free(storage);
    }

    Py_RETURN_NONE;
}
#endif
