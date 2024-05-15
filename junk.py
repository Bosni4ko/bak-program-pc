import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the data
filepath = 'C:\\Users\\User\\Desktop\\bak program\\Shimmer ieraksti\\KE_3\\KE_3_Session1_Shimmer_F562_Calibrated_PC.csv'
shimmer_df = pd.read_csv(filepath, sep='\t', skiprows=1)
shimmer_df = shimmer_df.drop([0, 1]).reset_index(drop=True)

# Extract and convert timestamps
timestamps = pd.to_datetime(shimmer_df['Shimmer_F562_TimestampSync_FormattedUnix_CAL'], format='%Y/%m/%d %H:%M:%S.%f')

# Calculate time since the first resistance value
time_since_start = timestamps - timestamps.iloc[0]

# Extract and convert resistance values
resistance = pd.to_numeric(shimmer_df['Shimmer_F562_GSR_Skin_Resistance_CAL'], errors='coerce')

# Compute rolling mean
window_size = 60
mean_resistance = resistance.rolling(window=window_size, center=True).mean()

# Convert time since start to total seconds
time_since_start_seconds = time_since_start.dt.total_seconds() / 60  # convert to minutes

# Plot
plt.figure(figsize=(20, 10))
plt.plot(time_since_start_seconds, mean_resistance, label='Skin Resistance', color='blue', linewidth=1)
plt.title('Skin Resistance Over Time')
plt.xlabel('Time Since Start (minutes)')
plt.ylabel('Resistance (kΩ)')
plt.grid(True)
plt.legend()

# Format x-axis labels as minutes and seconds
def format_func(value ):
    # Convert value (minutes) to an integer number of seconds
    seconds = int(value * 60)
    minutes = seconds // 60
    seconds = seconds % 60
    return f'{minutes}:{seconds:02d}'

plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(format_func))
plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
plt.tight_layout()  # Adjust layout to make room for rotated labels
plt.show()





