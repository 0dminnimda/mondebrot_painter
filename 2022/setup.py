import os
from glob import glob

import numpy as np
from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

from mandelbrot_painter import __name__, __version__

requirements = {}
for path in glob("requirements/*.txt"):
    with open(path) as file:
        name = os.path.basename(path)[:-4]
        requirements[name] = [line.strip() for line in file]

with open("README.md") as file:
    long_description = file.read()

github_link = "https://github.com/0dminnimda/mondebrot_painter"


extensions = [
    Extension(
        "*", ["mandelbrot_painter/*.pyx"],
        extra_compile_args=["-O3", "-ffast-math", "-march=native", "-fopenmp"],
    ),
]


setup(
    name=__name__,
    version=__version__,
    description="My Mandelbrot Set visualizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="0dminnimda",
    author_email="0dminnimda.contact@gmail.com",
    url=github_link,
    packages=find_packages(),
    license="MIT",
    install_requires=requirements.pop("basic"),
    python_requires="~=3.9",
    extras_require=requirements,
    package_data={__name__: ["py.typed"]},
    ext_modules=cythonize(
        extensions,
        language_level=3,
        # annotate=True,
    ),
    include_dirs=[np.get_include()],
)
