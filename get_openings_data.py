# Calculate average number of moves per opening

from ctypes import pointer
import json

f = open("C:/Users/Michael Cleversley/Downloads/lichess_data/apr18.pgn")
line = f.readline()
openings = {} # will map openings to a tuple of (times_found, total_moves)
current_opening = ""
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
  if line[0] == "1":
    line = line.rstrip().replace(".", "")
    line = line.split(" ")
    num_moves = -1
    for unit in reversed(line):
      if unit.isdigit():
        num_moves = int(unit)
        break
    if current_opening in openings:
      openings[current_opening][0] += 1
      openings[current_opening][1] += num_moves
    else:
      openings[current_opening] = [1, num_moves]

  line = f.readline()

openings_to_avg = {opening: nums[1]/nums[0] for (opening, nums) in openings.items()}

with open('openings.json', 'w') as convert_file:
  convert_file.write(json.dumps(openings))

with open('openings_avg.json', 'w') as convert_file:
  convert_file.write(json.dumps(openings_to_avg))

print(openings_to_avg["Center Game"])