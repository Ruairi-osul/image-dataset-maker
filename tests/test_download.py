from image_dataset_maker.download import _url_to_image_filename


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
