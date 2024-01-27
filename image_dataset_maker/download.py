from pathlib import Path
import requests
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from urllib.parse import urlparse, unquote


def _url_to_image_filename(url: str) -> str:
    """
    Get the filename from a URL of an image.

    Args:
        url (str): The URL of the image.

    Returns:
        str: The filename of the image.
    """
    url = url.strip()
    parsed_url = urlparse(url)
    base_filename = unquote(parsed_url.path.split("/")[-1])
    filename = base_filename.split("?")[0] if "?" in base_filename else base_filename

    return filename


def download_image(
    url: str, file_path: Optional[Path] = None, timeout: int = 10, verbose: bool = False
) -> Path | None:
    """
    Download an image from a given URL and save it to a specified file path.

    Args:
        url (str): The URL of the image to download.
        file_path (Optional[Path], optional): The path where the image will be saved. If not provided, the image will be saved in the current directory with its original name from the URL. Defaults to None.
        timeout (int, optional): The maximum time to wait for the server to respond, in seconds. Defaults to 10.
        verbose (bool, optional): If True, print error messages when download fails. Defaults to False.

    Returns:
        Path | None: The path where the image was saved, or None if the download failed.

    """
    file_path = file_path or _url_to_image_filename(url)
    file_path = Path(file_path)

    if not file_path.suffix:
        suffix = Path(url).suffix or ".jpg"
        file_path = file_path.with_suffix(suffix)

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if verbose:
            print(f"HTTP error occurred while downloading {url}")
        return None
    except requests.exceptions.ConnectionError:
        if verbose:
            print(f"Failed to connect to {url}")
        return None
    except requests.exceptions.Timeout:
        if verbose:
            print(f"Timeout occurred while connecting to {url}")
        return None
    except requests.exceptions.RequestException as err:
        if verbose:
            print(f"An error occurred: {err}")
        return None

    with open(file_path, "wb") as f:
        f.write(response.content)

    return file_path


def download_images(
    urls: list[str],
    dest_dir: Path | str | None = None,
    timeout: int = 10,
    verbose: bool = False,
    max_workers: int | None = None,
) -> list[Path | None]:
    """
    Download multiple images from given URLs and save them to a specified directory.

    Args:
        urls (list[str]): The URLs of the images to download.
        dest_dir (Path | str | None, optional): The directory where the images will be saved. If not provided, the images will be saved in the current directory. Defaults to None.
        timeout (int, optional): The maximum time to wait for the server to respond, in seconds. Defaults to 10.
        verbose (bool, optional): If True, print error messages when download fails. Defaults to False.
        max_workers (int | None, optional): The maximum number of threads that can be used to execute the given calls. If None, the number of workers will be the number of processors on the machine, multiplied by 5. Defaults to None.

    Returns:
        list[Path | None]: A list of paths where the images were saved, or None for the URLs where the download failed.
    """
    dest_dir = Path(dest_dir) if dest_dir is not None else Path.cwd()
    dest_dir.mkdir(parents=True, exist_ok=True)

    download_func = partial(download_image, timeout=timeout, verbose=verbose)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for url in urls:
            future = executor.submit(download_func, url, dest_dir / Path(url).name)
            futures.append(future)

        downloaded_paths = [future.result() for future in as_completed(futures)]

    return downloaded_paths
