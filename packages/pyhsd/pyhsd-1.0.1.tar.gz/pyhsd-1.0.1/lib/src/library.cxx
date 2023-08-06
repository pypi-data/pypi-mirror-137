#include "library.h"
#include "transitions.h"
#include "hsd.h"

#include <algorithm>

double calculateDistanceBetween(string extracted, string desired, string transitionsFilepath)
{
    // Load transitions file
    TransitionMap* transitions = loadTransitions(transitionsFilepath);

    return calculateHSD(extracted, desired, transitions);
}

vector<Match> findBestMatches(string extracted, Options* options, int N, string transitionsFilepath)
{
    // Load transitions file
    TransitionMap* transitions = loadTransitions(transitionsFilepath);

    // Calculate HSD for each option
    vector<Match> matches;
    for (string option : *options) {
        matches.push_back(Match{
            option,
            calculateHSD(extracted, option, transitions)
        });
    }
    // TODO - paralellize? since we can pretty easily anyway?

    // Sort by lowest string distance
    sort(matches.begin(), matches.end(), [](const Match &lhs, const Match &rhs) {
        return lhs.distance < rhs.distance;
    });

    // Pick N best matches
    return vector<Match>(matches.begin(), matches.begin()+N);
}