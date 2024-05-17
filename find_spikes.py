import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
video_stimulus_names = ['Zolitudes_Lieta (1)','VideoMaximaRac','VideoMaximaEmo', 'Rusina_Lieta_02/ ISS','Rusina_Lieta_03 _ ISS + STUKANS','VideoJekabpilsRac', 'VideoJekabpilsEmo', 'NEO_Lieta','VideoKiberRac','VideoKiberEmo']




# Load the data from an Excel file
file_path = 'C:\\Users\\User\\Desktop\\bak program\\Joined data\\KE_6\\joined_data_68.xlsx'
df = pd.read_excel(file_path)
filtered_df = df[df['Presented Stimulus name'].isin(video_stimulus_names)]
# Apply a moving average to smooth the data
window_size = 60  # Adjust window size as needed
filtered_df['smoothed_value'] = filtered_df['Shimmer_F562_GSR_Skin_Resistance_CAL'].rolling(window=window_size).mean()

# Find peaks (spikes)
peaks, _ = find_peaks(filtered_df['smoothed_value'], distance=window_size, prominence=5)

# Find troughs (drops) by inverting the signal
troughs, _ = find_peaks(-filtered_df['smoothed_value'], distance=window_size, prominence=5)

# Combine peaks and troughs
all_spikes = np.concatenate((peaks, troughs))
all_spikes.sort()

# Filter out rows with spikes
spikes = filtered_df.iloc[all_spikes]

# def merge_close_spikes(spikes, range_size):
#     merged_spikes = []
#     current_max_index = spikes[0]

#     for i in range(1, len(spikes)):
#         if spikes[i] - current_max_index < range_size:
#             if filtered_df['smoothed_value'].iloc[spikes[i]] > filtered_df['smoothed_value'].iloc[current_max_index]:
#                 current_max_index = spikes[i]
#         else:
#             merged_spikes.append(current_max_index)
#             current_max_index = spikes[i]

#     merged_spikes.append(current_max_index)
#     return merged_spikes

# range_size = 60  # Adjust the range size as needed
# merged_spikes = merge_close_spikes(all_spikes, range_size)

# # Filter out rows with spikes
# spikes = filtered_df.iloc[merged_spikes]

# Plot the original data and the detected spikes
plt.figure(figsize=(20, 6))
plt.plot(filtered_df['Shimmer_F562_TimestampSync_FormattedUnix_CAL'], filtered_df['smoothed_value'], label='Smoothed Value', color='orange')
plt.scatter(spikes['Shimmer_F562_TimestampSync_FormattedUnix_CAL'], spikes['smoothed_value'], color='red', label='Spikes and Drops')
plt.xlabel('Timestamp')
plt.ylabel('Value')
plt.legend()
plt.show()

# Save the result to a new Excel file
output_file_path = 'spikes_and_drops_detected.xlsx'
df.to_excel(output_file_path, index=False)





