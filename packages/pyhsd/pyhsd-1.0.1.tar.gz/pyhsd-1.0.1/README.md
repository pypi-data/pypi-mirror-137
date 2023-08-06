# Humanized String Distance Algorithm

This project is created and maintained by [Inventives, Inc.](https://inventives.ai), and is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/legalcode).

## About

The *Humanized String Distance* (HSD) algorithm is based on a modified dynamic-time-warping solution to compare two strings. The HSD algorithm accounts for closeness of characters based on handwritten and/or extracted (OCR) text. For example, the **i** character looks similar to **j** and handwriting recognition systems may easily mistake them for each other based on the writing style. Handwritten or extracted characters like **B** and **8** are easily confused, similar to **S** and **5**, **.** and **,** and many more. The HSD algorithm is a lot more tolerant of these and improves the performance of string distance calculation to match extracted text to a known set of values.

The HSD algorithm takes in the extracted text, and expected/desired text as arguments, and provides a modified string distance score.

The expected/desired string may include lower case alphabets, numbers, and various special characters including:
 - Space ( )
 - Period (.)
 - Comma (,)
 - Hyphen (-)

## Installation

Install from the `pip` package manager.
```
pip install pyhsd
```

Or, install from source.
```
pip install setuptools pybind11 wheel
pip install -e .
```

## Usage

```
import pyhsd
```

### Calculate HSD distance between two strings

```
d = pyhsd.distance('he110', 'hello')
```

### Find closest match from a list of options

```
numMatches = 1
matches = pyhsd.match('he110', [ 'hello', 'world' ], numMatches)
```

Each match is an instance of the `Match` class which contains properties `value` representing the string it matched, and `distance` with the HSD distance for the match.

### Custom transitions file

To match with custom transitions, you may pass a CSV file whch maps possible extracted characters (rows) to desired characters (columns). The corresponded cell for each row-column represents a score on the scale 0 to 1 representing how similar the characters are. For instance, **q** and **v** are rarely confused, so they have a low score (0), but **b** and **h** may be confused easily, giving them a higher score (0.3). If the row and column characters are the same, then the cell value will be 1 representing an exact match.