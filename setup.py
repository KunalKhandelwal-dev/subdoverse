from pathlib import Path

from setuptools import setup, find_packages

BASE_DIR = Path(__file__).parent

README = (
    BASE_DIR / "README.md"
).read_text(
    encoding="utf-8"
)


setup(
    name="subdoverse",

    version="1.0.0",

    description="Professional Python-based Subdomain Enumeration Tool",

    long_description=README,

    license="MIT",

    long_description_content_type="text/markdown",

    author="Kunal Khandelwal",

    author_email="your-email@example.com",

    url="https://github.com/KunalKhandelwal-dev/subdoverse",

    project_urls={
        "Source": "https://github.com/KunalKhandelwal-dev/subdoverse",
        "Issues": "https://github.com/KunalKhandelwal-dev/subdoverse/issues",
        "Documentation": "https://github.com/KunalKhandelwal-dev/subdoverse",
    },

    python_requires=">=3.10",

    packages=find_packages(),

    include_package_data=True,

    package_data={
        "subdoverse": [
            "config.json",
        ],
    },

    keywords=[
        "subdomain",
        "reconnaissance",
        "osint",
        "bug bounty",
        "pentesting",
        "cybersecurity",
        "dns",
        "enumeration",
        "security",
    ],

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",

        "Topic :: Security",
        "Topic :: Internet",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3",

        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",

        "Operating System :: OS Independent",
    ],

    install_requires=[
        "requests>=2.34.0",
        "dnspython>=2.8.0",
    ],

    entry_points={
        "console_scripts": [
            "subdoverse=subdoverse.main:main",
        ],
    },


)