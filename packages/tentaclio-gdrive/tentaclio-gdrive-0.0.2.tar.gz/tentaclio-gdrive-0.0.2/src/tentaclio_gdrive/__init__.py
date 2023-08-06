"""This package implements the tentaclio gdrive client """
from tentaclio import *  # noqa

from .clients.google_drive_client import GoogleDriveFSClient


# Google drive handlers
STREAM_HANDLER_REGISTRY.register(  # type: ignore
    "googledrive", StreamURLHandler(GoogleDriveFSClient)  # type: ignore
)
STREAM_HANDLER_REGISTRY.register("gdrive", StreamURLHandler(GoogleDriveFSClient))  # type: ignore
SCANNER_REGISTRY.register("googledrive", ClientDirScanner(GoogleDriveFSClient))  # type: ignore
SCANNER_REGISTRY.register("gdrive", ClientDirScanner(GoogleDriveFSClient))  # type: ignore
REMOVER_REGISTRY.register("googledrive", ClientRemover(GoogleDriveFSClient))  # type: ignore
REMOVER_REGISTRY.register("gdrive", ClientRemover(GoogleDriveFSClient))  # type: ignore
