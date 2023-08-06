from setuptools import setup

setup(
    name="pydbro",
    version="0.1.0",
    description="Python Console Database Browser",
    long_description=open("README.txt").read(),
    long_description_content_type="text/plain",
    url="https://github.com/mtatton/pydbro",
    author="Michael Tatton",
    license="",
    packages=["pydbro"],
    install_requires=[
        "",
    ],
    entry_points={
        "console_scripts": [
          "pydbro = pydbro.pydbro:cli",
          "coned = pydbro.coned:cli",
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: User Interfaces",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
    ],
)
