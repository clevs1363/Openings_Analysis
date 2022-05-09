from ctypes import pointer
import numpy as np
import json
import re
from sklearn.linear_model import LinearRegression
import pickle
from joblib import dump, load

def line_to_nums(line):
    # line = line.replace("{", "(").replace("}", ")")
    # moves = re.sub(r"\([^()]*\)", "", line)
    # print(moves)
    moves = line.replace("#", "").replace("+", "").replace("?", "").replace("!", "").replace("1-0", "").replace("0-1", "").replace("1/2-1/2", "").replace("\n", "").split(" ") # data looks like [1., e4, e6, 2., d4, b6]:
    # print(moves)
    converted_moves = []
    counter = 1
    for item in moves:
        if counter == 20:
            break
        converted_move = 0
        if item and "." not in item:
            # print(item)
            if "x" in item:
                if "=" in item: # fxe8=Q
                    item = "P" + item[2] + item[3]
                else:
                    item = item.replace("x", "") # exd4 -> ed4
                    if item[0] not in p2n:
                        item = "P" + item[1:]
            if "=" in item: # g=Q
                item = "P" + item[:2]
            if len(item) < 3:
                # add P for pawn
                item = "P" + item
            if item == "O-O":
                item = "Kg1"
            if item == "O-O-O":
                item = "Kc1"
            if len(item) == 4: # handles Ngf6
                item = item[:1] + item[2:]
            # print(item)
            if len(item) == 3:
                try:
                    converted_move = converted_move + p2n[item[0]] + ord(item[1]) + int(item[2])
                except:
                    pass
            # print(converted_move)
            converted_moves.append(converted_move)
            counter += 1
    if len(converted_moves) < 20:
        converted_moves = converted_moves + [0] * (20-len(converted_moves))
    return converted_moves

f = open('../data/openings_avg.json')
openings_reference = list(json.load(f).keys())
f.close()

# print(openings_reference)

p2n = {"K": 1, "Q": 9, "N": 3, "B": 3, "R": 5, "P": 1}

# openings = []
# move_data = []

# f = open("C:/Users/Michael Cleversley/Downloads/lichess_data/apr18.pgn")
# line = f.readline()
# # openings = {} # will map openings to a tuple of (times_found, total_moves)
# current_opening = ""
# while line:
#     if line == "\n": # skip blank lines
#         line = f.readline()
#         continue

#     if "Opening" in line:
#         # print(line)
#         line = line.replace("\"", "").replace("]", "").replace("\n", "")
#         space_i = line.index(" ")
#         colon_i = line.find(":") if line.find(":") != -1 else 100000 # returns -1 if not found, change to high number to
#         comma_i = line.find(",") if line.find(",") != -1 else 100000
#         pound_i = line.find("#") if line.find("#") != -1 else 100000
#         current_opening = line[space_i:min(colon_i, comma_i, pound_i)].strip()
#     if line[0] == "1" and "{" not in line:
#         converted_moves = line_to_nums(line)
#         move_data.append(converted_moves)
#         openings.append(openings_reference.index(current_opening) + 1)
    
#     line = f.readline()

# # clip openings 

# X = np.array(move_data, dtype=int)
# y = np.array(openings, dtype=int)

# reg = LinearRegression().fit(X, y)
# reg.score(X, y)

# prediction1 = reg.predict(np.array([line_to_nums("1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. c3 Nf6 5. d4 exd4 6. cxd4 Bb4")]))
# print("Actual is Ruy Lopez, index of " + str(openings_reference.index("Ruy Lopez")))
# print("Predicted is " + openings_reference[int(prediction1)] + ", index of " + str(int(prediction1)))

# dump(reg, 'lin_reg.joblib') 
reg = load('lin_reg.joblib')

prediction1 = reg.predict(np.array([line_to_nums("1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. c3 Nf6 5. d4 exd4 6. cxd4 Bb4")]))
print("Actual is Ruy Lopez, index of " + str(openings_reference.index("Ruy Lopez")))
print("Predicted is " + openings_reference[int(prediction1)] + ", index of " + str(int(prediction1)))