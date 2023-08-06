# Copyright 2022 Ryan Eloff
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Setup fastconf."""
import codecs
import pathlib
import re
from typing import List

import pkg_resources
import setuptools


NAME = "lightconf"
PACKAGES = ["lightconf"]
META_PATH = ["lightconf", "__init__.py"]
KEYWORDS = ["configuration", "config", "cfg", "dataclass", "yaml"]
CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
PYTHON_REQUIRES = ">=3.6"


HERE = pathlib.Path(__file__).parent.resolve()


def read_encoded(rel_path: pathlib.Path) -> str:
    """Extract contents from an encoded file."""
    with codecs.open(str(HERE.joinpath(rel_path)), "r") as fp:
        return fp.read()


META_FILE = read_encoded(pathlib.Path(META_PATH[0]).joinpath(*META_PATH[1:]))


def find_meta(meta: str) -> str:
    """Extract __*meta*__ from META_FILE.

    cf. https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
    source https://github.com/python-attrs/attrs/blob/7804a68ee3dd2c2a0302d482237c51ce975ef17f/setup.py#L90
    """
    meta_match = re.search(rf"^__{meta}__ = ['\"]([^'\"]*)['\"]", META_FILE, re.M)
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(f"Unable to find __{meta}__ string.")


def get_long_desc(rel_path: str) -> str:
    """Extract long description from README file."""
    with HERE.joinpath(rel_path).open() as fp:
        long_desc = fp.read()
    return long_desc


def get_install_requires(rel_path: str) -> List[str]:
    """Extract install requirements from requirements.txt file."""
    with HERE.joinpath(rel_path).open() as fp:
        install_requires = [
            str(requirement) for requirement in pkg_resources.parse_requirements(fp)
        ]
    return install_requires


if __name__ == "__main__":
    setuptools.setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=find_meta("url"),
        project_urls={
            "Source Code": find_meta("url"),
            # TODO(rpeloff) changelog
        },
        version=find_meta("version"),
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        keywords=KEYWORDS,
        long_description=get_long_desc("README.md"),
        long_description_content_type="text/markdown",
        packages=PACKAGES,
        classifiers=CLASSIFIERS,
        python_requires=PYTHON_REQUIRES,
        install_requires=get_install_requires("requirements.txt"),
    )
