import codecs
import json
import datetime

db = {}


class DataPoint:
    def __init__(self, time, data):
        # 201;1;201;127;48;1236;Rusthållaregården;Nästa;58.42268;15.59134;200;None
        #  1;2;  3;  4; 5;   6;                7;    8;       9;      10; 11;  12
        self.time = time
        self.line_type = data[0]  # Eg. 201 when line 1
        self.line = data[1]
        if self.line_type != data[2]:
            raise ImportError("Odd data format, expected " + data[0] + " to be equal to " + data[2] + ".")
        self.d = data[3]  # This could be 'bus id' (most likely, but there seem to be multiple busses with the same id?)
        self.e = data[4]  # This seems to change randomly?
        self.stop_id = data[5]
        self.stop = data[6]
        self.eta = data[7]
        self.lat = data[8]
        self.long = data[9]
        self.angle = data[10]
        self.type = data[11]

    def get_key(self):
        return self.d

    def __str__(self):
        return json.dumps({"time": self.time,
                           "line": self.line,
                           "line type": self.line_type,
                           "stop": self.stop,
                           "eta": self.eta,
                           "lat": self.lat,
                           "long": self.long,
                           "type": self.type,
                           "d": self.d,
                           "e": self.e,
                           "stop id": self.stop_id,
                           "angle": self.angle,
                           }, indent=4, ensure_ascii=False)


def clock(data_point):
    return datetime.datetime.fromtimestamp(float(data_point.time)).strftime('%Y-%m-%d %H:%M:%S')

def read_line(file):
    file.readline()


def read_file(filename):
    with codecs.open(filename, "r", "utf-8") as file:
        while True:
            line = file.readline()
            if line is None or len(line) == 0:
                break
            data = line.split(";")
            time = data[0]
            data = data[1:]

            while len(data) > 12:
                sd = data[0:12]
                dp = DataPoint(time, sd)
                key = dp.get_key()
                if key not in db:
                    db[key] = []
                db[key].append(dp)
                data = data[12:]


if __name__ == '__main__':
    read_file("data.log")
    try:
        x = []
        for dp in db["92888"]:
            if len(x) == 0 or x[-1] != (dp.line, dp.stop):
                x.append(clock(dp), dp.line, dp.stop)
        print(x)
    except KeyError:
        print("Problem! Valid keys: " + ", ".join(sorted(db)))

    if True:
        for key in db:
            stopset = set()
            for dp in db[key]:
                stopset.add(dp.line)
            print(key + " " + ", ".join(stopset))
