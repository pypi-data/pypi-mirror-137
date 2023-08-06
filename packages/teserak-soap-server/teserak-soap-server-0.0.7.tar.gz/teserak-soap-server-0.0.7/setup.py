from setuptools import find_packages, setup

setup(
    name="teserak-soap-server",
    python_requires=">=3.8",
    version="0.0.7",
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
        "starlette==0.16.0",
        "xsdata==22.1",
        "python-multipart==0.0.5",
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
