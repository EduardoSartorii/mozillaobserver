#!/usr/bin/python3
#! -*- coding: utf-8 -*-
__author__ = 'Eduardo Sartori'
__license__ = "MIT"
__version__ = "1.0.1"

import yaml
import os
import logging
import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs

class Main:
    def __init__(self):
        with open("utils/config/config.yml", 'r') as stream:
            data = yaml.load(stream, Loader=yaml.FullLoader)        
            self.debug = data.get('debug', '')
            self.url = data.get('url', '')
            self.path_webdriver = data.get("path_webdriver", '')
            self.headless = data.get("headless", '')

        if self.debug:
            logging.basicConfig(
                level = logging.DEBUG,
                format = '%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                datefmt = '%Y-%m-%d %H:%M:%S',
            )	
        else:
            logging.basicConfig(
                level = logging.INFO,
                format = '%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                datefmt = '%Y-%m-%d %H:%M:%S',
            )
        self.logger = logging.getLogger(__name__)
        options = webdriver.FirefoxOptions()
        if self.headless:
            options.add_argument("-headless")
            self.logger.info("Headless está ativado, o browser não será aberto.")
        else:
            self.logger.info("Headless está desativado, o browser será aberto.")		
        _browser_profile = webdriver.FirefoxProfile()
        _browser_profile.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0")
        _browser_profile.set_preference("dom.webnotifications.enabled", False)
        self.driver = webdriver.Firefox(executable_path=self.path_webdriver,options=options,firefox_profile=_browser_profile)
    @property
    def start(self):
        self.logger.info("[STATUS] Iniciando novo ciclo")
        self.request_url()

    def request_url(self):
        self.logger.info(f"[STATUS] Realizando request na página: {self.url}")        
        self.driver.get(f"{self.url}")
        time.sleep(4)
        self.parse_html(content= bs(self.driver.page_source,"html.parser"))


    def parse_html(self, content:str) -> None:
        score = content.find("span", id="scan-score")
        input(score.text)
if __name__ == "__main__":
    init = Main()
    init.start 