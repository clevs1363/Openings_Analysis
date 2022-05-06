from scipy.stats import bootstrap, norm
import json
import numpy as np
import random

f = open('../data/cumulative_stats.json')
cumulative_stats = json.load(f)
f.close()

f = open('../data/minmax_opening_lengths.json')
minmax_opening_lengths = json.load(f)
f.close()

inference_stats = {} # stats to store

min_opening_name = cumulative_stats["min_opening"]
max_opening_name = cumulative_stats["max_opening"]

min_opening_data = np.asarray(minmax_opening_lengths[min_opening_name])
max_opening_data = np.asarray(minmax_opening_lengths[max_opening_name])

#-- calculate 95% confidence intervals --#
min_ci = bootstrap((min_opening_data,), np.average, confidence_level=0.95).confidence_interval
max_ci = bootstrap((max_opening_data,), np.average, confidence_level=0.95).confidence_interval

inference_stats.update({
    "min_ci": min_ci,
    "max_ci": max_ci
})

# calculate p-values
n_trials = 1000
ci_contains_true_min_avg = 0
ci_contains_true_max_avg = 0
rng = np.random.default_rng()

true_min_avg = cumulative_stats["avg_mov_num"]
true_max_avg = cumulative_stats["avg_mov_num"]

for i in range(n_trials):
    min_data = random.choices(min_opening_data, k=min(cumulative_stats["min_opening_samples"], 1000)) # sample with replacement
    max_data = random.choices(max_opening_data, k=cumulative_stats["max_opening_samples"]) # sample with replacement

    min_ci = bootstrap((min_data,), np.average, confidence_level=0.95, n_resamples=100, random_state=rng).confidence_interval
    max_ci = bootstrap((max_data,), np.average, confidence_level=0.95, n_resamples=100, random_state=rng).confidence_interval

    if min_ci[0] < true_min_avg < min_ci[1]:
       ci_contains_true_min_avg += 1

    if max_ci[0] < true_max_avg < max_ci[1]:
       ci_contains_true_max_avg += 1

# get p-values
min_pvalue = ci_contains_true_min_avg/1000
max_pvalue = ci_contains_true_max_avg/1000

inference_stats.update({
    "min_pvalue": min_pvalue,
    "max_pvalue": max_pvalue
})

print("Minimum p-value: " + str(min_pvalue * 100) + "%")
print("Maximum p-value: " + str(max_pvalue * 100) + "%") 

with open('../data/inference_stats.json', 'w') as convert_file:
    convert_file.write(json.dumps(inference_stats))

