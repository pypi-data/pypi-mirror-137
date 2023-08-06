
import os

validity = []
for i in range(100):
    print(i)
    out_dist = False
    in_dist = False
    joint_dist = False
    out_samples = []
    in_samples = []
    joint_samples = []
    with open(os.path.join('models', 'bench', 'distributions', 'bench_' + str(i) + '.csv')) as dl:
        for line in dl:
            if joint_dist:
                if line.strip():
                    joint_samples.append((int(line.split(',')[0]), int(line.split(',')[1].strip())))
            if line[:-1] == 'joint distribution':
                out_dist = False
                in_dist = False
                joint_dist = True
            if in_dist:
                if line.strip():
                    in_samples.append((int(line.split(',')[0]), int(line.split(',')[1].strip())))
            if line[:-1] == 'in distribution':
                out_dist = False
                in_dist = True
                joint_dist = False
            if out_dist:
                if line.strip():
                    out_samples.append((int(line.split(',')[0]), int(line.split(',')[1].strip())))
            if line[:-1] == 'out distribution':
                out_dist = True
                in_dist = False
                joint_dist = False

    species = []
    reactions = []
    with open(os.path.join('models', 'bench', 'antimony', 'bench_' + str(i) + '.txt')) as ml:
        for line in ml:
            if 'var' in line:
                species.extend(line[4:-1].split(', '))
            if 'ext' in line:
                species.extend(line[4:-1].split(', '))
            if '->' in line:
                line = line.split(': ')[1].split(';')[0].split(' -> ')
                for j, each in enumerate(line):
                    line[j] = each.split(' + ')
                reactions.append(line)

    out_counts = [0 for _ in species]
    in_counts = [0 for _ in species]

    for each in reactions:
        print(each)
        if len(each[0]) == 1 and len(each[1]) == 1:
            out_counts[species.index(each[0][0])] += 1
            in_counts[species.index(each[1][0])] += 1
        if len(each[0]) == 2 and len(each[1]) == 1:
            out_counts[species.index(each[0][0])] += 1
            out_counts[species.index(each[0][1])] += 1
            in_counts[species.index(each[1][0])] += 2
        if len(each[0]) == 1 and len(each[1]) == 2:
            out_counts[species.index(each[0][0])] += 2
            in_counts[species.index(each[1][0])] += 1
            in_counts[species.index(each[1][1])] += 1
        if len(each[0]) == 2 and len(each[1]) == 2:
            out_counts[species.index(each[0][0])] += 2
            out_counts[species.index(each[0][1])] += 2
            in_counts[species.index(each[1][0])] += 2
            in_counts[species.index(each[1][1])] += 2

    match = True
    for each in out_samples:
        if out_counts.count(each[0]) != each[1]:
            match = False
    for each in in_samples:
        if in_counts.count(each[0]) != each[1]:
            match = False
    validity.append(match)

print(validity)
