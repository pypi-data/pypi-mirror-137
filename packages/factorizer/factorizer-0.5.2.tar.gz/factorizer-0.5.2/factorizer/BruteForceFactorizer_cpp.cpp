#include <iostream>
#include <boost/multiprecision/cpp_int.hpp>
#include "utils.hpp"
using namespace std;
using Bint = boost::multiprecision::cpp_int;

string BruteForceFactorizer_cppfunc(string s){
    Bint n(s);
    Bint sqrt_n = isqrt(n);
    for(Bint i=2;i<=sqrt_n;i++){
        if(n%i==0){
            return i.str();
        }
    }
    return "1";
}
