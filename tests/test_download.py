from image_dataset_maker.download import (
    _url_to_image_filename,
    download_image,
    download_images,
)
from pathlib import Path


DUCK_PIC = "https://en.wikipedia.org/wiki/Mallard#/media/File:Anas_platyrhynchos_male_female_quadrat.jpg"
DUCK_PIC2 = "https://en.wikipedia.org/wiki/Mallard#/media/File:Anas_Rubripes_and_Anas_Platyrhynchos_August_2008.JPG"
TEMP_DIR = Path("tmp")


class Test_UrlToImageFilename:
    # Should return the filename of a valid URL with a single path element
    def test_valid_url_single_path(self):
        url = "https://example.com/image.jpg"
        expected_filename = "image.jpg"
        assert _url_to_image_filename(url) == expected_filename

    # Should return the filename of a valid URL with multiple path elements
    def test_valid_url_multiple_paths(self):
        url = "https://example.com/images/folder/image.jpg"
        expected_filename = "image.jpg"
        assert _url_to_image_filename(url) == expected_filename

    # Should return the filename of a valid URL with a query string
    def test_valid_url_query_string(self):
        url = "https://example.com/image.jpg?size=medium"
        expected_filename = "image.jpg"
        assert _url_to_image_filename(url) == expected_filename

    # Should return an empty string for an empty URL
    def test_empty_url(self):
        url = ""
        expected_filename = ""
        assert _url_to_image_filename(url) == expected_filename

    # Should return an empty string for a URL with no path
    def test_url_no_path(self):
        url = "https://example.com"
        expected_filename = ""
        assert _url_to_image_filename(url) == expected_filename


class TestDownloadImage:
    # Downloads image from valid URL
    def test_valid_url(self):
        url = DUCK_PIC
        try:
            file_path = "image.jpg"
            result = download_image(url, file_path)
            assert result is not None
            assert isinstance(result, Path)
            assert result.exists()
        finally:
            result.unlink()

    # Saves image to specified file path
    def test_specified_file_path(self):
        url = DUCK_PIC
        file_path = "test_image.jpg"
        result = download_image(url, file_path)
        try:
            assert result is not None
            assert isinstance(result, Path)
            assert result.exists()
            assert result == Path(file_path)
        finally:
            result.unlink()

    # Returns None for invalid URL
    def test_invalid_url(self):
        url = "invalid_url"
        result = download_image(url)
        assert result is None

    # Returns None for invalid file path
    def test_invalid_file_path(self):
        url = "https://example.com/image.jpg"
        file_path = ""
        result = download_image(url, file_path)
        assert result is None

    # Returns None for HTTP error status code
    def test_http_error_status_code(self):
        url = "https://example.com/nonexistent.jpg"
        result = download_image(url)
        assert result is None


class TestDownloadImages:
    # Should download and save images to specified directory
    def test_download_to_specified_directory(self):
        urls = [
            DUCK_PIC,
            DUCK_PIC2,
        ]
        dest_dir = TEMP_DIR

        downloaded_paths = download_images(urls, dest_dir=dest_dir)

        try:
            assert len(downloaded_paths) == len(urls)
            for path in downloaded_paths:
                assert path is not None
                assert Path(path).is_file()
                assert Path(path).parent == Path(dest_dir)
        finally:
            for path in downloaded_paths:
                if path is not None:
                    Path(path).unlink()

    # Should download and save images to current directory if no destination directory is provided
    def test_download_to_current_directory(self):
        urls = [
            DUCK_PIC,
            DUCK_PIC2,
        ]

        downloaded_paths = download_images(urls)

        try:
            assert len(downloaded_paths) == len(urls)
            for path in downloaded_paths:
                assert path is not None
                assert Path(path).is_file()
                assert Path(path).parent == Path.cwd()
        finally:
            for path in downloaded_paths:
                if path is not None:
                    Path(path).unlink()

    # Should download and save images with their original names from the URL if no file path is provided
    def test_download_with_original_names(self):
        urls = [
            DUCK_PIC,
            DUCK_PIC2,
        ]

        downloaded_paths = download_images(urls)

        # match the filename from the URL
        downloaded_paths = sorted(downloaded_paths, key=lambda path: Path(path).name)
        urls = sorted(urls, key=lambda url: Path(url).name)

        try:
            assert len(downloaded_paths) == len(urls)
            for path, url in zip(downloaded_paths, urls):
                assert path is not None
                assert Path(path).is_file()
                assert Path(path).name.lower() == Path(url).name.lower()
        finally:
            for path in downloaded_paths:
                if path is not None:
                    Path(path).unlink()
