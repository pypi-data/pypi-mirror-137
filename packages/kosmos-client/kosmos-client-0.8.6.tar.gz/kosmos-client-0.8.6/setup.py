import setuptools
setuptools.setup(
    name="kosmos-client",
    version="0.8.6",
    author="Jan Janssen",
    author_email="Jan.Janssen@dfki.de",
    description="Client to connect to the KosmoS Platform",
    long_description="README",
    # long_description_content_type="text/markdown",
    url="https://kosmos-lab.de/python-client/",
    install_requires=["websocket-client", "requests", "dataclasses-json"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    license_file="LICENSE",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
