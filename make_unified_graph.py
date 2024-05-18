import pandas as pd
import matplotlib.pyplot as plt
import os

# Define paths and file templates
joined_data_base_path = 'Joined data\\KE_'
joined_data_extension = '.xlsx'
joined_data_file_template = '\\joined_data_'
write_folder = '\\Graphs'
write_file_template = '\\Graph_KE_'
graph_extension = '.png'

excel_write_path = 'Joined data'

# Participant and file range settings
participant_id_start = 5
participant_id_end = 11
start_file = 58
end_file = 130

files_per_participant = 6
file_id = start_file

# Stimulus names
video_stimulus_names = ['Zolitudes_Lieta (1)','VideoMaximaRac','VideoMaximaEmo', 'Rusina_Lieta_02/ ISS','Rusina_Lieta_03 _ ISS + STUKANS','VideoJekabpilsRac', 'VideoJekabpilsEmo', 'NEO_Lieta','VideoKiberRac','VideoKiberEmo']
video_name = ['VID - video','VID - atbilde', 'Maxima video', 'Maxima - atbilde', 'Policija - video', 'Policija - atbilde']

# Function to plot combined data
def plot_combined_data(write_path, data_list, window_size):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(40, 10))
    num_participants = len(data_list)
    colors = plt.cm.get_cmap('hsv', num_participants)
    for idx, data in enumerate(data_list):
        timestamps, conductance, time_from_start, participant_id = data
        
        mean_conductance = conductance.rolling(window=window_size, center=True).mean()
        median_gsr = mean_conductance.rolling(window=int(8 * 120), center=True, min_periods=1).median()
        adjusted_conductance = mean_conductance - median_gsr

        ax1.plot(time_from_start, mean_conductance, label=f'KE_ {participant_id}', linewidth=1, color=colors(idx))

        ax2.plot(time_from_start, adjusted_conductance, label=f'KE_ {participant_id}', linewidth=1, color=colors(idx))
    
    # Customize plots
    ax1.set_title('Skin Conductance Over Time')
    ax1.set_xlabel('Time Since Start (minutes)')
    ax1.set_ylabel('Conductance (uS)')
    ax1.grid(True)
    ax1.legend()

    ax2.set_title('Phasic Skin Conductance Over Time')
    ax2.set_xlabel('Time Since Start (minutes)')
    ax2.set_ylabel('Conductance (uS)')
    ax2.axhline(y=0, color='black', linewidth=2)
    ax2.grid(True)
    ax2.legend()
    
    max_time = max([data[2].max() for data in data_list])
    x_ticks = [tick for tick in range(0, int(max_time) + 1, 5)]
    x_labels = [f'{int(tick // 60)}:{int(tick % 60):02d}' for tick in x_ticks]
    
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(x_labels, rotation=45)
    
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels(x_labels, rotation=45)
    
    plt.xticks(x_ticks, x_labels, rotation=45)
    plt.tight_layout()
    plt.savefig(write_path)
    plt.close()


def find_data(timeline_data,participant_id_start,participant_id_end,files_per_participant,start_file):
    file_id = start_file
    for participant_id in range(participant_id_start, participant_id_end + 1):
        i = 0
        while i < files_per_participant:
            filepath = joined_data_base_path + str(participant_id) + joined_data_file_template + str(file_id) + joined_data_extension
            if os.path.exists(filepath): 
                df = pd.read_excel(filepath)
                filtered_df = df[df['Presented Stimulus name'].isin(video_stimulus_names)]
                if not filtered_df.empty:
                    timestamps = pd.to_datetime(filtered_df['Shimmer_F562_TimestampSync_FormattedUnix_CAL'], format='%Y/%m/%d %H:%M:%S.%f')
                    conductance = pd.to_numeric(filtered_df['Shimmer_F562_GSR_Skin_Conductance_CAL'], errors='coerce')
                    time_from_start = (timestamps - timestamps.iloc[0]).dt.total_seconds()
                
                    timeline_name = filtered_df['Timeline name'].iloc[0]
                    if timeline_name in timeline_data:
                        timeline_data[timeline_name].append((timestamps, conductance, time_from_start, participant_id))
            else:
                i = i - 1
            i += 1
            file_id += 1
    return timeline_data

# Main data processing loop
timeline_data = {name: [] for name in video_name}

timeline_data = find_data(timeline_data,participant_id_start = 3, participant_id_end=3,files_per_participant=6,start_file=46)
timeline_data = find_data(timeline_data,participant_id_start = 4, participant_id_end=4,files_per_participant=6,start_file=105)
timeline_data = find_data(timeline_data,participant_id_start = 5, participant_id_end=11,files_per_participant=6,start_file=58)
timeline_data = find_data(timeline_data,participant_id_start = 12, participant_id_end=12,files_per_participant=5,start_file=100)
timeline_data = find_data(timeline_data,participant_id_start = 13, participant_id_end=16,files_per_participant=6,start_file=111)
#timeline_data = find_data(timeline_data,participant_id_start = 13, participant_id_end=13,files_per_participant=6,start_file=111)
# Save combined plots for each "Timeline name"
for timeline_name, data_list in timeline_data.items():
    if data_list:  # Only plot if there is data
        write_path = 'Joined data\\' + timeline_name + graph_extension
        plot_combined_data(write_path, data_list, window_size=30)

