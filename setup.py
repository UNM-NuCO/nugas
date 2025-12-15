import setuptools
import sys
import os

try:
    import sysconfig
    from pybind11.setup_helpers import Pybind11Extension, build_ext

    # List of C++ extension modules
    ext_modules = [
        Pybind11Extension(
            "nugas.misc.pdz_c",
            ["src/nugas/misc/pdz_c.cpp"],
        ),
        Pybind11Extension(
            "nugas.f2e0d1a.eom_c",
            ["src/nugas/f2e0d1a/eom_c.cpp"],
        ),
        Pybind11Extension(
            "nugas.f2e0d1a.lax42",
            ["src/nugas/f2e0d1a/lax42.cpp"],
        ),
    ]

    # Additional compiler flags depending on the platform/compiler
    if sys.platform.startswith("darwin"):  # MacOS, assuming clang
        extra_compile_args = ['-Xpreprocessor', '-fopenmp']
        extra_link_args = []



    elif 'CXX' in os.environ and 'icpc' in os.environ['CXX']:
        extra_compile_args = ['-xHost', '-qopenmp']
        extra_link_args = ['-qopenmp']
    else:  # assuming g++
        extra_compile_args = ['-fopenmp']
        extra_link_args = ['-lgomp']

    # Add conda include path if available
    if "CONDA_PREFIX" in os.environ:
        extra_compile_args.append(f'-I{os.environ["CONDA_PREFIX"]}/include')

    # Add Python include path
    extra_compile_args.append(f'-I{sysconfig.get_paths()["include"]}')

    # Apply flags to all extensions
    for ext in ext_modules:
        ext.extra_compile_args = extra_compile_args
        ext.extra_link_args = extra_link_args

    setuptools.setup(
        ext_modules=ext_modules,
        cmdclass={"build_ext": build_ext},
    )

except Exception as e:
    # Fall back to pure Python installation if C++ compilation fails
    print("** FAILED TO BUILD THE C++ EXTENSIONS. INSTALLED THE PURE PYTHON PACKAGE INSTEAD. **", file=sys.stderr)
    print(f"** Error: {e} **", file=sys.stderr)
    setuptools.setup()
