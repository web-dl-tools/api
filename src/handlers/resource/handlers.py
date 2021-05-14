"""
Resource handlers.

This file contains the BaseHandler implementation of the resource handler.
"""
import re
import requests
import time

from urllib.parse import urljoin
from selenium import webdriver

from src.download.handlers import BaseHandler, BaseHandlerStatus
from ..utils import create_resource_folder, extract_file_extension, extract_filename, download_request


class ResourceHandler(BaseHandler):
    """
    A resource handler which implements the BaseHandler object.
    """

    driver = None
    html = None
    paths = None

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
        except (requests.exceptions.ConnectionError, requests.exceptions.InvalidSchema):
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
        self.driver = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            options=self.configure_chrome_options(),
        )
        self.driver.set_page_load_timeout(30)
        self.logger.debug("Setup Selenium webdriver connection instance.")

        self.logger.debug(f"Loading {self.request.url} in Selenium Server instance...")
        self.driver.get(self.request.url)
        self.logger.info(f"Finished loading in Selenium Server instance. Sleeping 10 seconds to allow scripts to complete...")
        time.sleep(10)

        self.html = self.driver.page_source
        title = self.driver.title
        self.request.set_title(
            title if title else "Page has no title"
        )
        self.logger.info(f"Extracted browser rendered html and title '{self.request.title}'.")

        self.extract_paths()

        create_resource_folder(self.request.path)
        self.logger.debug(f"Created folder for resource.")

        self.save_screenshot()
        self.logger.info("Created and saved screenshot.")

        self.driver.quit()
        self.logger.debug("Quit the Selenium Server instance and closes all associated windows.")

    def download(self) -> None:
        """
        Additional download steps which extracts
        all paths from the resource, trims and
        filterers them according to the given
        extensions and additionally removes duplicates.

        :return: None
        """
        for i, path in enumerate(self.paths):
            self.download_file(path)
            self.request.set_progress(int(((i + 1) / len(self.paths)) * 100))

    def configure_chrome_options(self) -> webdriver.ChromeOptions:
        """
        Configure chrome options for Selenium Server.

        :return: a ChromeOptions object.
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-features=NetworkService")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument('--window-size=1920,1080')
        self.logger.debug("Setup Selenium Server configuration.")

        return chrome_options

    def save_screenshot(self):
        """
        Save a screenshot of the current Selenium Server instance.
        """
        with open(f"{self.request.path}/{self.request.id}.png", "wb+") as f:
            f.write(self.driver.get_screenshot_as_png())

    def extract_paths(self) -> None:
        """
        Extracts all paths from the resource, trims and
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

        self.paths = filtered_paths

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

        extension = extract_file_extension(dict(r.headers))
        filename = extract_filename(url, dict(r.headers), extension)
        self.logger.debug(
            f"Extracted extension {extension} and filename {filename}."
        )

        self.logger.debug(f"Started download.")
        result = download_request(url, self.request.path, filename, extension)
        self.logger.info(f"Finished download with {', '.join('{} {}'.format(k,v) for k,v in result.items())}.")
