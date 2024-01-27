from duckduckgo_search import DDGS


def search_images(
    keywords,
    region="wt-wt",
    safesearch="moderate",
    size=None,
    color=None,
    type_image=None,
    layout=None,
    license_image=None,
    max_results=100,
) -> list[str]:
    """
    Wrapper for the DuckDuckGo Search API, returning URL strings.

    Args:
        keywords (str): Keywords for query.
        region (str, optional): Region code, e.g., wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch (str, optional): Safesearch level, can be 'on', 'moderate', 'off'. Defaults to "moderate".
        timelimit (str, optional): Time limit for the search, can be 'Day', 'Week', 'Month', 'Year'. Defaults to None.
        size (str, optional): Size of the images to search for, can be 'Small', 'Medium', 'Large', 'Wallpaper'. Defaults to None.
        color (str, optional): Color of the images to search for, can be 'color', 'Monochrome', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple', 'Pink', 'Brown', 'Black', 'Gray', 'Teal', 'White'. Defaults to None.
        type_image (str, optional): Type of the images to search for, can be 'photo', 'clipart', 'gif', 'transparent', 'line'. Defaults to None.
        layout (str, optional): Layout of the images to search for, can be 'Square', 'Tall', 'Wide'. Defaults to None.
        license_image (str, optional): License of the images to search for, can be 'any' (All Creative Commons), 'Public' (PublicDomain), 'Share' (Free to Share and Use), 'ShareCommercially' (Free to Share and Use Commercially), 'Modify' (Free to Modify, Share, and Use), 'ModifyCommercially' (Free to Modify, Share, and Use Commercially). Defaults to None.
        max_results (int, optional): Maximum number of results. If None, returns results only from the first response. Defaults to None.

    Returns:
        list[str]: List of image URLs.
    """
    with DDGS() as ddgs:
        ddgs_images_gen = ddgs.images(
            keywords,
            region=region,
            safesearch=safesearch,
            size=size,
            color=color,
            type_image=type_image,
            layout=layout,
            license_image=license_image,
            max_results=max_results,
        )
        urls = [result["image"] for result in ddgs_images_gen]

    return urls
