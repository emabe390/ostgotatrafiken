import time
import json
import requests
import codecs

url = "https://posroi.ostgotatrafiken.se/posroi/get"


def read_data_point(file):
    resp = requests.get(url)
    data_list = json.loads(resp.content)
    file.write(str(time.time()) + ";" + ";".join(str(x).strip(" ") for x in data_list) + "\n")


if __name__ == '__main__':
    with codecs.open("data.log", "a+", "utf-8") as f:
        while True:
            read_data_point(f)
            time.sleep(10)
            f.flush()
