#include "mapping.h"
#include "utils.h"

#include <algorithm>
#include <random>
#include <chrono>

using namespace std;
using namespace chrono;

int** complete_mapping(int inp_size, int n_bits) {
    int* mapp = range(0, inp_size);
    int seed = system_clock::now().time_since_epoch().count();
    shuffle(mapp, mapp + inp_size, default_random_engine(seed)); 
    int** mapping = slice(mapp, inp_size, n_bits);
    delete [] mapp;
    return mapping;
};

int* random_mapping(int inp_size, int n_bits) {
    int* arange = range(0, inp_size);
    int* choice = random_choice(arange, inp_size, n_bits);
    delete []  arange;
    return choice;

};