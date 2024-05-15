
# Load required libraries
library(readxl)
library(dplyr)
library(lubridate)
library(openxlsx)

#Load datasets paths
#Tobii with ms path
#4:  105-110
#12: 100-104
#13-16: 111-136
tobii_start_file <-111
tobii_end_file <- 136
base_tobii_path <- "Data Tobii With ms\\"
tobii_file_pattern <- "data_tobii_with_ms_"
tobii_file_extension <- ".xlsx"
#Shimmer path
shimmer_start_file <- 13
shimmer_end_file <- 16
base_shimmer_path <- "Shimmer ieraksti\\KE_"
base_shimmer_path_2 <- "\\KE_"
shimmer_file_pattern <- "_Session1_Shimmer_F562_Calibrated_PC"
shimmer_file_extension <- ".csv"
#Joined data path
base_write_path <- "Joined data\\KE_"
write_file_pattern <- "\\joined_data_"
write_file_extension <- ".xlsx"
#data_shimmer_2 <- read.csv("C:\\Users\\User\\Desktop\\bak_data\\KE_Rezultati\\09.05.2024. Rezultati\\Shimmer ieraksti\\2024-05-07_11.57.02_KE_5_PC_Session1\\KE_5_Session1_Shimmer_F562_Calibrated_PC.csv",header = TRUE)
#C:\\Users\\User\\Desktop\\bak program\\KE_3_Session1_Shimmer_F562_Calibrated_PC.csv
#C:\\Users\\User\\Desktop\\bak program\\Shimmer ieraksti\\KE_3\\KE_3_Session1_Shimmer_F562_Calibrated_PC.csv
#C:\\Users\\User\\Desktop\\bak_data\\KE_Rezultati\\09.05.2024. Rezultati\\Shimmer ieraksti\\2024-05-07_11.57.02_KE_5_PC_Session1\\KE_5_Session1_Shimmer_F562_Calibrated_PC.csv
tobii_file_number <- tobii_start_file
for (i in shimmer_start_file:shimmer_end_file) {
  #load shimmer datasets
  shimmer_file_name <- paste0(base_shimmer_path, i,base_shimmer_path_2 ,i,shimmer_file_pattern,shimmer_file_extension )
  #print(shimmer_file_name)
  if (!file.exists(shimmer_file_name)) {
    next  # Skip this iteration of the loop
  }
  data_shimmer <- read.csv(shimmer_file_name,sep="\t",skip = 1)
  data_shimmer$time_shimmer<- as.POSIXct(data_shimmer$Shimmer_F562_TimestampSync_FormattedUnix_CAL,format = "%Y/%m/%d %H:%M:%OS", tz="UTC")
  #print(data_shimmer$time_shimmer)
  #posix_datetime <- as.POSIXct(data_shimmer$time, format = "%Y-%m-%d %H:%M:%OS3")
  #print(data_shimmer$Shimmer_F562_TimestampSync_FormattedUnix_CAL)
  
  #tobii file counter for each shimmer datasets
  counter <- 0
  # Load tobii datasets
  while (counter < 6){
    tobii_file_name <- paste0(base_tobii_path,tobii_file_pattern,tobii_file_number,tobii_file_extension)
    tobii_file_number <- tobii_file_number + 1
    if (!file.exists(tobii_file_name)) {
      next  # Skip this iteration of the loop
    }
    counter <- counter + 1
    
    data <- read_excel(tobii_file_name, sheet = "Sheet 1")
    
    #str(data$datetime_with_ms)
    #print(data$datetime_with_ms)
    
    # Convert datetime strings to POSIXct with millisecond precision
    data$datetime_with_ms <- as.POSIXct(data$datetime_with_ms, format = "%Y/%m/%d %H:%M:%OS", tz="UTC")
    
    # Print the converted datetime
    #print(data$datetime_with_ms)
    #print(data_shimmer$time_shimmer)
    
    
    # Left join the datasets based on the closest datetime_with_ms value
    joined_data <- data %>%
      mutate(closest_datetime_shimmer = sapply(datetime_with_ms, function(x) data_shimmer$time_shimmer[which.min(abs(data_shimmer$time_shimmer - x))])) %>%
      mutate(closest_datetime_shimmer = as.POSIXct(closest_datetime_shimmer, tz = "UTC")) %>%
      left_join(data_shimmer, by = c("closest_datetime_shimmer" = "time_shimmer"))
    
    
    # Remove the intermediate column
    joined_data <- select(joined_data, -closest_datetime_shimmer)
    
    # View the joined dataset
    #print(joined_data)
    
    # Write the data frame to Excel
    output_filename <- paste0(base_write_path, i, write_file_pattern, tobii_file_number-1,write_file_extension)
    write.xlsx(joined_data, output_filename, rowNames = FALSE)
  }
}