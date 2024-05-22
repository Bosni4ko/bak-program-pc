
# Load required libraries
library(readxl)
library(dplyr)
library(lubridate)
library(openxlsx)


#Tobii file id
tobii_start_file <-111
tobii_end_file <- 136

#File paths
base_tobii_path <- "Data Tobii With ms\\"
tobii_file_pattern <- "data_tobii_with_ms_"
tobii_file_extension <- ".xlsx"

#Participant id
shimmer_start_file <- 13
shimmer_end_file <- 16

#Shimmer path
base_shimmer_path <- "Shimmer ieraksti\\KE_"
base_shimmer_path_2 <- "\\KE_"
shimmer_file_pattern <- "_Session1_Shimmer_F562_Calibrated_PC"
shimmer_file_extension <- ".csv"

#Joined data path
base_write_path <- "Joined data\\KE_"
write_file_pattern <- "\\joined_data_"
write_file_extension <- ".xlsx"

#Current tobii file id
tobii_file_number <- tobii_start_file
#For each file in range
for (i in shimmer_start_file:shimmer_end_file) {
  #load shimmer datasets
  shimmer_file_name <- paste0(base_shimmer_path, i,base_shimmer_path_2 ,i,shimmer_file_pattern,shimmer_file_extension )
  
  # Skip this iteration of the loop if file doesnt exist
  if (!file.exists(shimmer_file_name)) {
    next  
  }
  #Read shimmer file
  data_shimmer <- read.csv(shimmer_file_name,sep="\t",skip = 1)
  data_shimmer$time_shimmer<- as.POSIXct(data_shimmer$Shimmer_F562_TimestampSync_FormattedUnix_CAL,format = "%Y/%m/%d %H:%M:%OS", tz="UTC")
  
  #tobii file counter for each shimmer datasets
  counter <- 0
  # Load tobii datasets
  while (counter < 6){
    #Get tobii file name
    tobii_file_name <- paste0(base_tobii_path,tobii_file_pattern,tobii_file_number,tobii_file_extension)
    tobii_file_number <- tobii_file_number + 1
    # Skip this iteration of the loop if file doesnt exist
    if (!file.exists(tobii_file_name)) {
      next  
    }
    counter <- counter + 1
    
    #Load data
    data <- read_excel(tobii_file_name, sheet = "Sheet 1")
    
    # Convert datetime strings to POSIXct with millisecond precision
    data$datetime_with_ms <- as.POSIXct(data$datetime_with_ms, format = "%Y/%m/%d %H:%M:%OS", tz="UTC")
    
    # Left join the datasets based on the closest datetime_with_ms value
    joined_data <- data %>%
      mutate(closest_datetime_shimmer = sapply(datetime_with_ms, function(x) data_shimmer$time_shimmer[which.min(abs(data_shimmer$time_shimmer - x))])) %>%
      mutate(closest_datetime_shimmer = as.POSIXct(closest_datetime_shimmer, tz = "UTC")) %>%
      left_join(data_shimmer, by = c("closest_datetime_shimmer" = "time_shimmer"))
    
    # Remove the intermediate column
    joined_data <- select(joined_data, -closest_datetime_shimmer)
    
    # Write the data frame to Excel
    output_filename <- paste0(base_write_path, i, write_file_pattern, tobii_file_number-1,write_file_extension)
    write.xlsx(joined_data, output_filename, rowNames = FALSE)
  }
}