"""Storage wrapper for image upload/update/delete operations."""
from django.core.files.storage import default_storage


def upload_image(file_obj, path: str) -> str:
    """Upload an image using local media in DEBUG and Cloudinary otherwise."""
    return default_storage.save(path, file_obj)


def delete_image(path: str | None) -> None:
    """Delete an image if it exists in the configured storage backend."""
    if path and default_storage.exists(path):
        default_storage.delete(path)


def update_image(old_path: str | None, file_obj, path: str) -> str:
    """Replace an existing image and return the new stored path."""
    delete_image(old_path)
    return upload_image(file_obj, path)
