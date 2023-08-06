#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "library.h"
#include <string>

using namespace std;
namespace py = pybind11;

PYBIND11_MODULE(pyhsd, m) {
    m.doc() = R""""(
        pyhsd.distance(extracted, desired, transitions="", allowed="")
        pyhsd.match(extracted, options, numResults=1, transitions="", allowed="")
        pyhsd.matchf(extracted, filepath, key, numResults=1, transitions="", allowed="")
    )"""";

    py::class_<Match>(m, "Match")
        .def(py::init<const string &>())
        .def_readwrite("value", &Match::value)
        .def_readwrite("distance", &Match::distance)
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
        py::arg("allowedChars") = "",
        R""""(
Calculate the HSD string distance between two strings.

Parameters
----------
@param extracted [str] - extracted (handwritten) string
@param desired [str] - desired/expected string to match against
@param transitions [str] - file path to custom transitions Csv file
@param allowed [str] - string of characters allowed in result

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
        py::arg("allowedChars") = "",
        R""""(
Find best matches for extracted string from a list of options.

Parameters
----------
@param extracted [str] - extracted (handwritten) string
@param options [List.str] - list of possible options to match against
@param numResults [int] - number of results to return
@param transitions [str] - file path to custom transitions CSV file
@param allowed [str] - string of characters allowed in result

Returns
-------
@out matches [List.Match] - matches with distances
        )""""
    );

    m.def(
        "matchf",
        &findBestMatchesFromFile,
        py::arg("extracted"),
        py::arg("filepath"),
        py::arg("key"),
        py::arg("N") = 1,
        py::arg("transitionsFilepath") = "",
        py::arg("allowedChars") = "",
        R""""(
Find best matches for extracted string from a list of options provided in a CSV file. The options file may have multiple lists with the header representing the key.

Parameters
----------
@param extracted [str] - extracted (handwritten) string
@param filepath [str] - file path to options CSV file
@param key [str] - column header for list in options file
@param numResults [int] - number of results to return
@param transitions [str] - file path to custom transitions CSV file
@param allowed [str] - string of characters allowed in result

Returns
-------
@out matches [List.Match] - matches with distances
        )""""
    );
}