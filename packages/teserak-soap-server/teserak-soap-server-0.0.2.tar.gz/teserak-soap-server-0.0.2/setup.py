from setuptools import setup, find_packages


setup(
    name="teserak-soap-server",
    python_requires=">=3.8",
    version='0.0.2',
    url="https://github.com/teserak/teserak-soap-server",
    license="BSD",
    description="The ASGI SOAP Server.",
    long_description="The ASGI SOAP Server.",
    author="Konrad Rymczak",
    author_email="me@teserak.com",
    packages=find_packages(exclude=["tests*"]),
    package_data={"teserak": ["py.typed"]},
    include_package_data=True,
    install_requires=[
        "starlette",
        "xsdata",
        "python-multipart",
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    zip_safe=False,
)
