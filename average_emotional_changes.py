import pandas as pd

#This program calculates average emotions strength change since first recording for each video or organization response


# Load the Excel file
file_path = 'emotional_strength_changes.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')
# Group by 'video_stimulus' and calculate the mean for each emotion
average_emotions = data.groupby('video_stimulus').mean(numeric_only=True)

# Save results to the excel
average_emotions.to_excel('average_emotions_by_video_stimulus.xlsx')
