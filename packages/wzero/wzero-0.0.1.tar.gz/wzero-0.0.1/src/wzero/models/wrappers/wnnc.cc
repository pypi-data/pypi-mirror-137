#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include "wisard_bind.cc"
#include "bleaching_wisard_bind.cc"
#include "bloom_wisard_bind.cc"
#include "bleaching_bloom_wisard_bind.cc"
#include "regression_wisard_bind.cc"

namespace py = pybind11;

PYBIND11_MODULE(wnnc, m) {

    py::class_<BindWiSARD>(m, "CcWiSARD")
        .def(py::init<int, int, int, bool>())
        .def("train", (void (BindWiSARD::*)(py::array_t<bool>&, py::array_t<int>&)) &BindWiSARD::train)
        .def("predict", (py::array_t<int> (BindWiSARD::*)(py::array_t<bool>&)) &BindWiSARD::predict)
        .def("mental_images", (py::array_t<float> (BindWiSARD::*)(void)) &BindWiSARD::mental_images)
        .def("clear", (void (BindWiSARD::*)(void)) &BindWiSARD::clear)
        .def("get_size", (int (BindWiSARD::*)(void)) &BindWiSARD::get_size)
    ;

    py::class_<BindBleachingWiSARD>(m, "CcBleachingWiSARD")
        .def(py::init<int, int, int, bool>())
        .def("train", (void (BindBleachingWiSARD::*)(py::array_t<bool>&, py::array_t<int>&)) &BindBleachingWiSARD::train)
        .def("predict", (py::array_t<int> (BindBleachingWiSARD::*)(py::array_t<bool>&)) &BindBleachingWiSARD::predict)
        .def("predictb", (py::array_t<int> (BindBleachingWiSARD::*)(py::array_t<bool>&, int)) &BindBleachingWiSARD::predictb)
        .def("mental_images", (py::array_t<float> (BindBleachingWiSARD::*)(void)) &BindBleachingWiSARD::mental_images)
        .def("clear", (void (BindBleachingWiSARD::*)(void)) &BindBleachingWiSARD::clear)
        .def("get_size", (int (BindBleachingWiSARD::*)(void)) &BindBleachingWiSARD::get_size)
    ;

    py::class_<BindBloomWiSARD>(m, "CcBloomWiSARD")
        .def(py::init<int, int, int, int, int, bool>())
        .def("train", (void (BindBloomWiSARD::*)(py::array_t<bool>&, py::array_t<int>&)) &BindBloomWiSARD::train)
        .def("predict", (py::array_t<int> (BindBloomWiSARD::*)(py::array_t<bool>&)) &BindBloomWiSARD::predict)
        .def("mental_images", (py::array_t<float> (BindBloomWiSARD::*)(void)) &BindBloomWiSARD::mental_images)
        .def("clear", (void (BindBloomWiSARD::*)(void)) &BindBloomWiSARD::clear)
        .def("get_size", (int (BindBloomWiSARD::*)(void)) &BindBloomWiSARD::get_size)
    ;

    py::class_<BindBleachingBloomWiSARD>(m, "CcBleachingBloomWiSARD")
        .def(py::init<int, int, int, int, int, bool>())
        .def("train", (void (BindBleachingBloomWiSARD::*)(py::array_t<bool>&, py::array_t<int>&)) &BindBleachingBloomWiSARD::train)
        .def("predict", (py::array_t<int> (BindBleachingBloomWiSARD::*)(py::array_t<bool>&)) &BindBleachingBloomWiSARD::predict)
        .def("predictb", (py::array_t<int> (BindBleachingBloomWiSARD::*)(py::array_t<bool>&, int)) &BindBleachingBloomWiSARD::predictb)
        .def("mental_images", (py::array_t<float> (BindBleachingBloomWiSARD::*)(void)) &BindBleachingBloomWiSARD::mental_images)
        .def("clear", (void (BindBleachingBloomWiSARD::*)(void)) &BindBleachingBloomWiSARD::clear)
        .def("get_size", (int (BindBleachingBloomWiSARD::*)(void)) &BindBleachingBloomWiSARD::get_size)
    ;

    py::class_<BindRegressionWiSARD>(m, "CcRegressionWiSARD")
        .def(py::init<int, int, int, bool>())
        .def("train", (void (BindRegressionWiSARD::*)(py::array_t<bool>&, py::array_t<float>&)) &BindRegressionWiSARD::train)
        .def("predict", (py::array_t<int> (BindRegressionWiSARD::*)(py::array_t<bool>&)) &BindRegressionWiSARD::predict)
        .def("mental_images", (py::array_t<float> (BindRegressionWiSARD::*)(void)) &BindRegressionWiSARD::mental_images)
        .def("clear", (void (BindRegressionWiSARD::*)(void)) &BindRegressionWiSARD::clear)
        .def("get_size", (int (BindRegressionWiSARD::*)(void)) &BindRegressionWiSARD::get_size)    ;
  
};