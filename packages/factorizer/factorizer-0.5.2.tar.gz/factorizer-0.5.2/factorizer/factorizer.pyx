import cython
from libcpp.string cimport string
import signal
import timeout_decorator
import requests
from requests.exceptions import Timeout


class TimeOutError(Exception):
    pass


class BaseClass:

    def __init__(self, timeout=None):
        self.DETERMINISTIC = None
        self.timeout = timeout
        
    def factorize(self, n, *args, **kwargs):
        assert self.DETERMINISTIC is not None
        if self.timeout:
            _factorize = timeout_decorator.timeout(self.timeout, use_signals=False, timeout_exception=TimeOutError)(self._factorize)
        else:
            _factorize = self._factorize
        d = _factorize(n=str(n).encode(), args=args, kwargs=kwargs)
        d = int(d.decode())
        assert d*(n//d) == n
        return (d, n//d)
    
    def _factorize(self, n, *args, **kwargs):
        pass


class BruteForceFactorizer(BaseClass):

    def __init__(self, timeout=None):
        super().__init__(timeout)
        self.DETERMINISTIC = True

    def _factorize(self, n, *args, **kwargs):
        cdef:
            string d
        d = BruteForceFactorizer_cppfunc(n)
        return d


class FermatFactorizer(BaseClass):

    def __init__(self, timeout=None):
        super().__init__(timeout)
        self.DETERMINISTIC = True

    def _factorize(self, n, *args, **kwargs):
        cdef:
            string d
        
        d = FermatFactorizer_cppfunc(n)
        return d


class PollardsRhoFactorizer(BaseClass):

    def __init__(self, c=1, timeout=None):
        super().__init__(timeout)
        self.DETERMINISTIC = False
        self.c = c

    def _factorize(self, n, *args, **kwargs):
        cdef:
            string d
        
        d = PollardsRhoFactorizer_cppfunc(n, self.c)
        return d


class RSAPrivateKeyFactorizer(BaseClass):

    def __init__(self, timeout=None):
        super().__init__(timeout)
        self.DETERMINISTIC = False

    def factorize(self, n, d, e=65537, *args, **kwargs):
        kwargs["d"] = d
        kwargs["e"] = e
        return super().factorize(n=n, args=args, kwargs=kwargs["kwargs"])

    def _factorize(self, n, *args, **kwargs):
        d = kwargs["kwargs"]["d"]
        e = kwargs["kwargs"]["e"]
        d = str(d).encode()
        e = str(e).encode()
        cdef:
            string p
        p = RSAPrivateKeyFactorizer_cppfunc(n, d, e)
        return p



class FactorDBFactorizer(BaseClass):
    
    def __init__(self, timeout=None):
        super().__init__(timeout)
        self.DETERMINISTIC = False
        self.ENDPOINT = "http://factordb.com/api"

    
    def _factorize(self, n):
        payload = {"query": n}
        
        try:
            r = requests.get(self.ENDPOINT, params=payload, timeout=self.timeout)
        except Timeout:
            raise TimeOutError
        except Exception as e:
            raise e
        return r.json()

    def factorize(self, n, raw_result=False):
        result = self._factorize(n)["factors"]
        if raw_result:
            return result
        
        if len(result)==1 and result[0][1]==1:
            return (1,n)
        else:
            d = int(result[0][0])
            assert d*(n//d) == n
            return (d, n//d)
        
        

        



