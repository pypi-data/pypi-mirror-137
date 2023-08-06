from setuptools import setup, find_packages
setup(
    name="burst_tools",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[
        "pynvml"
    ],
    scripts=['bin/gpumem'],
    python_requires='>=3',
)
