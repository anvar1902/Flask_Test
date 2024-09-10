import datetime
import random
import time
time_data = 0
for i in range(100):
    hypr_dict = {}
    for i in range(1, 13):
        for j in range(1, 29):
            for k in range(24):
                for v in range(60):
                    hypr_dict[str(datetime.datetime(2020, i, j, k, v))] = random.randint(0, 100000)

    start = time.time()
    print("Start")

    def check(year, month, day, hour):
        sum = 0
        c = 0
        for k, v in hypr_dict.items():
            if f'{year}-{month}-{day} {hour}' in k.lower():
                c += 1
                sum += v
        if sum != 0 and c != 0:
            sum = sum / c
            print(sum)

    hashrate_data = {}
    for k, v in hypr_dict.items():
        if k[:-6] in hashrate_data:
            hashrate_data[k[:-6]][0] = hashrate_data[k[:-6]][0] + 1
            hashrate_data[k[:-6]][1] = hashrate_data[k[:-6]][1] + v
        else:
            hashrate_data[k[:-6]] = [1, v]

    hashrate_sorted_data = {}
    for k, v in hashrate_data.items():
        hashrate_sorted_data[k] = v[1] // v[0]
    print(hashrate_sorted_data)

    stop = time.time()
    time_data += stop-start
print(time_data)