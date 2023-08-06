// stdafx.h : include file for standard system include files,
//  or project specific include files that are used frequently, but
//      are changed infrequently
//
#pragma once

//#include <omp.h>
#include <float.h>
#include <sys/timeb.h>

#include <iomanip>
#include <vector>
#include <map>
#include <stack>
#include <set>
#include <list>
#include <queue>
#include <limits>
#include <cassert>
#include <fstream>
#include <sstream>
#include <iostream>
#include <string>
#define _USE_MATH_DEFINES
#include <math.h>

constexpr double LENGTH_EPSILON_CONTROL = 1e-9;
constexpr double RateOfNormalShift = 5e-3;
constexpr double ToleranceOfConvexAngle = 5e-2;
