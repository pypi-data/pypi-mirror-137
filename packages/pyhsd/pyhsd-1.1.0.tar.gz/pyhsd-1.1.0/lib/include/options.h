#ifndef _OPTIONS_H_
#define _OPTIONS_H_

#include <string>
#include <vector>

using namespace std;

typedef vector<string> Options;

Options* loadOptions(string filepath, string key="");

#endif