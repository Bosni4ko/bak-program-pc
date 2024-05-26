import pandas as pd
import matplotlib.pyplot as plt
import os

#Shimmer file path and participant ids
shimmer_base_path = 'Shimmer ieraksti\\KE_'
shimmer_base_path_2 = '\\KE_'
participant_id_start = 3
participant_id_end = 16
shimmer_file_template = '_Session1_Shimmer_F562_Calibrated_PC'
shimmer_file_extension = '.csv'

#Joined data path and file ids
joined_data_base_path = 'Joined data\\KE_'
write_folder = '\\Graphs'
shimmer_write_file_template = '\\Shimmer_graph_KE'
graph_extension = '.png'
start_file = 46
end_file = 87


# Format x-axis labels as minutes and seconds
def format_func(value, tick_number ):
    # Convert value (minutes) to an integer number of seconds
    seconds = int(value * 60)
    minutes = seconds // 60
    seconds = seconds % 60
    return f'{minutes}:{seconds:02d}'

def plot_shimmer_data(write_path,df, timestamps, conductance,window_size):
    # Plotting the data
    window_size_seconds = 8  # 4 seconds before and 4 seconds after
    sample_rate = 120 #Sample rate of 120HZ
    #Calculate average conductance and phasic conductance
    mean_conductance = conductance.rolling(window=window_size, center=True).mean()
    median_gsr = mean_conductance.rolling(window=int(window_size_seconds * sample_rate), center=True, min_periods=1).median()
    adjusted_conductance = mean_conductance - median_gsr
    #Plot the data
    plt.figure(figsize=(40, 10))
    plt.plot(time_since_start_seconds, mean_conductance, label='Original Skin Conductance', color='blue', linewidth=1)
    plt.plot(time_since_start_seconds, adjusted_conductance, label='Phasic Skin Conductance', color='red', linewidth=1)
    plt.title('Skin Conductance  Over Time')
    plt.xlabel('Time Since Start (minutes)')
    plt.ylabel('Conductance (uS)')
    plt.grid(True)
    plt.legend()
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(format_func))
    plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
    plt.tight_layout()  # Adjust layout to make room for rotated labels
    plt.savefig(write_path)  # Saves the plot as a PNG file
    plt.close()  # Close the plot figure to free up memory    

#Process each participant file
for participant_id in range(participant_id_start, participant_id_end + 1):
    #Get file path
    filepath = shimmer_base_path + str(participant_id) + shimmer_base_path_2 + str(participant_id) + shimmer_file_template + shimmer_file_extension
    if os.path.exists(filepath):  
        # Open the file and read the first line to find the separator
        shimmer_df = pd.read_csv(filepath,sep='\t',skiprows=1)
        shimmer_df = shimmer_df.drop([0, 1]).reset_index(drop=True)

        # Extract and convert timestamps
        timestamps = pd.to_datetime(shimmer_df['Shimmer_F562_TimestampSync_FormattedUnix_CAL'], format='%Y/%m/%d %H:%M:%S.%f')
        # Calculate time since the first conductance value
        time_since_start = timestamps - timestamps.iloc[0]
        # Convert time since start to total seconds
        time_since_start_seconds = time_since_start.dt.total_seconds() / 60  # convert to minutes

        # Extract and convert conductance values
        conductance = pd.to_numeric(shimmer_df['Shimmer_F562_GSR_Skin_Conductance_CAL'], errors='coerce')
        if not os.path.exists(shimmer_base_path + str(participant_id)):
            continue
        if not os.path.exists(joined_data_base_path + str(participant_id) + write_folder):
            os.mkdir(joined_data_base_path + str(participant_id) + write_folder)
        #Save graph
        write_path = joined_data_base_path + str(participant_id) + write_folder + shimmer_write_file_template + str(participant_id) + graph_extension
        plot_shimmer_data(write_path,shimmer_df,timestamps,conductance,window_size = 60)