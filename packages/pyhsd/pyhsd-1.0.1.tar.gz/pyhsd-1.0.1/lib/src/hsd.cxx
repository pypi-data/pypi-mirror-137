#include "transitions.h"

#include <vector>
#include <algorithm>

// We're implementing a modified version of the dynamic time warping algorithm which is originally use to match time-series patterns.
// https://www.youtube.com/watch?v=_K1OsqCicBY&ab
double calculateHSD(string extracted, string desired, TransitionMap* t)
{
    // Desired must be in lower cast
    for_each(desired.begin(), desired.end(), [](char &c) {
        c = ::tolower(c);
    });

    // Create a distance matrix with the first axis representing extracted string characters and the second representing desired/expected string characters.
    vector<vector<double>> M(extracted.size(), vector<double>(desired.size(), 0));

    // Construct the matrix like in the video listed above
    // e is the cursor position of the extracted string
    for (int e=0; e<extracted.size(); e++) {
        // d is the cursor position of the desired string
        for (int d=0; d<desired.size(); d++) {
            // Determine the transition distance between the characters
            string ec, dc;
            ec += extracted[e];
            dc += desired[d];
            // NOTE: I HATE C++'s string vs char issues...

            double distance = getTransitionDistance(ec, dc, t);

            // Determine the values of the surrounding cells (left, bottom, corner)
            double minDistance = -1;
            if (e > 0) minDistance = M[e-1][d];

            if (d > 0 && minDistance > -1 && M[e][d-1] < minDistance)
                minDistance = M[e][d-1];

            if (e > 0 && minDistance > -1 && d > 0 && M[e-1][d-1] < minDistance)
                minDistance = M[e-1][d-1];

            // Calculate the current cell value
            M[e][d] = distance + (minDistance > -1 ? minDistance : 0);
        }
    }

    // Find the best (almost like potential field actually!) path from the end to the beginning such that we go towards the lowest value
    int e = extracted.size() - 1;
    int d = desired.size() - 1;

    // We start with a score of the last cell (top-right corner), and keep track of any penalties
    double penalty = M[e][d];

    // Traverse down the matrix until we get to the origin (0,0)
    while (e > 0 || d > 0)
    {
        // Determine the values of the surrounding cells
        double left = e > 0 ? M[e-1][d] : -1;
        double down = d > 0 ? M[e][d-1] : -1;
        double corner = e > 0 && d > 0 ? M[e-1][d-1] : -1;

        // Move in the direction of the smallest value If not going diagonally, take a penalty
        // Go left?
        if (left > -1 && e > 0 && left < down && left < corner) {
            e--;
            penalty++;
        }

        // Go down?
        else if (down > -1 && d > 0 && down < left && down < corner) {
            d--;
            penalty++;
        }

        // Go to Diagon Alley? (down-left)
        else {
            // If we're at the edge of the matrix - unfortunately, we can't go diagonally. Take a hit for that
            if (e == 0 || d == 0) penalty++;

            // Go down until you hit the origin or an edge
            if (e > 0) e--;
            if (d > 0) d--;
        }
    }

    return penalty;
}