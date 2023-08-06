
import os
import glob

# dir_name = 'inPLa2_800_ma'
# dir_name = 'inPLa2_outPLa3_400_ma_5'
dir_name = 'inPLa2_outPLa3_800_ma_mp_1'
directory = os.path.join('../models', dir_name, 'antimony')
print(directory)
files = glob.glob(os.path.join(directory, '*'))

counts = []
for file in files:
    count = 0
    # print(file)
    readfile = open(file, 'r')
    lines = readfile.readlines()
    for line in lines:
        if line[0] == 'J':
            count += 1
    counts.append(count)

# for each in counts:
#     print(each)
print()
print(sum(counts)/len(counts))
