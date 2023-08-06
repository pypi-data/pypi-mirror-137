# issuudl-py
*A python-based downloader for Issuu.*
---
# Functions
## download(url, end, ext, folder, start) and downloadWithId(id, end, ext, folder, start)
    download(url: str, end: int, ext: str, folder: str ="./", start: int = 1)
    downloadWithId(id: str, end: int, ext: str, folder: str ="./", start: int = 1)

These 2 functions download all pages within the given range.

Required variables: Article URL or ID. Page you want it to end on. Extension ("swf", "jpg" or "both").

Optional variables: Folder you want it to be stored (must exist, otherwise defaults to the folder the script is running in). Starting page (defaults to the first page).

The URL/ID, extension and folder must be strings. Starting and ending pages must be integers.

## downloadPage(url, page, ext, folder) and downloadPageWithId(id, page, ext, folder)
    downloadPage(url: str, page: int, ext: str, folder: str ="./")
    downloadPageWithId(id: str, page: int, ext: str, folder: str ="./issuu/")

These 2 functions downloads the specific page. Can also be done with download() but this makes it easier.

Required variables: Article URL or ID. Specific page. Extension ("swf", "jpg" or "both").

Optional variables: Folder you want it to be stored (must exist, otherwise defaults to the folder the script is running in).

The URL/ID, extension and folder must be strings. The desired page must be an integer.

## getId(url)
    getId(url: str)

This function retrieves the article ID.

Required variables: Article URL.

The URL must be a string.

## getJPG(page, id, folder) and getSWF(page, id, folder)
    getJPG(page: int, id: str, folder: str ="./")
    getSWF(page: int, id: str, folder: str ="./")

This retrieves the Jpeg file or Flash file.

Required variables: Article ID. Specific page.

Optional variables: Folder you want it to be stored (must exist, otherwise defaults to the folder the script is running in).

The ID and folder must be strings. The desired page must be an integer.