from setuptools import setup, find_packages

requires = [
    "bumpversion",
    "certifi",
    "chardet",
    "click",
    "click-log",
    "cloudsmith-cli",
    "colorlog",
    "Cython",
    "Deprecated",
    "devpi-client",
    "idna<3",
    "jq",
    "more-itertools",
    "packaging",
    "pydantic",
    "PyGithub",
    "PyJWT",
    "python-gitlab",
    "python-gnupg",
    "pyyaml",
    "requests",
    "setuptools",
    "toml",
    "twine",
    "urllib3",
    "wheel",
    "wrapt",
    "typing-extensions;python_version<'3.8'",  # for TypedDict in python 3.6
]

setup(
    name="irt",
    packages=find_packages(),
    version="1.1.0",
    description="Inmanta release tool",
    author="Inmanta",
    author_email="code@inmanta.com",
    license="Inmanta EULA",
    install_requires=requires,
    entry_points='''
        [console_scripts]
        irt=irt.main:cmd
        dep-merge=irt.dep_merge:main
        merge-tool=irt.mergetool:main
    ''',
)
