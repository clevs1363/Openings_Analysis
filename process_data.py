def process_metadata():
  return

def process_game():
  return

f = open("sample_data.pgn")
line = f.readline()
results = [0, 0, 0]
while line:
  if line == "\n": # skip blank lines
    line = f.readline()
    continue
  line = line.rstrip()[1:-1].replace("\"", "") # remove quotes and start and end brackets
  line_kv = line.split(" ")
  if line_kv[0] == "Result":
    result = line_kv[1].split("-")
    if "1/2" in result: # handle draws
      results[2] += 1
    else:
      results[0] += float(result[0])
      results[1] += float(result[1])
  line = f.readline()

print(results)
percentage = round(results[0] / sum(results), 4) * 100 # white victories
print("Desired result occurred " + str(percentage) + "% of the time")