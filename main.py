import time
import json
import requests
import codecs

url = "https://posroi.ostgotatrafiken.se/posroi/get"


def read_data_point(file, csv=False):
    resp = requests.get(url)
    data_list = json.loads(resp.content)

    if csv:

        chunks = [data_list[i:i + 12] for i in range(0, len(data_list), 12)]
        for chunk in chunks:
            file.write(",".join(str(x).strip(" ").replace(",", "") for x in chunk) + "\n")
    else:
        file.write(str(time.time()) + ";" + ";".join(str(x).strip(" ") for x in data_list) + "\n")


if __name__ == '__main__':
    with codecs.open("data2.log", "a+", "utf-8") as f:
        while True:
            read_data_point(f, csv=True)
            time.sleep(1)
            f.flush()
