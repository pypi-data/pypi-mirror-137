#ifndef _HSD_H_
#define _HSD_H_

#include "transitions.h"

#include <string>

using namespace std;

double calculateHSD(string extracted, string desired, TransitionMap* t);

#endif