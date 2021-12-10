import pathlib
from setuptools import setup, find_packages


# The directory containing this file
HERE = pathlib.Path(__file__).parent


# The text of the README file
README = (HERE / "README.md").read_text()


CLASSIFIERS = ["Natural Language :: English",
               "Intended Audience :: Developers",
               "Intended Audience :: Science/Research",
               "Programming Language :: Python :: 3.7",
               "Programming Language :: Python :: 3.8",
               "Programming Language :: Python :: 3.9",
               "Programming Language :: Python :: 3.10",
               "Topic :: Utilities",
               "Topic :: Scientific/Engineering :: GIS",]


REQUIREMENTS = ["geojson==2.5.0",
                "requests==2.25.0",
                "typeguard==2.13.0",
                "shapely==1.8.0"]


TEST_REQUIREMENTS = ["pytest",
                     "requests-mock"]


setup(
    name="osdatahub",
    version="0.0.0",
    python_requires=">=3.7",
    description="osdatahub is Ordnance Survey's (OS) Python API wrapper, designed to make data from the OS Data Hub APIs readily accessible to developers.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/OrdnanceSurvey/osdatahub",
    author="OS Rapid Prototyping",
    author_email="rapidprototyping@os.uk",
    license="OGL",
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    extras_require={
        "dev": TEST_REQUIREMENTS
    },
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
)
