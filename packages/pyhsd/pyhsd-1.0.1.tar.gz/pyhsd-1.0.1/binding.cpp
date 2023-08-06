#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "library.h"
#include <string>

using namespace std;
namespace py = pybind11;

PYBIND11_MODULE(pyhsd, m) {
    m.doc() = R""""(
        hsd.distance(extracted, desired, transitions)
        hsd.match(extracted, options, numResults, transitions)
    )"""";

    py::class_<Match>(m, "Match")
        .def(py::init<const string &>())
        .def("__repr__", [](const Match &a) {
            return "<pyhsd.Match object for '" + a.value + "'>";
        })
        .def("__str__", [](const Match &a) {
            return "{ value: \"" + a.value + "\", distance: \"" + to_string(a.distance) + "\" }";
        });

    m.def(
        "distance",
        &calculateDistanceBetween,
        py::arg("extracted"),
        py::arg("desired"),
        py::arg("transitionsFilepath") = "",
        R""""(
Calculate the HSD string distance between two strings.

Parameters
----------
@param extracted [str] - extracted (handwritten) string
@param desired [str] - desired/expected string to match against
@param transitions [str] - file path to custom transitions Csv file

Returns
-------
@out distance [double] - HSD between input strings
        )""""
    );

    m.def(
        "match",
        &findBestMatches,
        py::arg("extracted"),
        py::arg("options"),
        py::arg("N") = 1,
        py::arg("transitionsFilepath") = "",
        R""""(
Find best matches for extracted string from a list of options.

Parameters
----------
@param extracted [str] - extracted (handwritten) string
@param options [List(str)] - list of possible options to match against
@param numResults [int] - number of results to return
@param transitions [str] - file path to custom transitions Csv file

Returns
-------
@out matches [List(Dict{ value [str], distance [double] })] - matches with distances
        )""""
    );
}