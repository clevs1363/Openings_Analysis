# Workflow 
1. get_openings_data.py processes the data file and stores the results in openings.json and openings_avg.json. 
2. interpret_openings_data.py interprets the data from (1) and stores various staistics in cumulative_stats.json. The data vectors from the openings with the smallest and largest averages are stored in minmax_opening_lengths.json.
3. calculate_bootstrap.py takes the data vectors from (2) and calculates the bootstrap.