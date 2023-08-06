import os
from .git_helper import GitHelper


def create_version(short_image_name: str, get_all_images):
    image_description = get_all_images(short_image_name)
    if image_description.version_file:
        version_file = os.path.join(short_image_name, ".docker-tagging-version")
        if not os.path.exists(version_file):
            version_file = ".docker-tagging-version"
        with open(version_file, "w") as f:
            f.write(GitHelper.commit_hash_tag())
