import json
import numpy as np

# Opening JSON files
f = open('../data/openings_avg.json')
openings_avg = json.load(f)
f.close()

f = open('../data/openings.json')
openings = json.load(f)
f.close()

openings_avg_values = openings_avg.values()
avg_num_moves = sum(openings_avg_values)/len(openings_avg_values)
sd_num_moves = np.std(np.fromiter(openings_avg_values, dtype=float))

cumulative_stats = {}
cumulative_stats["avg_mov_num"] = avg_num_moves
cumulative_stats["sd_mov_num"] = sd_num_moves

# get min opening, avg move num, and sample size
min_opening = ""
cur_min = 999999
for (key, value) in openings_avg.items():
    if openings[key][0] > 1000 and value < cur_min:
        min_opening = key
        cur_min = value
min_opening_samples = openings[min_opening][0] # value of openings dict is an array, first value being the number of games sampled
min_avg = openings_avg[min(openings_avg, key=openings_avg.get)]
cumulative_stats.update({
    "min_opening": min_opening,
    "min_opening_samples": min_opening_samples,
    "min_mov_num": min_avg
})

# get max opening
max_opening = ""
cur_max = 0
for (key, value) in openings_avg.items():
    if openings[key][0] > 1000 and value > cur_max:
        max_opening = key
        cur_max = value
max_opening_samples = openings[max_opening][0] # value of openings dict is an array, first value being the number of games sampled
max_avg = openings_avg[max(openings_avg, key=openings_avg.get)]
cumulative_stats.update({
    "max_opening": max_opening,
    "max_opening_samples": max_opening_samples,
    "max_mov_num": max_avg
})

# determine if max and min values are statistically significant with the bootstrap
# need to get move lengths of the max and min into a data vector

minmax_opening_lengths = {max_opening: [], min_opening: []}

f = open("C:/Users/Michael Cleversley/Downloads/lichess_data/apr18.pgn")
line = f.readline()
current_opening = ""
current_termination = ""
while line:
    if line == "\n": # skip blank lines
        line = f.readline()
        continue
    if "Opening" in line:
        # print(line)
        line = line.replace("\"", "").replace("]", "").replace("\n", "")
        space_i = line.index(" ")
        colon_i = line.find(":") if line.find(":") != -1 else 100000 # returns -1 if not found, change to high number to
        comma_i = line.find(",") if line.find(",") != -1 else 100000
        pound_i = line.find("#") if line.find("#") != -1 else 100000
        current_opening = line[space_i:min(colon_i, comma_i, pound_i)].strip()
    if "Termination" in line:
        line = line.replace("\"", "").replace("]", "").replace("\n", "")
        current_termination = line.split(" ")[1]
        print(current_termination)
    if (current_opening == max_opening or current_opening == min_opening) and current_termination != "Abandoned" and line[0] == "1":
        line = line.rstrip().replace(".", "")
        line = line.split(" ")
        num_moves = -1
        for unit in reversed(line):
            if unit.isdigit():
                num_moves = int(unit)
                break
        minmax_opening_lengths[current_opening].append(num_moves)
    
    line = f.readline()

with open('../data/cumulative_stats.json', 'w') as convert_file:
    convert_file.write(json.dumps(cumulative_stats))

with open('../data/minmax_opening_lengths.json', 'w') as convert_file:
    convert_file.write(json.dumps(minmax_opening_lengths))