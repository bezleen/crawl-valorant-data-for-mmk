import sys
sys.path.insert(0, '.')

import copy
import json
import pydash as py_
import csv
import random
from csv import DictWriter, writer
from os.path import exists

import src.url_config as URLConf
import src.config as Conf


def generate_url_new():
    base_url = copy.deepcopy(URLConf.MAIN)
    all_url = {}
    # all_url = {
    #     '<rank>': {
    #         0:"<url0>",
    #         1:"<url1>"
    #     }
    # }
    all_url_new = {}
    all_count = 0
    first_loop = True
    for rank in URLConf.RANK:
        count = 0

        for mode in URLConf.MODE:
            for map in URLConf.MAP:
                if count > 9 and first_loop == False:
                    continue

                true_url = base_url.format(mode=mode, rank=rank, map=map)
                py_.set_(all_url_new, all_count, true_url)
                count += 1
                all_count += 1
        if first_loop == True:
            first_loop = False
    with open('data/urls.json', 'w') as f:
        f.write(json.dumps(all_url_new))
    expect_length = all_count * 20
    print(f"expect length data = {expect_length}")
    return


def generate_url():
    base_url = copy.deepcopy(URLConf.MAIN)
    all_url = {}
    # all_url = {
    #     '<rank>': {
    #         0:"<url0>",
    #         1:"<url1>"
    #     }
    # }
    all_count = 0
    for rank in URLConf.RANK:
        count = 0
        for mode in URLConf.MODE:
            for map in URLConf.MAP:
                # rank = rank if mode == 'competitive' else 3
                true_url = base_url.format(mode=mode, rank=rank, map=map)
                py_.set_(all_url, f"{rank}.{count}", true_url)
                count += 1
                all_count += 1
    with open('data/urls.json', 'w') as f:
        f.write(json.dumps(all_url))
    expect_length = all_count * 20
    print(f"expect length data = {expect_length}")
    return


def new_value(value, min=0, max=None):
    # value = float(value)
    assert max
    percent = float(random.randint(5, 30))
    plus_or_minus = random.randint(0, 1)
    if plus_or_minus == 0:
        new_value = value * ((100.0 - percent) / 100.0)
        if new_value < min or new_value > max:
            new_value = value * ((100.0 + percent) / 100.0)
        return round(new_value, 3)
    new_value = value * ((100.0 + percent) / 100.0)
    if new_value < min or new_value > max:
        new_value = value * ((100.0 - percent) / 100.0)
    return round(new_value, 3)


def random_data():

    with open('data/valorant_mmk.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        count = 0
        header = True
        for row in csv_reader:
            if header:
                header = False
                continue
            print(count)
            count += 1

            kd = float(row[0])
            kill = float(row[1])
            death = float(row[2])
            assistant = float(row[3])
            win_rate = float(row[4])
            pick_rate = float(row[5])
            avg_score = float(row[6])
            first_blood_rate = float(row[7])
            #
            for _ in range(2):
                kd = new_value(kd, max=1.0)
                kill = new_value(kill, max=50)
                death = new_value(death, max=50)
                assistant = new_value(assistant, max=50)
                win_rate = new_value(win_rate, max=100)
                pick_rate = new_value(pick_rate, max=100)
                avg_score = new_value(avg_score, max=1000)
                first_blood_rate = new_value(first_blood_rate, max=10)
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
                file_path = 'data/extend_data.csv'
                if not exists(file_path):
                    with open(file_path, 'a') as f:
                        writer_obj = writer(f)
                        writer_obj.writerow(list(data.keys()))
                        f.close()
                with open(file_path, 'a') as f:
                    dictwriter_obj = DictWriter(f, fieldnames=list(data.keys()))
                    dictwriter_obj.writerow(data)
                    f.close()


def combine_csv():
    with open('data/label2.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        count = 0
        header = True
        id = 180853
        for row in csv_reader:
            if header:
                header = False
                continue
            print(count)
            count += 1
            kd = float(row[1])
            kill = float(row[2])
            death = float(row[3])
            assistant = float(row[4])
            win_rate = float(row[5])
            pick_rate = float(row[6])
            avg_score = float(row[7])
            first_blood_rate = float(row[8])
            label = int(row[9])
            data = {
                "id": id,
                "KD": kd,
                "Kill": kill,
                "Death": death,
                "Assistant": assistant,
                "WinRate": win_rate,
                "PickRate": pick_rate,
                "AvgScore": avg_score,
                "FirstBloodRate": first_blood_rate,
                "label": label
            }
            file_path = 'data/label1.csv'
            if not exists(file_path):
                with open(file_path, 'a') as f:
                    writer_obj = writer(f)
                    writer_obj.writerow(list(data.keys()))
                    f.close()
            with open(file_path, 'a') as f:
                dictwriter_obj = DictWriter(f, fieldnames=list(data.keys()))
                dictwriter_obj.writerow(data)
                f.close()
            # after append
            id += 1


if __name__ == '__main__':
    # generate_url()
    # generate_url_new()

    # random_data()
    combine_csv()
