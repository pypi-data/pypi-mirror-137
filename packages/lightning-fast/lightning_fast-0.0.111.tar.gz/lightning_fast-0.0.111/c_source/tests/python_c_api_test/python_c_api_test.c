//
// Created by 徐秋实 on 2021/12/8.
//
#define PY_SSIZE_T_CLEAN

#include <Python.h>


static PyObject *
system_command(PyObject *self, PyObject *args)
{
  const char *command;
  int sts;

  if (!PyArg_ParseTuple(args, "s", &command))
    return NULL;
  sts = system(command);
  return PyLong_FromLong(sts);
}
static PyMethodDef PythonCApiTestMethods[] = {
    {"system",  system_command, METH_VARARGS,
          "Execute a shell command."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};
static struct PyModuleDef PythonCApiTestModule = {
    PyModuleDef_HEAD_INIT,
    "lightning_fast.c_tools.python_c_api_test",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    PythonCApiTestMethods
};
PyMODINIT_FUNC
PyInit_python_c_api_test(void)
{

  return PyModule_Create(&PythonCApiTestModule);
}