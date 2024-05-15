import pandas as pd
from datetime import timedelta, datetime
import matplotlib.pyplot as plt


participant = "KE_3"
# Load the Shimmer CSV file
filename = 'Shimmer ieraksti/2024-05-07_09.54.34_KE_3_PC_Session1/KE_3_Session1_Shimmer_F562_Calibrated_PC.csv'  
shimmer_df = pd.read_csv(filename)

#Load Tobii csv files
filename = 'Tobii/Krizes_emocijas Recording46.xlsx'
tobii_df = pd.read_excel(filename)

#Get Tobii video start timestamp
event_tobii_df = tobii_df[tobii_df['Event'] == 'VideoStimulusStart']
tobii_recording_start_timestamp = datetime.strptime(tobii_df['Recording start time'].iloc[1], '%H:%M:%S.%f').time()
if not event_tobii_df.empty:
        # Convert the 'Recording timestamp' from microseconds to 'hh:mm:ss.000'
        video_start_timestamp = event_tobii_df['Recording timestamp'].apply(
            lambda x: str(timedelta(microseconds=x))[:-3]
        )
        video_start_formatted_timestamp = datetime.strptime(video_start_timestamp.iloc[0], '%H:%M:%S.%f').time()
# Convert time to timedelta since midnight
def time_to_timedelta(t):
    return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)

# Sum the two durations
gsr_video_start_timestamp = time_to_timedelta(tobii_recording_start_timestamp) + time_to_timedelta(video_start_formatted_timestamp)
print(gsr_video_start_timestamp)

# Ensure the timestamp and resistance columns are in the correct format
# Convert timestamps to string if necessary, and resistance to float
shimmer_df['Shimmer_F562_TimestampSync_FormattedUnix_CAL'] = shimmer_df['Shimmer_F562_TimestampSync_FormattedUnix_CAL'].astype(str)
shimmer_df['Shimmer_F562_GSR_Skin_Resistance_CAL'] = pd.to_numeric(shimmer_df['Shimmer_F562_GSR_Skin_Resistance_CAL'], errors='coerce')

#
# Handling any NaN values that may appear during conversion
shimmer_df.dropna(subset=['Shimmer_F562_GSR_Skin_Resistance_CAL'], inplace=True)

# Group by timestamp and calculate the average resistance for each timestamp
grouped_shimmer_df = shimmer_df.groupby('Shimmer_F562_TimestampSync_FormattedUnix_CAL')['Shimmer_F562_GSR_Skin_Resistance_CAL'].mean().reset_index()
# Selecting the required columns
timestamps = grouped_shimmer_df['Shimmer_F562_TimestampSync_FormattedUnix_CAL']
resistance = grouped_shimmer_df['Shimmer_F562_GSR_Skin_Resistance_CAL']

# Plotting the data
# plt.figure(figsize=(50, 10))
# plt.plot(timestamps, resistance, label='Skin Resistance', color='blue',linewidth=1)
# plt.title('Skin Resistance Over Time')
# plt.xlabel('Timestamp')
# plt.ylabel('Resistance (kΩ)')
# plt.grid(True)
# plt.legend()
# plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
# plt.tight_layout()  # Adjust layout to make room for rotated labels

# # Save the plot to a file instead of showing it
# plt.savefig('Average_Skin_Resistance_Over_Time.png')  # Saves the plot as a PNG file
# plt.close()  # Close the plot figure to free up memory
