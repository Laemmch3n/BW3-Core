#!/usr/bin/python
# -*- coding: utf-8 -*-
"""!
    ____  ____  ______       __      __       __       _____
   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  /
  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <
 / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /
/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/
                German BOS Information Script
                     by Bastian Schroll

@file:        doubleFilter.py
@date:        15.01.2018
@author:      Bastian Schroll
@description: Class to implement a filter for double alarms
@todo test, refactor and document
@todo check_msg is not implemented yet
"""
import logging
import time

from boswatch.config import Config

logging.debug("- %s loaded", __name__)


class DoubleFilter:
    """!Double Filter Class"""

    def __init__(self, scanWord):
        """!init"""
        self._config = Config()
        self._filterList = []
        self._scanWord = scanWord

    def check(self, bwPacket):
        for listPacket in self._filterList:
            if listPacket.get("timestamp") < (time.time() - self._config.getInt("doubleFilter", "IgnoreTime", "serverConfig")):
                self._filterList.remove(listPacket)
                logging.debug("entry to old remove")
                continue

            if listPacket.get(self._scanWord) is bwPacket.get(self._scanWord):
                self._filterList.remove(listPacket)
                logging.debug("found a same and remove the old one")

        self._filterList.insert(0, bwPacket)
        self._deleteTooMuch()
        logging.debug(self._filterList)

    def _deleteTooMuch(self):
        if len(self._filterList) > self._config.getInt("doubleFilter", "MaxEntry", "serverConfig"):
            logging.debug("list full, delete one")
            self._filterList.pop()