# only a template for visualizing results
# have to change correspondingly

input_filename = "r3_res.log"
output_filename = "round3_result.csv"

start_line = 50006
end_line = 190006

with open(input_filename, 'r', encoding='utf-8') as infile, open(output_filename, 'w', encoding='utf-8') as outfile:
    for i, line in enumerate(infile, 1): 
        if start_line <= i <= end_line:
            outfile.write(line)
        elif i > end_line:
            break

######################################################################################################################

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

df = pd.read_csv('round3_result.csv', sep=';')
df['abs_time'] = df['timestamp']
products = df['product'].unique()
window_size = 50

plt.figure(figsize=(12, 6))

colors = cm.get_cmap('tab20', len(products))

plt.figure(figsize=(12, 6))
for i, product in enumerate(products):
    sub_df = df[df['product'] == product].sort_values(by='abs_time')
    smoothed = sub_df['profit_and_loss'].rolling(window=window_size, center=True).mean()
    plt.plot(sub_df['abs_time'], smoothed, label=product, color=colors(i))

plt.xlabel("T")
plt.ylabel("PNL")
plt.title("Round3 Result")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

