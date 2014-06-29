from setuptools import setup

setup(
    name="SimpleFSM",
    description="A simple package that allows you model arbitrary automatons.", 
    version="0.0.1",
    packages = ["simplefsm"],
    author="Lucas Liendo",
    author_email="mindmaster@gmail.com",
    keywords="automaton finite state machine",
    install_requires=["nose>=1.3.2"], 
    zip_safe=False,
    test_suite="nose.collector",
)
