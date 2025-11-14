"""
Downloader module for Quick Vworld Plugin

This module provides a base downloader class using QgsFileDownloader
for synchronous HTTP GET/POST requests.
"""

import logging
from qgis.core import Qgis, QgsFileDownloader
from qgis.PyQt.QtCore import QByteArray, QEventLoop, QUrl

LOGGER = logging.getLogger('QuickVworld')


class Downloader:
    """
    HTTP Downloader base class using QgsFileDownloader.
    
    This class provides synchronous download functionality using
    QEventLoop to wait for the download to complete.
    """

    def __init__(self, url=None):
        """
        Constructor.
        
        :param url: URL to download from
        :type url: str or QUrl
        """
        if url:
            self._url = QUrl(url) if isinstance(url, str) else url
        else:
            self._url = None
            
        self.result_path = None
        self.errors = []
        self._loop = None
        self._downloader = None

    def set_url(self, url):
        """
        Set the download URL.
        
        :param url: URL to download from
        :type url: str or QUrl
        """
        self._url = QUrl(url) if isinstance(url, str) else url

    def error(self, messages):
        """
        Handle download errors.
        
        :param messages: Error message(s)
        :type messages: str or list
        """
        if isinstance(messages, list):
            self.errors.extend(messages)
        else:
            self.errors.append(messages)
        
        LOGGER.error(f"Download error: {messages}")
        
        # Quit the event loop if running
        if self._loop and self._loop.isRunning():
            self._loop.quit()

    def canceled(self):
        """Handle download cancellation."""
        LOGGER.info('Download canceled')
        
        # Quit the event loop if running
        if self._loop and self._loop.isRunning():
            self._loop.quit()

    def completed(self):
        """Handle download completion."""
        LOGGER.info('Download completed')
        
        # Quit the event loop if running
        if self._loop and self._loop.isRunning():
            self._loop.quit()

    def download_sync(self, use_post=False, post_data=None):
        """
        Download data synchronously.
        
        This method blocks until the download is complete or an error occurs.
        
        :param use_post: Use POST method instead of GET
        :type use_post: bool
        :param post_data: POST data to send (only used if use_post=True)
        :type post_data: str or bytes
        :return: True if successful, False otherwise
        :rtype: bool
        """
        if not self._url:
            LOGGER.error("No URL set for download")
            return False
            
        if not self.result_path:
            LOGGER.error("No result path set for download")
            return False

        # Clear previous errors
        self.errors = []

        try:
            if use_post and post_data:
                # POST request
                post_data_bytes = QByteArray(
                    post_data.encode() if isinstance(post_data, str) else post_data
                )
                self._downloader = QgsFileDownloader(
                    self._url,
                    self.result_path,
                    delayStart=True,
                    httpMethod=Qgis.HttpMethod.Post,
                    data=post_data_bytes
                )
            else:
                # GET request
                self._downloader = QgsFileDownloader(
                    self._url,
                    self.result_path,
                    delayStart=True
                )

            # Connect signals
            self._downloader.downloadExited.connect(self.completed)
            self._downloader.downloadError.connect(self.error)
            self._downloader.downloadCanceled.connect(self.canceled)

            # Create event loop for synchronous execution
            self._loop = QEventLoop()
            self._downloader.downloadExited.connect(self._loop.quit)
            
            # Start download
            LOGGER.info(f"Starting download from: {self._url.toString()}")
            self._downloader.startDownload()
            
            # Wait for download to complete
            self._loop.exec_()
            
            # Check for errors
            if self.errors:
                LOGGER.error(f"Download failed with errors: {self.errors}")
                return False
                
            LOGGER.info(f"Download successful: {self.result_path}")
            return True
            
        except Exception as e:
            LOGGER.exception(f"Exception during download: {e}")
            self.errors.append(str(e))
            return False
        finally:
            self._loop = None
            self._downloader = None

    def get_errors(self):
        """
        Get list of errors.
        
        :return: List of error messages
        :rtype: list
        """
        return self.errors

    def has_errors(self):
        """
        Check if there are any errors.
        
        :return: True if errors exist
        :rtype: bool
        """
        return len(self.errors) > 0

