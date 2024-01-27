from pathlib import Path


def get_image_files(root: Path, included_extensions: list[str] = None) -> list[Path]:
    """Get all image files in a directory.

    Args:
        root (Path): Path to the directory.
        included_extensions (list[str], optional): List of file extensions to include. Defaults to None.

    Returns:
        list[Path]: List of paths to image files.
    """
    included_extensions = included_extensions or [".jpg", ".jpeg", ".png", ".bmp"]
    return [
        f
        for f in root.glob("**/*")
        if f.suffix.lower() in included_extensions and f.is_file()
    ]
