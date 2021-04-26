"""
Resource handlers.

This file contains the BaseHandler implementation of the resource handler.
"""
import os
import re
import requests
import mimetypes
import time

from urllib.parse import urljoin
from selenium import webdriver

from src.download.handlers import BaseHandler, BaseHandlerStatus


class ResourceHandler(BaseHandler):
    """
    A resource handler which implements the BaseHandler object.
    """

    driver = None
    html = None

    @staticmethod
    def handles(url: str) -> BaseHandlerStatus:
        """
        Notify the status of a handler for a given url.

        :param url: a str containing a valid url.
        :return: a BaseHandlerStatus object containing the status for the linked handler.
        """
        from .models import ResourceRequest

        status = BaseHandlerStatus(ResourceRequest.__name__)
        status.set_options({})

        try:
            r = requests.head(url, allow_redirects=True)
            status.set_supported(
                r.headers["content-type"].startswith("text/html")
                and r.status_code == requests.codes.ok
            )
        except requests.exceptions.InvalidSchema:
            status.set_supported(False)

        return status

    def pre_process(self) -> None:
        """
        Additional pre-processing steps which
        loads the external url in a Chromium instance
        connected and managed by Selenium Server in order to
        extracts the html and title from the request raw data
        and prepares the filepath(s).

        :return: None
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')

        self.driver = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            options=chrome_options,
        )
        self.driver.set_page_load_timeout(30)
        self.logger.debug("Setup Selenium Server webdriver connection instance.")

        self.driver.get(self.request.url)
        self.logger.debug(f"Loaded {self.request.title} in Selenium Server instance. Sleeping 10 seconds to allow scripts to complete.")
        time.sleep(10)

        self.html = self.driver.page_source
        title = self.driver.title
        self.request.set_title(
            title if title else "Page has no title"
        )
        self.logger.info(f"Extracted html and title '{self.request.title}'.")

        if not os.path.exists(self.request.path):
            os.makedirs(self.request.path)
            self.logger.info(f"Created folder for resource.")

        with open(f"{self.request.path}/{self.request.id}.png", "wb+") as f:
            f.write(self.driver.get_screenshot_as_png())
            self.logger.info("Created and saved screenshot.")

        self.driver.quit()
        self.logger.debug("Destroyed Selenium Server webdriver connection instance.")

    def download(self) -> None:
        """
        Additional download steps which extracts
        all paths from the resource, trims and
        filterers them according to the given
        extensions and additionally removes duplicates.

        :return: None
        """
        paths = []

        # Extract all absolute paths.
        for m in re.finditer(
                r"(http|ftp|https)(:\/\/)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])?",
                self.html
        ):
            paths.append(m.group())

        # Extract all relative paths and join with request url.
        for m in re.finditer(r"(\"|')(\/[\w\.\-]+)+\/?", self.html):
            paths.append(urljoin(self.request.url, m.group()[1:]))
        for m in re.finditer(r"(\"|')(..\/)+([\w\.\-\/]+)+(\"|')", self.html):
            paths.append(urljoin(self.request.url, m.group()[1:]))

        # Extract all absolute paths and prepend with request url schema.
        for m in re.finditer(r"(\"|')(\/\/)([\w|.|\/]+)+", self.html,):
            paths.append(urljoin(self.request.url, m.group()[1:]))

        self.logger.debug(f"Extracted {len(paths)} paths.")

        # Trim endings
        paths = [
            path.strip("\"'") for path in paths
        ]

        # filter
        filtered_paths = [
            path for path in paths if path.endswith(tuple(self.request.extensions))
        ]

        # Remove duplicates
        filtered_paths = list(dict.fromkeys(filtered_paths))
        self.logger.debug(f"Filtered down to {len(filtered_paths)} paths.")
        self.request.set_data({"paths": paths, "filtered_paths": filtered_paths})

        for i, path in enumerate(filtered_paths):
            self.download_file(path)
            self.request.set_progress(int(((i + 1) / len(filtered_paths)) * 100))

    def download_file(self, url: str) -> None:
        """
        Generate the filename and extension of an url
        resource and download the file accordingly.

        :param url: A str containing a valid url resource.
        :return: None
        """
        self.logger.debug(f"Processing url {url}.")

        r = requests.get(url, stream=True)
        size = r.headers.get("content-length")

        if size is None:
            self.logger.warn(f"Resource has no given file size. Downloading anyway.")
        elif int(size) < self.request.min_bytes:
            self.logger.warn(f"Resource file is too small ({size} bytes). Skipping.")
            return

        content_type = r.headers["content-type"].split(";")[0]
        extension = mimetypes.guess_extension(content_type)
        filename = (
            re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]
            if "Content-Disposition" in r.headers.keys()
            else url.split("/")[-1]
        )
        if filename.endswith(extension):
            filename = filename[: -len(extension)]

        self.logger.debug(
            f"Extracted extension {extension} and created filename {filename}."
        )

        with open(f"{self.request.path}/{filename}{extension}", "wb+") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

        self.logger.info(f"Finished with url {url}.")
