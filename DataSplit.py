import os
import re

"""
    Try to find a line which starts with "0xC0" at the beginning of source data, and delete those lines above it.
    Try to find a line which ends with "0xC0" at the bottom of source data, and delete those lines below it.
"""

# data_string = []
data_string = ""
# the index of data
index = 182
# two channels of ECG be used: 0 for respiration and ECG, 1 for two channels of ECG
Two_Channels = 1
# there is a single data at the beginning
single = 0


def get_address(data_index, channels):
    # noinspection PyGlobalUndefined
    global complement_data, final_data
    address = "D:\\My Documents\\ECG Detector Project\\data\\"
    data_file = open(os.path.join(address, ("data" + str(data_index) + ".txt")))
    resp_path = "RESP\\data"
    ecg_path = "ECG\\data"
    channels_path = "ECG\\TwoChannels\\data"
    twos_complement = "_two's complement.txt"
    dec = "_dec.txt"
    if channels:
        complement_data1 = \
            open(os.path.join(address, (channels_path + str(data_index) + "_Channel1" + twos_complement)), 'a')
        final_data1 = \
            open(os.path.join(address, (channels_path + str(data_index) + "_Channel1" + dec)), 'a')
        complement_data2 = \
            open(os.path.join(address, (channels_path + str(data_index) + "_Channel2" + twos_complement)), 'a')
        final_data2 = \
            open(os.path.join(address, (channels_path + str(data_index) + "_Channel2" + dec)), 'a')
    else:
        complement_data1 = \
            open(os.path.join(address, (resp_path + str(data_index) + twos_complement)), 'a')
        final_data1 = open(os.path.join(address, (resp_path + str(data_index) + dec)), 'a')

        complement_data2 = \
            open(os.path.join(address, (ecg_path + str(data_index) + twos_complement)), 'a')
        final_data2 = open(os.path.join(address, (ecg_path + str(data_index) + dec)), 'a')
    return data_file, complement_data1, final_data1, complement_data2, final_data2


def process_string(data, files):

    for line in files.readlines():
        string1 = line.split(":")[-1]
        string2 = string1.lower()
        string3 = string2.split("\"")
        string3 = "".join(string3)
        string4 = string3.split("\n")
        string = "".join(string4)

        data += string

    data1 = re.split("c0 c0", data)
    data_ = "".join(data1)
    return data_


def switch_form(files1, files2):
    # noinspection PyGlobalUndefined
    global result1, result2
    item = 0
    data_buf1 = []
    data_buf2 = []
    data = data_string.split(" ")
    data = "".join(data)
    data = data.split(" ")
    data = "".join(data)
    if single == 0:
        data = data[2:-2]

    length = len(data)
    while item < length:
        if single == 1:
            result1 = '0x'
            result1 = result1 + ''.join(data[item + 4])
            result1 = result1 + ''.join(data[item + 5])
            result1 = result1 + ''.join(data[item + 6])
            result1 = result1 + ''.join(data[item + 7])
            result1 = result1 + ''.join("00")

            result2 = '0x'
            result2 = result2 + ''.join(data[item])
            result2 = result2 + ''.join(data[item + 1])
            result2 = result2 + ''.join(data[item + 2])
            result2 = result2 + ''.join(data[item + 3])
            result2 = result2 + ''.join("00")
        else:
            result1 = '0x'
            result1 = result1 + ''.join(data[item])
            result1 = result1 + ''.join(data[item + 1])
            result1 = result1 + ''.join(data[item + 2])
            result1 = result1 + ''.join(data[item + 3])
            result1 = result1 + ''.join("00")

            result2 = '0x'
            result2 = result2 + ''.join(data[item + 4])
            result2 = result2 + ''.join(data[item + 5])
            result2 = result2 + ''.join(data[item + 6])
            result2 = result2 + ''.join(data[item + 7])
            result2 = result2 + ''.join("00")

        item += 8

        data_buf1.append(result1)
        data_buf2.append(result2)
        if item + 3 > length:
            break
        if item + 7 > length:
            break
        print(result1)
        print(result2)
    for item in data_buf1:
        files1.write(item)
        files1.write("\n")
    for item in data_buf2:
        files2.write(item)
        files2.write("\n")
    return data_buf1, data_buf2


def two_complement(value, bits):
    if value >= 2 ** bits:
        raise ValueError("Value: {} out of range of {}-bit value.".format(value, bits))
    else:
        return value - int((value << 1) & 2 ** bits)


def get_dec(data1, data2, file1, file2):
    for one in data1:
        res = int(one, 16)
        bits_width = 24
        r_e = two_complement(res, bits_width)
        # print(r_e)
        file1.write(str(r_e))
        file1.write("\n")
    for one in data2:
        res = int(one, 16)
        bits_width = 24
        r_e = two_complement(res, bits_width)
        # print(r_e)
        file2.write(str(r_e))
        file2.write("\n")


def get_lines(file):
    count = -1
    for count, line in enumerate(file):
        pass
    count += 1
    return count


datafile, final1, get_res1, final2, get_res2 = get_address(index, Two_Channels)
data_string = process_string(data_string, datafile)
data_result1, data_result2 = switch_form(final1, final2)
get_dec(data_result1, data_result2, get_res1, get_res2)
datafile.close()
final1.close()
get_res1.close()
final2.close()
get_res2.close()
# count_of_line = get_lines(datafile)
print("finished!")

#
#
#
'''    old version for old module.    '''
#
#
#
# import os
# import re
# # import linecache
#
# data_string = []
# channel = 1  # channel 1 for ECG, channel 2 for respiration.
# index = 152  # the index of data
# number_of_line = 10  # number of lines to be cut off. Not be used by now.
#
#
# def get_address(ch, data_index):
#     # noinspection PyGlobalUndefined
#     global complement_data, final_data
#     address = "D:\\My Documents\\ECG Detector Project\\data\\"
#     data_file = open(os.path.join(address, ("data" + str(data_index) + ".txt")))
#     if ch == 1:
#         complement_data = open(os.path.join(address, ("RESP\\data" + str(data_index) + "_two's complement.txt")), 'a')
#         final_data = open(os.path.join(address, ("RESP\\data" + str(data_index) + "_dec.txt")), 'a')
#     elif ch == 2:
#         complement_data = open(os.path.join(address, ("ECG\\data" + str(data_index) + "_two's complement.txt")), 'a')
#         final_data = open(os.path.join(address, ("ECG\\data" + str(data_index) + "_dec.txt")), 'a')
#     return data_file, complement_data, final_data
#
#
# def process_string(data, files):
#     for line in files.readlines():
#         # for num in range(count_of_line):
#         # print(line)
#         string1 = line.split(":")[-1]
#         # string1 = linecache.getline(files, num + 1).split(":")[-1]
#         # print(string1)
#         # string2 = string1.split("C0 C0 00 00")
#         string2 = re.split("C[0246E] C[0246E] [0246E]0 00", string1)
#         string3 = "".join(string2)
#         string3 = re.split(r"\"C[02] [0246E]0 00 ", string3)
#         string3 = "".join(string3)
#         # string3 = string3.split((" C[02]" + "\""))[0]
#         string3 = string3[1: -5]
#         string3 = "".join(string3)
#         string4 = string3.lower()
#         # string4 = string3.split("\"")[-1]
#         length = len(string4)
#         # print(length)
#
#         # string_a = string_a.split(" ", 1)[1]  # 1
#         # string_b = string_b.split(" ", 1)[0]  # 2
#         # print(string_a)
#         if length == 36:
#             string_a = string4.split("  ")[0]
#             string_b = string4.split("  ")[1]
#             data.append(string_a)
#             data.append(string_b)
#         else:
#             string_a = string4.split("  ")[0]
#             data.append(string_a)
#     return data
#
#
# def switch_form(channels, files):
#     # noinspection PyGlobalUndefined
#     global result
#     data_buf = []
#     for lines in data_string:
#         string_ = lines.split(" ")
#         if channels == 1:
#             result = '0x'
#             result = result + ''.join(string_[-6])
#             result = result + ''.join(string_[-5])
#             result = result + ''.join("00")
#
#         if channels == 2:
#             result = '0x'
#             result = result + ''.join(string_[-3])
#             result = result + ''.join(string_[-2])
#             result = result + ''.join("00")
#
#         data_buf.append(result)
#         # print(result)
#     for item in data_buf:
#         files.write(item)
#         files.write("\n")
#     return data_buf
#
#
# def two_complement(value, bits):
#     if value >= 2 ** bits:
#         raise ValueError("Value: {} out of range of {}-bit value.".format(value, bits))
#     else:
#         return value - int((value << 1) & 2 ** bits)
#
#
# def get_dec(data, file):
#     for one in data:
#         res = int(one, 16)
#         bits_width = 24
#         r_e = two_complement(res, bits_width)
#         # print(r_e)
#         file.write(str(r_e))
#         file.write("\n")
#
#
# def get_lines(file):
#     count = -1
#     for count, line in enumerate(file):
#         pass
#     count += 1
#     return count
#
#
# datafile, final, get_res = get_address(channel, index)
# # count_of_line = get_lines(datafile)
# data_string = process_string(data_string, datafile)
# data_result = switch_form(channel, final)
# get_dec(data_result, get_res)
# datafile.close()
# final.close()
# get_res.close()
# print("finished!")
