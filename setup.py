from setuptools import setup, find_packages

setup(
    name="hivra-capsulenet",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'capsulenet=cli:main',
        ],
    },
    author="Hivra Network",
    description="Distributed capsule architecture for trusted connections",
    python_requires=">=3.8",
)
