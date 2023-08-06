from libcpp.string cimport string

cdef extern from "BruteForceFactorizer_cpp.hpp":
    string BruteForceFactorizer_cppfunc(string s)

cdef extern from "FermatFactorizer_cpp.hpp":
    string FermatFactorizer_cppfunc(string s)

cdef extern from "PollardsRhoFactorizer_cpp.hpp":
    string PollardsRhoFactorizer_cppfunc(string s, long c)

cdef extern from "RSAPrivateKeyFactorizer_cpp.hpp":
    string RSAPrivateKeyFactorizer_cppfunc(string s, string d, string e)