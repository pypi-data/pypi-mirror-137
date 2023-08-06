from setuptools import setup, find_packages

setup(
    name="askparrot-decryption-sdk",
    version="0.1.3",
    description="Pagos decryption SDK",
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["pagos_data_cipher"],
    include_package_data=True,
    install_requires=["pycryptodome"]
)