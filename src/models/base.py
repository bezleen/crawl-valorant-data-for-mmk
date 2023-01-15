import sys
sys.path.insert(0, '.')


import time
import json
from csv import DictWriter, writer
from os.path import exists

import pydash as py_
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


import src.config as Conf
import src.url_config as URLConf


class ValorantCrawl(object):
    def __init__(self):
        self.service = Service(executable_path="chrome_drivers/chromedriver")
        self.driver = webdriver.Chrome(service=self.service)

    # def crawl_by_rank(self):
    #     with open('data/urls.json', 'r') as f:
    #         dict_urls = json.loads(f.read())
    #     for rank in list(dict_urls.keys()):
    #         print(rank)
    #         label = py_.get(Conf.LABEL_MAPPING, f"{rank}")
    #         rank_urls = py_.get(dict_urls, f"{rank}")
    #         for index, value in rank_urls.items():
    #             print(f"Crawling rank: {label}-{rank}, index={index}, value={value}")
    #             self.exec_crawl(value)
    #     return
    def crawl_default(self, from_index=None):
        with open('data/urls.json', 'r') as f:
            dict_urls = json.loads(f.read())
        new_dict_urls = dict_urls
        if isinstance(dict_urls, list):
            new_dict_urls = {}
            for index, value in enumerate(dict_urls):
                py_.set_(new_dict_urls, f"{index}", value)
        if from_index:
            for index in range(from_index, len(list(new_dict_urls.keys()))):
                value = py_.get(new_dict_urls, f"{index}")
                print(f"Crawling index={index}, value={value}")
                self.exec_crawl(value)
            return
        for index, value in new_dict_urls.items():
            print(f"Crawling index={index}, value={value}")
            try:
                self.exec_crawl(value)
            except:
                self.write_error_url(value)
        return

    def write_error_url(self, url):
        with open('data/error_url.txt', 'a') as f:
            f.writelines(f"{url},")

    def exec_crawl(self, url):
        self.driver.get(url)
        time.sleep(2)

        # get table
        table_datas = self.driver.find_elements(By.CSS_SELECTOR, ".infinite-table> div:nth-child(2) > div > div")
        # print(table)
        # table_datas = table.find_elements(By.CSS_SELECTOR, "div:nth-child(2) > div")
        len_rows = len(table_datas)
        if len_rows < 2:
            self.write_error_url(url)
            return
        # print(len_rows)
        for row in range(1, len_rows + 1):
            # print(row)
            kd = self.driver.find_element(By.CSS_SELECTOR, f".infinite-table > div:nth-child(2) > div>div:nth-child({row}) >div:nth-child(3) > span").get_attribute("innerHTML")
            kill = self.driver.find_element(By.CSS_SELECTOR,
                                            f".infinite-table > div:nth-child(2) > div>div:nth-child({row}) >div:nth-child(4)> div > span:nth-child(1)").get_attribute("innerHTML")
            death = self.driver.find_element(By.CSS_SELECTOR,
                                             f".infinite-table > div:nth-child(2) > div>div:nth-child({row}) >div:nth-child(4)> div > span:nth-child(3)").get_attribute("innerHTML")
            assistant = self.driver.find_element(
                By.CSS_SELECTOR, f".infinite-table > div:nth-child(2) > div>div:nth-child({row}) >div:nth-child(4)> div > span:nth-child(5)").get_attribute("innerHTML")
            win_rate = self.driver.find_element(By.CSS_SELECTOR, f".infinite-table > div:nth-child(2) > div>div:nth-child({row}) >div:nth-child(5) > p").get_attribute("innerHTML")[:-1]
            pick_rate = self.driver.find_element(By.CSS_SELECTOR, f".infinite-table > div:nth-child(2) > div>div:nth-child({row}) >div:nth-child(6) > span").get_attribute("innerHTML")[:-1]
            avg_score = self.driver.find_element(By.CSS_SELECTOR, f".infinite-table > div:nth-child(2) > div>div:nth-child({row}) >div:nth-child(7) > p").get_attribute("innerHTML")
            first_blood_rate = self.driver.find_element(
                By.CSS_SELECTOR, f".infinite-table > div:nth-child(2) > div>div:nth-child({row}) >div:nth-child(8) > span").get_attribute("innerHTML")[:-1]

            kd = float(kd.replace(" ", ""))
            kill = float(kill.replace(" ", ""))
            death = float(death.replace(" ", ""))
            assistant = float(assistant.replace(" ", ""))
            win_rate = float(win_rate.replace(" ", ""))
            pick_rate = float(pick_rate.replace(" ", ""))
            avg_score = float(avg_score.replace(" ", ""))
            first_blood_rate = float(first_blood_rate.replace(" ", ""))

            data = {
                "KD": kd,
                "Kill": kill,
                "Death": death,
                "Assistant": assistant,
                "WinRate": win_rate,
                "PickRate": pick_rate,
                "AvgScore": avg_score,
                "FirstBloodRate": first_blood_rate
            }
            file_path = 'data/valorant_mmk.csv'
            if not exists(file_path):
                with open(file_path, 'a') as f:
                    writer_obj = writer(f)
                    writer_obj.writerow(list(data.keys()))
                    f.close()
            with open(file_path, 'a') as f:
                dictwriter_obj = DictWriter(f, fieldnames=list(data.keys()))
                dictwriter_obj.writerow(data)
                f.close()
        return
