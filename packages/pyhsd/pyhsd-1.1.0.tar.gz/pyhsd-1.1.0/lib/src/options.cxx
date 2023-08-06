#include "options.h"

#include <fstream>
#include <sstream>

// Load options from file to a vector of strings for a given key
Options* loadOptions(string filepath, string key)
{
    Options* opts = new vector<string>();

    int col = 0; // Column with key in header

    // Load options CSV file
    fstream csv(filepath);
    if (!csv.is_open()) {
        throw runtime_error("Could not open transitions file.");
    }

    string line, cell;
    bool isHeader = true;

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

                // If header, and we matched with the key, then set column index and continue with the rest
                if (isHeader) {// If key is empty, use the first column
                    if (key == "") {
                        col = 0;
                        break;
                    }

                    else if (key.compare(cell) == 0) {
                        col = column;
                        break; // Stop with this row
                    }
                }

                // Save option if we're at the correct column (corresponding to the key)
                else if (column == col) {
                    // If empty, we're done!!
                    if (cell == "") {
                        return opts;
                    }
                    opts->push_back(cell);
                }

                column++; // Next column
            }

            else part += cell + ",";
        }
        isHeader = false;
    }

    return opts;
}