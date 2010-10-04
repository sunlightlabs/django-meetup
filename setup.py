from distutils.core import setup
from meetup import __version__

readme = open('README.rst').read()

setup(
    name="django-meetup",
    version=__version__,
    py_modules=["meetup"],
    description="A very basic client for creating a local cache of Meetup.com/everywhere events.",
    author="Jeremy Carbaugh",
    author_email = "jcarbaugh@sunlightfoundation.com",
    license='BSD',
    long_description=readme,
    platforms=["any"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)