#include <iostream>
#include <boost/multiprecision/cpp_int.hpp>
#include "utils.hpp"
using namespace std;
using Bint = boost::multiprecision::cpp_int;


string FermatFactorizer_cppfunc(string s){
    Bint n(s);
    Bint x = isqrt(n)+1;
    Bint y = isqrt(pow(x,2)-n);
    Bint w = pow(x,2)-n-pow(y,2);
    for(;;){
        if(w==0){
            Bint retval = x-y;
            return retval.str();
        }
        else if(w>0){
            y+=1;
        }
        else{
            x+=1;
        }
        w = pow(x,2)-n-pow(y,2);
    }
}
