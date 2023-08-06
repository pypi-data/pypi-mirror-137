//
// Created by 徐秋实 on 2021/12/9.
//
#include "pybind11/pybind11.h"
#include "pybind11/stl.h"
#include "pybind11/stl_bind.h"
#include "../interface/label_encoder.h"

PYBIND11_MAKE_OPAQUE(std::vector<std::string>)
namespace py = pybind11;

PYBIND11_MODULE(encoders , m ){
  m.doc() = "fast encoder labels";

  py::bind_vector<std::vector<std::string>> (m, "OneDStringVector");

  pybind11::class_<encoders::LabelEncoder>(m, "LabelEncoder" )
      .def(pybind11::init())
      .def_readonly("label_map", &encoders::LabelEncoder::encoder_map)
      .def("encode_1d", &encoders::LabelEncoder::encode1D)
      .def("transform_1d", &encoders::LabelEncoder::transform1D);
}