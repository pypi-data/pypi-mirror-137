#include <Python.h>

static PyObject *method_is_forbidden_keys(PyObject *self, PyObject *args) {

    PyObject *py_dict;
    PyObject *py_list;

    if(!PyArg_ParseTuple(args, "OO", &py_dict, &py_list)) {
        return NULL;
    }

    int list_len = PyList_Size(py_list);

    for (int i = 0; i < list_len; i++){
        if (PyDict_Contains(py_dict, PyList_GetItem(py_list, i)))
            return PyBool_FromLong(1);
    }

    return PyBool_FromLong(0);
}

static PyMethodDef forbidden_keysMethods[] = {
    {"is_forbidden_keys", method_is_forbidden_keys, METH_VARARGS, "Checks if any key in a dictionary is in a list of forbidden words"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef forbidden_keysmodule = {
    PyModuleDef_HEAD_INIT,
    "forbidden_keys",
    "Module for checking forbidden keys",
    -1,
    forbidden_keysMethods
};


PyMODINIT_FUNC PyInit_forbidden_keys(void) {
    return PyModule_Create(&forbidden_keysmodule);
}
