from setuptools import find_packages, setup
import os

__version__ = os.environ.get("VERSION", "develop")

setup(
    name='flaightidl',
    version=__version__,
    description='IDL for Flyte Platform (Latch fork)',
    url='',
    maintainer='maximsmol',
    maintainer_email='max@latch.bio',
    packages=find_packages('gen/pb_python'),
    package_dir={'': 'gen/pb_python'},
    dependency_links=[],
    package_data = {
        '': ['*.pyi', 'py.typed'],
    },
    install_requires=[
        'protobuf>=3.5.0,<4.0.0',
        # Packages in here should rarely be pinned. This is because these
        # packages (at the specified version) are required for project
        # consuming this library. By pinning to a specific version you are the
        # number of projects that can consume this or forcing them to
        # upgrade/downgrade any dependencies pinned here in their project.
        #
        # Generally packages listed here are pinned to a major version range.
        #
        # e.g.
        # Python FooBar package for foobaring
        # pyfoobar>=1.0, <2.0
        #
        # This will allow for any consuming projects to use this library as
        # long as they have a version of pyfoobar equal to or greater than 1.x
        # and less than 2.x installed.
    ],
    extras_require={
        ':python_version=="2.7"': ['typing>=3.6'],  # allow typehinting PY2
    },
)
