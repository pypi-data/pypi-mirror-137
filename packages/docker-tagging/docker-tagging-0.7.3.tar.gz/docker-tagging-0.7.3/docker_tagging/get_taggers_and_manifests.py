# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from typing import Callable, Optional, Dict, List, Tuple
from .images_hierarchy import ImageDescription, TaggerInterface, ManifestInterface


def get_taggers_and_manifests(
        short_image_name: str,
        get_all_images
) -> Tuple[List[TaggerInterface], List[ManifestInterface]]:
    taggers = []
    manifests = []
    while short_image_name is not None:
        image_description = get_all_images(short_image_name)

        taggers = image_description.taggers + taggers
        manifests = image_description.manifests + manifests

        short_image_name = image_description.parent_image
    return taggers, manifests
