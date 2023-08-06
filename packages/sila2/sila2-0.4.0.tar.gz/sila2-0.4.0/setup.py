import re
from distutils.dir_util import copy_tree
from glob import glob
from os import makedirs
from os.path import basename, dirname, join
from shutil import copy

from setuptools import setup

base_dir = dirname(__file__)


def copy_resources_from_sila_base():
    resource_dir = join(base_dir, "src", "sila2", "resources")
    makedirs(resource_dir, exist_ok=True)

    # xsd
    copy_tree(join(base_dir, "sila_base", "schema"), join(resource_dir, "xsd"))

    # xsl
    makedirs(join(resource_dir, "xsl"), exist_ok=True)
    for file in glob(join(base_dir, "sila_base", "xslt", "*.xsl")):
        copy(file, join(resource_dir, "xsl", basename(file)))

    # proto
    makedirs(join(resource_dir, "proto"), exist_ok=True)
    copy(
        join(base_dir, "sila_base", "protobuf", "SiLAFramework.proto"),
        join(resource_dir, "proto", "SiLAFramework.proto"),
    )
    copy(
        join(base_dir, "sila_base", "protobuf", "SiLABinaryTransfer.proto"),
        join(resource_dir, "proto", "SiLABinaryTransfer.proto"),
    )


def prepare_readme():
    """README contains gitlab-internal links, which need to be extended for PyPI"""
    content = open(join(dirname(__file__), "README.md")).read()
    link_pattern = r"\]\(([^h][^)]+)\)"
    return re.sub(link_pattern, "](https://gitlab.com/sila2/sila_python/-/tree/master/\\1)", content)


copy_resources_from_sila_base()

setup(
    long_description=prepare_readme(),
)
