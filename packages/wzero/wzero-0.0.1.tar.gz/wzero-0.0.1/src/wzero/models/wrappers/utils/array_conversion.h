#ifndef ARRAY_CONVERSION_H
#define ARRAY_CONVERSION_H

#include "../../cc/utils/array.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
namespace py = pybind11;

template <class T>
Array1D<T> to_array_1d(py::array_t<T>& arr) {
    py::buffer_info buf = arr.request();
    return Array1D<T>((T*)buf.ptr, buf.shape[0]);
};

template <class T>
Array2D<T> to_array_2d(py::array_t<T>& arr) {
    py::buffer_info buf = arr.request();
    return Array2D<T>((T*)buf.ptr, buf.shape[0], buf.shape[1]);
};

template <class T1, class T2>
py::array_t<T2> to_np_array(Array2D<T1>& arr) {
    ssize_t ndim = 2;
    std::vector<ssize_t> shape = {arr.shape[0], arr.shape[1]};
    std::vector<ssize_t> strides = {sizeof(T1)*arr.shape[1], sizeof(T1)};
    return py::array_t<T2>(py::buffer_info(
        arr.data,
        sizeof(T2),
        py::format_descriptor<T2>::format(),
        ndim,
        shape,
        strides
    ));
}

#endif