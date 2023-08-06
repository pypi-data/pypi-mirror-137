#include <iostream>
#include <boost/multiprecision/cpp_int.hpp>
#include <boost/random.hpp>
#include <cmath>
#include "utils.hpp"
using namespace std;
using Bint = boost::multiprecision::cpp_int;

string RSAPrivateKeyFactorizer_cppfunc(string s, string d_, string e_){
    Bint n(s);
    Bint d(d_);
    Bint e(e_);
    Bint t = e*d-1;
    Bint u = 0;
    using engine = boost::random::independent_bits_engine<boost::mt19937, 16384, Bint>;
    engine gen;
    while(true){
        Bint quotient = t/2;
        Bint remainder = t%2;
        if(remainder!=0){break;}
        u += 1;
        t = quotient;
    }
    bool found = false;
    Bint c1, c2;
    while(!found){
        Bint i("1");
        Bint a = (gen()+1)%n;
        while(i<=u and !found){
            Bint c1_ = powm(Bint("2"),i-1,n);
            c1 = powm(a,c1_*t,n);
            Bint c2_ = powm(Bint("2"),i,n);
            c2 = powm(a,c2_*t,n);
            found = (c1!=1) and (c1!=-1%n) and (c2==1);
            i+=1;
        }
    }
    Bint retval =  gcd(c1-1, n);
    return retval.str();
    
}
