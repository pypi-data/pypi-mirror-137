#ifndef _LIBRARY_H_
#define _LIBRARY_H_

#include "match.h"
#include "options.h"

#include <vector>
#include <string>
using namespace std;

double calculateDistanceBetween(string extracted, string desired, string transitionsFilepath="", string allowedChars="");

vector<Match> findBestMatches(string extracted, Options* options, int N=1, string transitionsFilepath="", string allowedChars="");

vector<Match> findBestMatchesFromFile(string extracted, string optionsFile, string key, int N=1, string transitionsFilepath="", string allowedChars="");

#endif