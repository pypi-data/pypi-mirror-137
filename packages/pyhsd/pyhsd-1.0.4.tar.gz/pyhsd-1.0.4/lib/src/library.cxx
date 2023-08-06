#include "library.h"
#include "options.h"
#include "transitions.h"
#include "hsd.h"
#include <omp.h>

#include <algorithm>

double calculateDistanceBetween(string extracted, string desired, string transitionsFilepath, string allowedChars)
{
    // Load transitions file
    TransitionMap* transitions = loadTransitions(transitionsFilepath, allowedChars);

    return calculateHSD(extracted, desired, transitions);
}

vector<Match> findBestMatches(string extracted, Options* options, int N, string transitionsFilepath, string allowedChars)
{
    // Load transitions file
    TransitionMap* transitions = loadTransitions(transitionsFilepath, allowedChars);

    // Calculate HSD for each option
    vector<Match> matches(options->size());

    #pragma omp parallel for
    for (int i=0; i<options->size(); i++) {
        string option = options->at(i);
        matches[i] = Match{
            option,
            calculateHSD(extracted, option, transitions)
        };
    }

    // Sort by lowest string distance
    sort(matches.begin(), matches.end(), [](const Match &lhs, const Match &rhs) {
        return lhs.distance < rhs.distance;
    });

    // Pick N best matches
    return vector<Match>(matches.begin(), matches.begin()+N);
}

vector<Match> findBestMatchesFromFile(string extracted, string optionsFile, string key, int N, string transitionsFilepath, string allowedChars)
{
    // Load options
    Options* options = loadOptions(optionsFile, key);

    return findBestMatches(extracted, options, N, transitionsFilepath, allowedChars);
}