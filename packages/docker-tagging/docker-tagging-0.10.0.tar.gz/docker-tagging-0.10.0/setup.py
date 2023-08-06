# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docker_tagging']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'docker>=5.0.3,<6.0.0', 'plumbum>=1.7.0,<2.0.0']

entry_points = \
{'console_scripts': ['tagging = docker_tagging.__main__:main']}

setup_kwargs = {
    'name': 'docker-tagging',
    'version': '0.10.0',
    'description': 'Docker stacks tagging and manifest creation. This project is inspired on https://github.com/jupyter/docker-stacks.',
    'long_description': '# Docker stacks tagging and manifest creation\n\nThe main purpose of the source code in this folder is to properly tag all the images and to update [build manifests](https://github.com/jupyter/docker-stacks/wiki).\nThese two processes are closely related, so the source code is widely reused.\n\nBasic example of a tag is a `python` version tag.\nFor example, an image `jupyter/base-notebook` with `python 3.8.8` will have a tag `jupyter/base-notebook:python-3.8.8`.\nThis tag (and all the other tags) are pushed to Docker Hub.\n\nManifest is a description of some important part of the image in a `markdown`.\nFor example, we dump all the `conda` packages including their versions.\n\n## Main principles\n\n- All the images are located in a hierarchical tree. More info on [image relationships](../docs/using/selecting.md#image-relationships).\n- We have `tagger` and `manifest` classes, which can be run inside docker containers to obtain tags and build manifest pieces.\n- These classes are inherited from the parent image to all the children images.\n- Because manifests and tags might change from parent to children, `taggers` and `manifests` are reevaluated on each image. So, the values are not inherited.\n- To tag an image and create a manifest, run `make hook/base-notebook` (or another image of your choice).\n\n## Source code description\n\nIn this section we will briefly describe source code in this folder and give examples on how to use it.\n\n### DockerRunner\n\n`DockerRunner` is a helper class to easily run a docker container and execute commands inside this container:\n\n```python\nfrom .docker_runner import DockerRunner\n\nwith DockerRunner("ubuntu:bionic") as container:\n    DockerRunner.run_simple_command(container, cmd="env", print_result=True)\n```\n\n### GitHelper\n\n`GitHelper` methods are run in the current `git` repo and give the information about last commit hash and commit message:\n\n```python\nfrom .git_helper import GitHelper\n\nprint("Git hash:", GitHelper.commit_hash())\nprint("Git message:", GitHelper.commit_message())\n```\n\nPrefix of commit hash (namely, 12 letters) is used as an image tag to make it easy to inherit from a fixed version of a docker image.\n\n### Tagger\n\n`Tagger` is a class, which can be run inside docker container to calculate some tag for an image.\n\nAll the taggers are inherited from `TaggerInterface`:\n\n```python\nclass TaggerInterface:\n    """Common interface for all taggers"""\n    @staticmethod\n    def tag_value(container) -> str:\n        raise NotImplementedError\n```\n\nSo, `tag_value(container)` method gets a docker container as an input and returns some tag.\n\n`SHATagger` example:\n\n```python\nclass SHATagger(TaggerInterface):\n    @staticmethod\n    def tag_value(container):\n        return GitHelper.commit_hash_tag()\n```\n\n- `taggers.py` contains all the taggers.\n- `tag_image.py` is a python executable which is used to tag the image.\n\n### Manifest\n\n`ManifestHeader` is a build manifest header.\nIt contains information about `Build datetime`, `Docker image size` and `Git commit` info.\n\nAll the other manifest classes are inherited from `ManifestInterface`:\n\n```python\nclass ManifestInterface:\n    """Common interface for all manifests"""\n    @staticmethod\n    def markdown_piece(container) -> str:\n        raise NotImplementedError\n```\n\n- `markdown_piece(container)` method returns piece of markdown file to be used as a part of build manifest.\n\n`AptPackagesManifest` example:\n\n```python\nclass AptPackagesManifest(ManifestInterface):\n    @staticmethod\n    def markdown_piece(container) -> str:\n        return "\\n".join([\n            "## Apt Packages",\n            "",\n            quoted_output(container, "apt list --installed")\n        ])\n```\n\n- `quoted_output` simply runs the command inside container using `DockerRunner.run_simple_command` and wraps it to triple quotes to create a valid markdown piece of file.\n- `manifests.py` contains all the manifests.\n- `create_manifests.py` is a python executable which is used to create the build manifest for an image.\n\n### Images Hierarchy\n\nAll images dependencies on each other and what taggers and manifest they make use of is defined in `images_hierarchy.py`.\n\n`get_taggers_and_manifests.py` defines a helper function to get the taggers and manifests for a specific image.\n',
    'author': 'Mathias Weiß',
    'author_email': 'mail@weissmedia.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/weissmedia/docker-tagging.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
