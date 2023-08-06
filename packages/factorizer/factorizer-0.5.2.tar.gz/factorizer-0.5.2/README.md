# factorizer

This is a simple factorization tool.

Here is the simplest example.

```usage.py
from factorizer import BruteForceFactorizer
divider = BruteForceFactorizer() 
divider.factorize(57) # Devide number in order, starting with 2, 3, 4, 5...
#>>>(3, 19)
```

# Install
## Requirements
 - boost
 
 if you are using apt, you can install with
 ```
 apt install libboost-dev
 ```

 ## Install
 You can just use pip to install
 ```
pip install factorizer
 ```
 
 # Usage
 ## Basic Usage

first, import package
 ```usage.py
 from factorizer import BruteForceFactorizer
 ```

 ```BruteForceFactorizer``` trys dividing given number with 2, 3, 4, 5...

All Methods in this package are listed below.

second, create a object
```usage.py
divider = BruteForceFactorizer()
```
then, call ```factorize()``` method to factorize a number.
```usage.py
divider.factorize(57)
#>>> (3, 19)
```
You will receive the tuple, whose length are 2 and the product of those are the given number.

That's all!!

## Setting Timeout
When you try to factorize some large numbers, what we care is whether the calculation ends in a short period. While we can't predict the required time, we provide time out method instead.

```no_timeout.py
from factorizer import BruteForceFactorizer
divider = BruteForceFactorizer()
divider.factorize(221) # This takes less than 1 second.
# >>> (13, 17) 
divider.factorize(144483604528043653279487) # This takes about 40 seconds in my environment.
# >>> (2147483647, 67280421310721)
```
Now you can set timeout for divider.

```timeout.py
from factorizer import BruteForceFactorizer
divider = BruteForceFactorizer(timeout=5)
divider.factorize(221)
# >>> (13, 17) 
divider.factorize(144483604528043653279487) # This raises timeout error after 5 seconds.
# >>> factorizer.TimeOutError
```

## Factorize Methods
SIP... Sorry!
### BruteForceFactorizer
### FermatFactorizer
### PollardsRhoFactorizer
### RSAPrivateKeyFactorizer
### FactorDBFactorizer