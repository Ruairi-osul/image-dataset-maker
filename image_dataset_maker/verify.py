from PIL import Image
from pathlib import Path
import os
from concurrent.futures import ProcessPoolExecutor
from functools import partial


def verify_image(image_path: Path, remove: bool = False, verbose: bool = False) -> bool:
    """Verrify an image file.

    Based on FastAI's `verify_image` function.


    Args:
        image_path (Path): Path to the image file.
        remove (bool, optional): If True, remove the image file if it is invalid. Defaults to False.
        verbose (bool, optional): If True, print error messages when verification fails. Defaults to False.

    Returns:
        bool: True if the image is valid, False otherwise.
    """
    image_path = Path(image_path)
    try:
        with Image.open(image_path) as img:
            img.load()
            img.draft(img.mode, (32, 32))
            return True
    except Exception as e:
        if verbose:
            print(f"Image file {image_path} is corrupt: {e}")
        if remove:
            image_path.unlink()
        return False


def verify_images(
    image_paths: list[Path],
    remove: bool = False,
    max_workers: int | None = None,
    verbose: bool = False,
) -> list[Path]:
    """Verify a list of image files.

    Based on FastAI's `verify_images` function.

    Args:
        image_paths (list[Path]): List of paths to image files.
        remove (bool, optional): If True, remove invalid image files. Defaults to False.
        max_workers (int | None, optional): Number of workers to use for parallel processing. If None, use all available CPUs. Defaults to None.
        verbose (bool, optional): If True, print error messages when verification fails. Defaults to False.

    Returns:
        list[Path]: List of paths to valid image files.
    """
    image_paths = list(image_paths)
    if max_workers is None:
        max_workers = os.cpu_count()

    verify_func = partial(verify_image, remove=remove, verbose=verbose)
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = executor.map(verify_func, image_paths)
        valid_image_paths = [
            image_path for image_path, is_valid in zip(image_paths, futures) if is_valid
        ]

    return valid_image_paths



