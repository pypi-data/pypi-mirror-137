from setuptools import find_packages, setup, Extension
import os
import glob



sources = glob.glob("factorizer/*.pyx")+glob.glob("factorizer/*.cpp")
if "factorizer.cpp" in sources:
    sources.remove("factorizer.cpp")
    
ext = Extension("factorizer", 
    sources = sources,
    language = "c++",
    extra_compile_args = ["-v", "-std=c++11", "-Wall"],
    extra_link_args = ["-std=c++11"]
)

with open("README.md", "r") as fp:
    long_description = fp.read()
with open("requirements.txt", "r") as fp:
    install_requires = fp.read().splitlines()

setup(
    name = "factorizer",
    version = "0.5.2",
    author = "Fulltea",
    author_email = "rikuta@furutan.com",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/FullteaOfEEIC/factorizer",
    packages = find_packages(),
    install_requires = install_requires,
    python_requires = '>=3.7',
    ext_modules = [ext]
)

if os.path.exists(os.path.join("factorizer", "factorizer.cpp")):
    os.remove(os.path.join("factorizer", "factorizer.cpp"))


