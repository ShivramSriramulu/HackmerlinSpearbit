from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hackmerlin-agent",
    version="1.0.0",
    author="Hrkrshnn",
    author_email="your.email@example.com",
    description="An autonomous agent for playing the HackMerlin puzzle game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ShivramSriramulu/HackmerlinSpearbit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "hackmerlin-agent=working_agent:main",
        ],
    },
    keywords="automation, selenium, ai, puzzle, game, hackmerlin",
    project_urls={
        "Bug Reports": "https://github.com/ShivramSriramulu/HackmerlinSpearbit/issues",
        "Source": "https://github.com/ShivramSriramulu/HackmerlinSpearbit",
        "Documentation": "https://github.com/ShivramSriramulu/HackmerlinSpearbit#readme",
    },
)
