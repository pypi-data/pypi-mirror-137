import setuptools
import re

with open("README.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

version = ""
with open("disno/__init__.py") as f:
    search = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)

    if search is not None:
        version = search.group(1)
    else:
        raise RuntimeError("Could not grab version string")

packages = [
    "disno",
    "disno.objects",
    "disno.http",
    "disno.http.endpoints",
]

setuptools.setup(
    name="disno",
    version=version,
    author="Middledot",
    author_email="middledot.productions@gmail.com",
    description="Another discord api wrapper just ignore",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/QwireDev/disno",
    project_urls={
        "Issue Tracker": "https://github.com/QwireDev/disno/issues",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=packages,
    python_requires=">=3.6",
)