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
min_boot = [0] * n_trials
max_boot = [0] * n_trials
rng = np.random.default_rng()

true_min_avg = cumulative_stats["min_mov_num"]
true_max_avg = cumulative_stats["max_mov_num"]

for i in range(n_trials):
    min_data = random.choices(min_opening_data, k=cumulative_stats["min_opening_samples"]) # sample with replacement
    max_data = random.choices(max_opening_data, k=cumulative_stats["max_opening_samples"]) # sample with replacement

    # min_ci = bootstrap((min_data,), np.average, confidence_level=0.90, n_resamples=100, random_state=rng).confidence_interval
    # max_ci = bootstrap((max_data,), np.average, confidence_level=0.90, n_resamples=100, random_state=rng).confidence_interval

    # if min_ci[0] < true_min_avg < min_ci[1]:
    #    ci_contains_true_min_avg += 1

    # if max_ci[0] < true_max_avg < max_ci[1]:
    #    ci_contains_true_max_avg += 1

    min_boot[i] = np.average(min_data)
    max_boot[i] = np.average(max_data)


# get p-values
min_dist = norm(np.average(min_boot), np.std(min_boot))
max_dist = norm(np.average(max_boot), np.std(max_boot))
min_pvalue = min_dist.cdf(true_min_avg)
max_pvalue = max_dist.cdf(true_max_avg)

inference_stats.update({
    "min_pvalue": min_pvalue,
    "max_pvalue": max_pvalue
})

print("Minimum p-value: " + str(min_pvalue * 100) + "%")
print("Maximum p-value: " + str(max_pvalue * 100) + "%")

with open('../data/inference_stats.json', 'w') as convert_file:
    convert_file.write(json.dumps(inference_stats))