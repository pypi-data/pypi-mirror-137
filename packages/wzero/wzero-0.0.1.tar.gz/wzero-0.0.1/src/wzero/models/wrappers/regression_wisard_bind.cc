#include "../cc/regression_wisard.cc"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
namespace py = pybind11;

class BindRegressionWiSARD : public BindBase<RegressionWiSARD, float> {
public:

    BindRegressionWiSARD(int input_lenght, int tuple_lenght, int num_classes, bool canonical)
    : BindBase(input_lenght, tuple_lenght, num_classes, canonical) {};

    void train(py::array_t<bool>& input_array, py::array_t<float>& classes_array) {
        Array2D<bool> input = to_array_2d<bool>(input_array);
        Array2D<float> classes = to_array_2d<float>(classes_array);
        RegressionWiSARD::train(input, classes);
    };

};