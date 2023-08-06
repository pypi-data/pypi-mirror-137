# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import importlib.util
from pathlib import Path
from yaml import safe_load
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Callable

from .taggers import TaggerInterface
from .taggers import SHATagger
from .taggers import DateTagger
from .taggers import UbuntuVersionTagger
from .taggers import PythonVersionTagger
from .taggers import PythonProjectVersionTagger
from .taggers import PythonProjectMinorMajorVersionTagger

from .manifests import ManifestInterface
from .manifests import AptPackagesManifest
from .manifests import CondaEnvironmentManifest
from .manifests import PipEnvironmentManifest

ALL_IMAGES = {}


@dataclass
class ImageDescription:
    parent_image: Optional[str]
    version_file: Optional[bool]
    taggers: List[TaggerInterface] = field(default_factory=list)
    manifests: List[ManifestInterface] = field(default_factory=list)


def to_class(module, module_str_lst) -> list:
    module_lst = []
    for item in module_str_lst:
        try:
            module_lst.append(eval(f'module.{item}'))
        except AttributeError:
            try:
                module_lst.append(eval(item))
            except NameError as e:
                raise Exception(f'class does not exist {e}')
    return module_lst


def _load_extension_module(ext_path: Path, module_name: str):
    module = None
    if ext_path.exists():
        spec = importlib.util.spec_from_file_location(module_name, ext_path.absolute())
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return module


def get_extension(tagging, name):
    modules = None
    if 'extension_path' in tagging:
        ext_path = Path(tagging['extension_path'])
        for path in ext_path.rglob(f'{name}.py'):
            module_name = path.absolute().stem
            return _load_extension_module(path, module_name)
    return modules


def create_images(config: Path, version_file) -> Callable[[Optional[str]], Optional[Dict[str, ImageDescription]]]:
    tagging = safe_load(config.open())['docker-tagging']
    version_file = tagging.get('version_file', version_file)
    for k, v in tagging['images'].items():
        taggers = to_class(get_extension(tagging, 'taggers'), v.get('taggers', []))
        manifests = to_class(get_extension(tagging, 'manifests'), v.get('manifests', []))
        parent_image = v.get('parent_image')
        ALL_IMAGES.update(
            {
                k: ImageDescription(
                    parent_image=parent_image,
                    taggers=taggers,
                    manifests=manifests,
                    version_file=version_file
                )
            }
        )
    return lambda key=None: ALL_IMAGES[key] if key else ALL_IMAGES
