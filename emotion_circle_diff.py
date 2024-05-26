import pandas as pd

#This program calculates the emotin strength changes of each session since the first session

# Load the Excel file
file_path = 'Aplis_results.xlsx'  
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Extract the emotion columns
emotion_columns = df.columns[2:]

# Initialize a new DataFrame to store the changes
change_df = pd.DataFrame(columns=['participant', 'session'] + list(emotion_columns))

# Ensure session column is treated as integer
df['session'] = df['session'].astype(int)

# Function to extract the numeric part of the emotion value
def extract_emotion_strength(value):
    digits = ''.join(filter(str.isdigit, str(value)))
    return int(digits) if digits else 0

# Process each participant
for participant in df['participant'].unique():
    # Get data for the current participant
    participant_data = df[df['participant'] == participant].copy()
    
    # Get the first session data
    first_session_data = participant_data[participant_data['session'] == 1]
    
    if first_session_data.empty:
        print(f"No data for participant {participant} in session 1")
        continue

    # Since the session '1' is unique, we take the first row
    first_session_row = first_session_data.iloc[0]
    
    for _, row in participant_data.iterrows():
        if row['session'] == 1:
            continue  # Skip the first session
        
        changes = {'participant': participant, 'session': row['session']}
        for emotion in emotion_columns:
            # Extract emotion strengths and calculate the change
            first_emotion_strength = extract_emotion_strength(first_session_row[emotion])
            current_emotion_strength = extract_emotion_strength(row[emotion])
            change = current_emotion_strength - first_emotion_strength
            changes[emotion] = change
        
        # Append changes to the change_df DataFrame
        change_df = change_df._append(changes, ignore_index=True)

# Save the results to a new Excel file
output_file_path = 'emotional_strength_changes.xlsx'
change_df.to_excel(output_file_path, index=False)




