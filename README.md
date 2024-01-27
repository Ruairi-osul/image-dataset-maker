# Image Dataset Maker

A small package for creating computer vision datasets.

## Installation

```bash
pip install git+https://github.com/Ruairi-osul/image-dataset-maker.git
```

## Functionality

The general idea is to generate a dataset of images by downloading the results of an image search on DuckDuckGo. The package contains functions for searching, downloading, verifying, resizing, and selecting the images. Some parts of this package are inspired by FastAI's vision utils module.

### Main Functions

- `search_images`: This function is used to search for images on DuckDuckGo.
- `download_images`: This function downloads the images found by the search function.
- `verify_images`: This function verifies the integrity of the downloaded images.
- `resize_images`: This function resizes the images to a specified size.
- `get_image_files`: This function finds images below a root path.

## Example Usage


```python
from image_dataset_maker import search_images, download_images, verify_images, resize_images, get_image_files

dest_dir = Path("images")

# Search for images of bears
image_urls = search_images(keywords="bears", max_results=10)

# Download the images
downloaded_paths = download_images(search_results, dest_dir=dest_dir)

# Find Image Files
image_paths = get_image_files(dest_dir)

# Verify the images, remove corrupt
verified_paths = verify_images(image_paths, remove=True)

# Resize the images
resized_paths = resize_images(verified_paths, (256, 256))

```
