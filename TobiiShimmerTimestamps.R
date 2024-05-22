# Load required libraries
library(readxl)
library(dplyr)
library(openxlsx)


#############################
#
#Tobii data
#
#############################
# Define the path and file pattern
base_path <- "Tobii\\"
base_write_path <- "Data Tobii With ms\\"
file_pattern <- "Krizes_emocijas Recording"
file_extension <- ".xlsx"

# Define the range of file numbers
start_file <- 105
end_file <- 110

for (i in start_file:end_file) {
  # Read the Tobii data
  #make file name
  file_name <- paste0(base_path, file_pattern, i, file_extension)
  # Skip this iteration of the loop if file doesnt't exist
  if (!file.exists(file_name)) {
    next  
  }
  #data <- read_excel("data_tobii.xlsx",sheet = "Sheet1")
  data <- read_excel(file_name, sheet = "Sheet1")
  
  #subset
  data<-subset(data,data$Sensor=="Eye Tracker")
  
  # Combine Recording date and Recording start time to create datetime column
  data$start_datetime <- as.POSIXct(paste(data$`Recording date`, data$`Recording start time`), format = "%m/%d/%Y %H:%M:%OS", tz = "UTC")
  
  # Calculate end time for each row in microseconds
  data$datetime_with_ms <- data$start_datetime + data$`Recording timestamp` / 1000000
  
  # Format the end time to show in microseconds with 3 digits after the last comma
  data$datetime_with_ms <- format(data$datetime_with_ms, format = "%Y/%m/%d %H:%M:%OS3", tz = "UTC")
  
  # Write the data frame to Excel
  output_filename <- paste0(base_write_path, "data_tobii_with_ms_", i, ".xlsx")
  write.xlsx(data, output_filename, rowNames = FALSE)
}








