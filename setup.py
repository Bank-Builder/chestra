from setuptools import find_packages, setup

setup(
    name="chestra",
    version="0.1.0",
    description="A modular, plugin-based workflow orchestrator for Pythonistas.",
    author="Andrew Turpin",
    author_email="andrew@turpin.co.za",
    url="https://github.com/bank-builder",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "PyYAML>=6.0",
        "requests>=2.28"
    ],
    python_requires=">=3.7",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "chestra=chestra.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
