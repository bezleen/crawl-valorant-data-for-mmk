import sys
sys.path.insert(0, '.')

import copy
import json
import pydash as py_

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


if __name__ == '__main__':
    # generate_url()
    generate_url_new()
