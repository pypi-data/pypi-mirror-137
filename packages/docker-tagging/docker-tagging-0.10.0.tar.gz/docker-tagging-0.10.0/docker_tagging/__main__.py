#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
import argparse
from pathlib import Path
from .images_hierarchy import create_images
from .tag_image import tag_image
from .create_manifests import create_manifests
from .create_version import create_version


def main():
    logging.basicConfig(level=logging.INFO)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--config", required=True, help="Path to the docker-tagging config (yaml)")
    arg_parser.add_argument("--short-image-name", required=True, help="Short image name to apply tags for")
    arg_parser.add_argument("--owner", required=True, help="Owner of the image")
    arg_parser.add_argument("--wiki-path", required=True, help="Path to the wiki pages")
    arg_parser.add_argument("--version-file", action='store_true')
    args = arg_parser.parse_args()

    get_all_images = create_images(Path(args.config), args.version_file)
    tag_image(args.short_image_name, args.owner, get_all_images)
    create_manifests(args.short_image_name, args.owner, args.wiki_path, get_all_images)
    create_version(args.short_image_name, get_all_images)


if __name__ == "__main__":
    main()
