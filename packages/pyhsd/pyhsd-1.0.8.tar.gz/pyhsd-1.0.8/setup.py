from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
import pathlib

ext_modules = [
    Pybind11Extension(
        "pyhsd",
        [
            "binding.cpp", 
            
            # C++ Source files
            "lib/src/transitions.cxx",
            "lib/src/hsd.cxx",
            "lib/src/options.cxx",
            "lib/src/library.cxx"
        ],
        include_dirs=['lib/include'],
        extra_compile_args=['-O3', '-fopenmp'],
        define_macros=[('__SUPPRESS_WARNINGS__', '')]
    )
]

setup(
    name="pyhsd",
    version="1.0.8",
    author="Inventives.ai <https://inventives.ai>",
    author_email="narendran.m@inventives.ai",
    url="https://bitbucket.org/pinetree-ai/algorithm-humanized-string-distance/src/master/",
    description="Humanized String Distance calculator",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    license="CC-BY-NC 4.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering"
    ],
    install_requires=['setuptools', 'wheel', 'pybind11'],
    include_package_data=True,
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext}
)