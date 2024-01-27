from image_dataset_maker import (
    search_images,
    download_images,
    verify_images,
    resize_images,
    get_image_files,
)
from pathlib import Path

dest_dir = Path("images")

# Search for images of bears
image_urls = search_images(keywords="bears", max_results=10)

# Download the images
downloaded_paths = download_images(image_urls, dest_dir=dest_dir)

# Find Image Files
image_paths = get_image_files(dest_dir)

# Verify the images, remove corrupt
verified_paths = verify_images(image_paths, remove=True)

# Resize the images
resized_paths = resize_images(verified_paths, (256, 256), resampling="box")
