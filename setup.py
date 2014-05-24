from setuptools import setup, find_packages


TEST_DIRS = ["*.tests", "*.tests.*", "tests.*", "tests"]

setup(
    name = "SimpleFSM",
    description = "A simple package that allows you model arbitrary automatons.", 
    version = "0.1",
    packages = find_packages(exclude=TEST_DIRS),
    author = "Lucas Liendo",
    author_email = "mindmaster@gmail.com",
    keywords = "automaton finite state machine",
    install_requires = ["nose >= 1.3.2"], 
    test_suite = "nose.collector",
)
