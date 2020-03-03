"""
Torrent handlers.

This file contains the BaseHandler implementation of the torrent handler.
"""
import time
import re

from qbittorrent import Client

from src.download.handlers import BaseHandler, BaseHandlerStatus


class TorrentHandler(BaseHandler):
    """
    A torrent handler which implements the BaseHandler object.
    """

    qb = None
    hash = None

    @staticmethod
    def handles(url: str) -> BaseHandlerStatus:
        """
        Notify the status of a handler for a given url.

        :param url: a str containing a valid url.
        :return: a BaseHandlerStatus object containing the status for the linked handler.
        """
        from .models import TorrentRequest

        magnet_regex = re.compile(r"magnet:\?xt=urn:btih:[a-zA-Z0-9]*")

        status = BaseHandlerStatus(TorrentRequest.__name__)
        status.set_description("A handler for downloading a torrent resource.")
        status.set_options({})
        status.set_supported(bool(magnet_regex.search(url)))

        return status

    def _pre_process(self) -> None:
        """
        An extension of the _pre_process method which
        creates an connection with the qbittorrent API.

        :return: None
        """
        super()._pre_process()

        self.qb = Client("http://qbittorrent:8001/")
        self.qb.login("admin", "adminadmin")
        self.logger.debug("Connected with qBittorrent.")

    def _download(self) -> None:
        """
        An extension of the _download method which
        download the torrent request using qbittorrent.

        :return: None
        """
        super()._download()

        self.qb.download_from_link(self.request.url, savepath=f"/{self.request.path}")
        self.logger.debug(f"Added {self.request.url} to the download list.")

        self.logger.debug(f"Waiting for qBittorrent pre-processing to complete.")
        while len(self.qb.torrents()) == 0:
            time.sleep(5)
        self.logger.debug(f"qBittorrent pre-processing has completed.")

        torrent = self.qb.torrents()[0]
        self.hash = torrent["hash"]
        self.logger.debug(f"Torrent hash {self.hash} retrieved. Starting download.")

        active = True
        while active:
            torrent = self.qb.torrents()[0]

            progress = int(torrent["progress"] * 100)
            if progress > self.request.progress:
                self.request.set_progress(progress)

            if torrent["state"] == "error":
                self.qb.delete(self.hash)
                raise Exception("An error occurred in qBittorrent.")
            elif torrent["state"] not in (
                    "metaDL",
                    "queuedDL",
                    "checkingDL",
                    "stalledDL",
                    "downloading",
                    "pausedDL",
            ):
                active = False
            else:
                time.sleep(5)

        self.logger.info("Torrent has completed download.")
        self.request.set_data(torrent)
        self.request.set_title(torrent["name"])

    def _post_process(self) -> None:
        """
        An extension of the _post_process method which
        removes the completed torrent to prevent seeding.

        :return: None
        """
        super()._post_process()

        self.qb.delete(self.hash)
        self.logger.debug(f"Torrent has been removed from qBittorrent.")
