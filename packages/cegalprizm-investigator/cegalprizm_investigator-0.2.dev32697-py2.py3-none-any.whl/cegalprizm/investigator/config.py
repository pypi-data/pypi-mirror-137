# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

import os

# pylint: disable=relative-beyond-top-level

from .utils import _get_envvar


class Config():

    __web_url: str = None
    __image_path: str = None
    __image_count: int = 0

    @staticmethod
    def set_web_url(web_url: str):
        Config.__web_url = web_url

    @staticmethod
    def get_web_url():
        if Config.__web_url is None:
            val = _get_envvar("CEGAL_INVESTIGATOR_WEB_URI")
            if val[0]:
                return val[1]
            else:
                return "http://localhost:5000/invweb"
        else:
            return Config.__web_url

    # @staticmethod
    # def get_web_api_url():
    #     val = _get_envvar("CEGAL_INVESTIGATOR_WEB_API_URI")
    #     if val[0]:
    #         return val[1]
    #     else:
    #         return "http://localhost:5000"

    @staticmethod
    def set_image_path(path: str):
        Config.__image_count = 0
        if not os.path.exists(path) or not os.path.isdir(path):
            Config.__image_path = None
            return

        Config.__image_path = path

    @staticmethod
    def get_image_path():
        if Config.__image_path is None:
            return None
        Config.__image_count += 1
        return os.path.join(Config.__image_path, str(Config.__image_count) + ".bmp")

    @staticmethod
    def print():
        print(f"InvPy Web URL : {Config.get_web_url()}")
