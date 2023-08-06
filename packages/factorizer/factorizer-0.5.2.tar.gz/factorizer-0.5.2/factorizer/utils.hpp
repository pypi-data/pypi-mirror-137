#include <iostream>
#include <boost/multiprecision/cpp_int.hpp>
using Bint = boost::multiprecision::cpp_int;

Bint isqrt(Bint n);

unsigned long ilog(Bint n);

Bint euclidean_gcd(Bint a, Bint b);
