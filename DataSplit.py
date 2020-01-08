import os
import re
# import linecache

data_string = []
# channel 1 for ECG, channel 2 for respiration.
channel = 1
# the index of data
index = 103
# number of lines to be cut off. Not be used by now.
number_of_line = 10


def get_address(ch, data_index):
    # noinspection PyGlobalUndefined
    global complement_data, final_data
    address = "D:\\My Documents\\CC2640R2F Project\\data\\"
    data_file = open(os.path.join(address, ("data" + str(data_index) + ".txt")))
    if ch == 1:
        complement_data = open(os.path.join(address, ("RESP\\data" + str(data_index) + "_two's complement.txt")), 'a')
        final_data = open(os.path.join(address, ("RESP\\data" + str(data_index) + "_dec.txt")), 'a')
    elif ch == 2:
        complement_data = open(os.path.join(address, ("ECG\\data" + str(data_index) + "_two's complement.txt")), 'a')
        final_data = open(os.path.join(address, ("ECG\\data" + str(data_index) + "_dec.txt")), 'a')
    return data_file, complement_data, final_data


def process_string(data, files):
    for line in files.readlines():
        # for num in range(count_of_line):
        # print(line)
        string1 = line.split(":")[-1]
        # string1 = linecache.getline(files, num + 1).split(":")[-1]
        # print(string1)
        # string2 = string1.split("C0 C0 00 00")
        string2 = re.split("C[0246E] C[0246E] [0246E]0 00", string1)
        string3 = "".join(string2)
        string3 = re.split(r"\"C[02] [0246E]0 00 ", string3)
        string3 = "".join(string3)
        # string3 = string3.split((" C[02]" + "\""))[0]
        string3 = string3[1: -5]
        string3 = "".join(string3)
        string4 = string3.lower()
        # string4 = string3.split("\"")[-1]
        length = len(string4)
        # print(length)

        # string_a = string_a.split(" ", 1)[1]  # 1
        # string_b = string_b.split(" ", 1)[0]  # 2
        # print(string_a)
        if length == 36:
            string_a = string4.split("  ")[0]
            string_b = string4.split("  ")[1]
            data.append(string_a)
            data.append(string_b)
        else:
            string_a = string4.split("  ")[0]
            data.append(string_a)
    return data


def switch_form(channels, files):
    # noinspection PyGlobalUndefined
    global result
    data_buf = []
    for lines in data_string:
        string_ = lines.split(" ")
        if channels == 1:
            result = '0x'
            result = result + ''.join(string_[-6])
            result = result + ''.join(string_[-5])
            result = result + ''.join("00")

        if channels == 2:
            result = '0x'
            result = result + ''.join(string_[-3])
            result = result + ''.join(string_[-2])
            result = result + ''.join("00")

        data_buf.append(result)
        # print(result)
    for item in data_buf:
        files.write(item)
        files.write("\n")
    return data_buf


def two_complement(value, bits):
    if value >= 2 ** bits:
        raise ValueError("Value: {} out of range of {}-bit value.".format(value, bits))
    else:
        return value - int((value << 1) & 2 ** bits)


def get_dec(data, file):
    for one in data:
        res = int(one, 16)
        bits_width = 24
        r_e = two_complement(res, bits_width)
        # print(r_e)
        file.write(str(r_e))
        file.write("\n")


def get_lines(file):
    count = -1
    for count, line in enumerate(file):
        pass
    count += 1
    return count


datafile, final, get_res = get_address(channel, index)
# count_of_line = get_lines(datafile)
data_string = process_string(data_string, datafile)
data_result = switch_form(channel, final)
get_dec(data_result, get_res)
datafile.close()
final.close()
get_res.close()
print("finished!")