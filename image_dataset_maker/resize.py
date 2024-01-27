from pathlib import Path
from PIL import Image
import os
from concurrent.futures import ProcessPoolExecutor
from functools import partial


def resize_image(
    image_path: Path,
    size: tuple[int, int],
    dest_path: Path | None = None,
    resampling: str = "default",
) -> None:
    """Resize an image to a given size using the specified resampling method.

    Args:
        image_path (Path): Path to the image file.
        size (tuple[int, int]): The desired size of the image.
        dest_path (Path, optional): Path where the resized image will be saved. Defaults to None.
        resampling (str, optional): The resampling method to use. Valid options are "default" "nearest", "box", "bilinear", "hamming", "bicubic", and "lanczos".
    """
    resampling_dict = {
        "default": None,
        "nearest": Image.NEAREST,
        "box": Image.BOX,
        "bilinear": Image.BILINEAR,
        "hamming": Image.HAMMING,
        "bicubic": Image.BICUBIC,
        "lanczos": Image.LANCZOS,
    }
    try:
        resampling_method = resampling_dict[resampling.lower()]
    except KeyError:
        raise ValueError(f"Invalid resampling method: {resampling}")

    if dest_path is None:
        dest_path = image_path
    image_path = Path(image_path)
    with Image.open(image_path) as img:
        img = img.resize(size, resample=resampling_method)
        img.save(image_path)


def _resize_func(image_path, size, resampling, dest_dir):
    """Helper function for parallel processing.
    
    """
    if dest_dir is not None:
        dest_path = dest_dir / image_path.name
    else:
        dest_path = None
    return resize_image(image_path, size=size, resampling=resampling, dest_path=dest_path)

def resize_images(
    image_paths: list[Path],
    size: tuple[int, int],
    resampling: str = "default",
    dest_dir: Path | None = None,
    max_workers: int | None = None,
) -> list[Path]:
    """Resize a list of image files to a given size.

    Args:
        image_paths (list[Path]): List of paths to image files.
        size (tuple[int, int]): The desired size of the images.
        resampling (str, optional): The resampling method to use. Valid options are "default" "nearest", "box", "bilinear", "hamming", "bicubic", and "lanczos".
        dest_dir (Path | None, optional): Path where the resized images will be saved. If None, the images will be resized in place. Defaults to None.
        max_workers (int | None, optional): Number of workers to use for parallel processing. If None, use all available CPUs. Defaults to None.

    Returns:
        list[Path]: List of paths to resized images.
    """
    image_paths = list(image_paths)
    if max_workers is None:
        max_workers = os.cpu_count()

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        func = partial(_resize_func, size=size, resampling=resampling, dest_dir=dest_dir)
        resized_images = list(executor.map(func, image_paths))

    return resized_images


