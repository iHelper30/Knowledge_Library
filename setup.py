from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="comprehensive-resource-library",
    version="0.1.0",
    author="iHelper30",
    author_email="project@comprehensiveresourcelibrary.org",
    description="A sophisticated resource management and automation framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iHelper30/Comprehensive_Resource_Library",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires='>=3.8',
    install_requires=[
        'python-dotenv>=1.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'flake8>=3.9.0',
            'mypy>=0.812',
            'black>=21.5b1',
        ],
    },
    entry_points={
        'console_scripts': [
            'crl=src.cli:main',  # Placeholder for potential CLI
        ],
    },
)
