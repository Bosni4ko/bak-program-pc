import pandas as pd
import numpy as np
import os
#Program finds minimal, maximal, average and median values for skin conductance, resistnace and ppg recordings 

#Define joined data path
base_path = 'Joined data\\KE_'
file_template = '\\joined_data_'
file_extension = '.xlsx'
#Participant id's
participant_id_start = 13
participant_id_end = 13
#File id's
start_file = 117
end_file = 117
files_per_participant = 1


video_stimulus_names = ['Zolitudes_Lieta (1)','VideoMaximaRac','VideoMaximaEmo', 'Rusina_Lieta_02/ ISS','Rusina_Lieta_03 _ ISS + STUKANS','VideoJekabpilsRac', 'VideoJekabpilsEmo', 'NEO_Lieta','VideoKiberRac','VideoKiberEmo']

#Process joined data file
def process_file(filepath):
    # Load the Excel file
    df = pd.read_excel(filepath)

    # get participant name
    participant_name = df['Participant name'].iloc[0]
    #Filtere data to get only data where stimulus is presented
    filtered_df = df[df['Presented Stimulus name'].isin(video_stimulus_names)]
    #Get sitmulus name
    if not filtered_df.empty:
        video_stimulus_name = filtered_df['Presented Stimulus name'].iloc[0]
    else:
        video_stimulus_name = 'empty'

    # Create a summary dictionary with median, mean, min, max values for conductance resistnac enad ppg
    summary = {
        'Participant name': participant_name,
        'Video stimulus name': video_stimulus_name,
        'Min_Skin_Conductance': df['Shimmer_F562_GSR_Skin_Conductance_CAL'].min(),
        'Max_Skin_Conductance': df['Shimmer_F562_GSR_Skin_Conductance_CAL'].max(),
        'Mean_Skin_Conductance': df['Shimmer_F562_GSR_Skin_Conductance_CAL'].mean(),
        'Median_Skin_Conductance': df['Shimmer_F562_GSR_Skin_Conductance_CAL'].median(),
        'Min_Skin_Resistance': df['Shimmer_F562_GSR_Skin_Resistance_CAL'].min(),
        'Max_Skin_Resistance': df['Shimmer_F562_GSR_Skin_Resistance_CAL'].max(),
        'Mean_Skin_Resistance': df['Shimmer_F562_GSR_Skin_Resistance_CAL'].mean(),
        'Median_Skin_Resistance': df['Shimmer_F562_GSR_Skin_Resistance_CAL'].median(),
        'Min_Skin_PPG' : df[df['Shimmer_F562_PPG_A13_CAL'] != 0]['Shimmer_F562_PPG_A13_CAL'].min(),
        'Max_Skin_PPG': df['Shimmer_F562_PPG_A13_CAL'].max(),
        'Mean_Skin_PPG': df[df['Shimmer_F562_PPG_A13_CAL'] != 0]['Shimmer_F562_PPG_A13_CAL'].mean(),
        'Median_Skin_PPG': df[df['Shimmer_F562_PPG_A13_CAL'] != 0]['Shimmer_F562_PPG_A13_CAL'].median(),
    }
    return summary


file_id = start_file
#Create data frame for summary
summaries = pd.DataFrame(columns=['Participant name','Video stimulus name',
                                'Min_Skin_Conductance','Max_Skin_Conductance','Mean_Skin_Conductance','Median_Skin_Conductance',
                                'Min_Skin_Resistance','Max_Skin_Resistance','Mean_Skin_Resistance','Median_Skin_Resistance',
                                'Min_Skin_PPG','Max_Skin_PPG','Mean_Skin_PPG','Median_Skin_PPG',])
#Loop which process each participant
for participant_id in range(participant_id_start, participant_id_end + 1):
    #Loop which process each participant file
    for i in range(files_per_participant):
        #Get file path
        filepath = base_path + str(participant_id) + file_template + str(file_id) + file_extension
        #Process file if its exist and append result to summary
        if os.path.exists(filepath):  
             summary = process_file(filepath)
             summaries = summaries._append(summary,ignore_index=True)
        else:
            i = i-1
        file_id = file_id + 1
summary_df = pd.DataFrame(summaries)

#Write excel file
output_filename = 'summary.xlsx'
if os.path.exists(output_filename):
    with pd.ExcelWriter(output_filename, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
        start_row = writer.sheets['Sheet1'].max_row if 'Sheet1' in writer.sheets else 0
        summary_df.to_excel(writer, index=False, header=False, startrow=start_row)
else:
    with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
        summary_df.to_excel(writer, index=False)
