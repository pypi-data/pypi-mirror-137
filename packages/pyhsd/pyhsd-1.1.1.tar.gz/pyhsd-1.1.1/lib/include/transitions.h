#ifndef _TRANSITIONS_H_
#define _TRANSITIONS_H_

#include <map>
#include <string>

using namespace std;

typedef map<string, map<string, double>> TransitionMap;

TransitionMap* loadTransitions(string filepath="", string allowedChars="");
double getTransitionDistance(string e, string d, TransitionMap* t);

#endif