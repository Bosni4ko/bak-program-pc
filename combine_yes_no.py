import pandas as pd
import matplotlib.pyplot as plt

#This program make a conductance and phasic conductance graphs of each participant during Yes/No survey

# Load the survey data
survey_file = 'Ja_Ne anketa_QuestionPro-SR-RawData-12146557-05-14-2024-T041833.163.xlsx'
survey_data = pd.read_excel(survey_file, sheet_name='Raw Data')

# Extract columns with participant code, starting timestamp and question numbers
participant_code_col = 'Dalībnieka kods (ievada eksperimenta vadītājs)'
timestamp_col = 'Timestamp (mm/dd/yyyy)'
question_cols = [str(i) for i in range(1, 16)]  # Columns '1', '2', ..., '15'

# Function to read participant shimmer data
def load_participant_data(participant_name):
    participant_file = f'Shimmer ieraksti/{participant_name}/{participant_name}_Session1_Shimmer_F562_Calibrated_PC.csv'
    participant_data = pd.read_csv(participant_file,sep='\t',skiprows=1)
    participant_data = participant_data.drop([0, 1]).reset_index(drop=True)
    return participant_data

#Function to handle different time format
def parse_time_flexibly(time_str):
    try:
        return pd.to_datetime(time_str, format='%Y/%m/%d %H:%M:%S.%f').time()
    except ValueError:
        return pd.to_datetime(time_str, format='%Y/%m/%d %H:%M:%S').time()
    
# Function to plot skin conductance during survey
def plot_skin_conductance(participant_name, participant_data,survey_start_time,question_timestamps):
    #Load timestamps and conductance
    timestamps = pd.to_datetime(participant_data['Shimmer_F562_TimestampSync_FormattedUnix_CAL'], format='%Y/%m/%d %H:%M:%S.%f')
    conductance = pd.to_numeric(participant_data['Shimmer_F562_GSR_Skin_Conductance_CAL'], errors='coerce')
    #Calculate average conductance with window 15 for better vizualasation 
    mean_conductance = conductance.rolling(window=15, center=True).mean()

    window_size_seconds = 8  # 4 seconds before and 4 seconds after
    sample_rate = 120
    median_gsr = mean_conductance.rolling(window=int(window_size_seconds * sample_rate), center=True, min_periods=1).median()
    # Subtract median GSR from conductance to get phasic conductance
    adjusted_conductance = mean_conductance - median_gsr

    #Filtere data relevant for survey using mask
    mask = timestamps.dt.time >= survey_start_time.time()
    filtered_timestamps = timestamps[mask]
    filtered_conductance = mean_conductance[mask]
    filtered_adjusted_conductance = adjusted_conductance[mask]

    
    # Plot the skin conductance data
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(40, 10))
    ax1.plot(filtered_timestamps, filtered_conductance, label='Skin Conductance')
    # Draw vertical lines and write question names
    for qt, question_name in zip(question_timestamps, question_cols):
        qt_time = pd.to_datetime(qt,format='%m/%d/%Y %H:%M:%S.%f').time()
        # Combine the date from the first timestamp with the question time
        qt_full_timestamp = pd.to_datetime(filtered_timestamps.dt.date.min()) + pd.to_timedelta(f"{qt_time.hour}:{qt_time.minute}:{qt_time.second}.{qt_time.microsecond}")
        ax1.axvline(x=qt_full_timestamp, color='purple', linestyle='--')
        ax1.text(qt_full_timestamp, filtered_conductance.max() * 0.95, f'Q{question_name}', rotation=90, verticalalignment='bottom', color='purple')
        ax2.axvline(x=qt_full_timestamp, color='purple', linestyle='--')

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Skin Conductance (µS)')
    ax1.set_title(f'Skin Conductance for Participant {participant_name} During Survey')
    ax1.legend()
    ax1.grid(True)

    ax2.plot(filtered_timestamps, filtered_adjusted_conductance, label='Phasic Skin Conductance',color='red')
    ax2.axhline(y=0, color='black', linewidth=2)  # Bold horizontal line at y = 0
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Skin Conductance (µS)')
    ax2.legend()
    ax2.grid(True)
    output_file = 'yes_no_graphs\\Skin_Conductance_' + participant_name + '_Survey.png'
    plt.savefig(output_file)
    plt.close(fig)  # Close the figure to free memory

# Process each participant in the survey data
for idx, row in survey_data.iterrows():
    #Get participant name, start time and question timestamps
    participant_name = row[participant_code_col]
    survey_start_time = pd.to_datetime(row[timestamp_col], format='%Y/%m/%d %H:%M:%S.%f')
    question_timestamps = [row[col] for col in question_cols if not pd.isna(row[col])]
    
    try:
        participant_data = load_participant_data(participant_name)
        plot_skin_conductance(participant_name, participant_data,survey_start_time,question_timestamps)
    except FileNotFoundError:
        print(f"Data file for participant {participant_name} not found.")


