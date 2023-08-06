#include "transitions.h"
#include "data.cxx"

#include <vector>
#include <fstream>
#include <sstream>
#include <iostream>

using namespace std;

// Select only allowed characters from transition map
TransitionMap* filterAllowed(TransitionMap* transitions, string allowedChars="")
{
    // If allowedChars string is empty, then keep all
    if (allowedChars == "") return transitions;

    // Go through transition map and remove elements for desired characters that are not in the allowed characters list
    TransitionMap* filtered = new TransitionMap();
    for (const auto &d : *transitions) {
        // If the character exists in the allowed characters list, add to new map
        if (allowedChars.find(d.first) != string::npos)
            filtered->insert(d);
    }

    return filtered;
}

// Load transitions from file to a transition map object
TransitionMap* loadTransitions(string filepath, string allowedChars)
{
    bool loadDefault = false;

    // If a custom transitions CSV file isn't provided, return default transitions data
    if (filepath == "") {
        return filterAllowed(&tDefault, allowedChars);
    }

    // Else, load from CSV file and return
    TransitionMap* transitions = new TransitionMap();

    fstream csv(filepath);
    if (!csv.is_open()) {
#ifdef __SUPPRESS_WARNINGS__
        cerr << "Could not open transitions file: " + filepath << endl;
        cerr << "Using default transitions map." << endl;
#endif

        return filterAllowed(&tDefault, allowedChars);
    }

    string line, row, cell;

    // Load header (expected/desired characters)
    bool isHeader = true;
    vector<string> header;

    // Read each line (separator: \n or \r is default)
    while (getline(csv, line))
    {
        stringstream ss(line);
        bool isString = false;
        string part{""};

        // Read each column (separator: ,)
        int column = -1;
        while (getline(ss, cell, ','))
        {
            auto i = cell.find("\"");
            if (i < cell.length()) {
                isString = !isString;
                part += cell.substr(0,i);
                cell = cell.substr(i+1, cell.length());
            }

            if (!isString) {
                cell += part;
                part = ""; // Reset

                // First cell is a row header - save
                if (column < 0) {
                    row = cell;
                }

                // If header, create an entry in the transitions map
                else if (isHeader) {
                    header.push_back(cell);
                    transitions->insert({ cell, map<string, double>() });
                }

                // Add value (score if exists) to transition map
                else {
                    try {
                        string key = header.at(column);
                        double value = stod(cell);
                        if (value > 0) {
                            transitions->at(key).insert({ row, value });
                        }
                    }

                    // Don't need to do anything...
                    catch (...) { }
                }

                column++; // Next column
            }

            else part += cell + ",";
        }
        isHeader = false;
    }

    // Transpose - the transitions.csv file has a triangular section that's empty because it's just supposed to be transposed values mirrored by the diagonal.
    // Go through the transition map and set any missing transponsed values.
    for (const auto &d : *transitions) {
        for (const auto &e : d.second) {
            // Ensure e->d exists in map
            if (!transitions->count(e.first)) {
                transitions->insert({ e.first, map<string, double>() });
            }
            
            auto &E = transitions->at(e.first);
            if (!E.count(d.first)) {
                E.insert({ d.first, e.second });
            }
        }
    }

    // Generate C++ initializer list with transition data as needed so we can include it in the build for faster load
#ifdef __DATA__
    ofstream df("./src/data.cxx");
    df << "#include \"transitions.h\"" << endl;
    df << "TransitionMap tDefault {" << endl;

    bool d0 = true;
    for (const auto &d : *transitions) {
        if (!d0) df << ",\n";
        df << "\t{\"" << d.first << "\", {";
        bool e0 = true;
        for (const auto &e : d.second) {
            if (!e0) df << ", ";
            df << "{\"" << e.first << "\", " << e.second << "}";
            e0 = false;
        }
        df << "}}";
        d0 = false;
    }

    df << "};";

    df.close();
    cout << "Created compilable transitions data file." << endl;
#endif

    return filterAllowed(transitions, allowedChars);
}

// Calculate transition distance between two characters with a given map
double getTransitionDistance(string e, string d, TransitionMap* t)
{
    // If the desired character doesn't exist in the map, set max distance
    if (!t->count(d)) {
        return 1;
    }

    // If the extracted character doesn't exist in the sub-list, set max distance
    if (!t->at(d).count(e)) {
        return 1;
    }

    // Else, return the transition distance (1 - match score)
    return 1 - t->at(d).at(e);
}