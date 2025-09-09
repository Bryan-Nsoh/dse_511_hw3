library(tidyverse)
library(janitor)

# read in the data
ads_data <- read_csv("./data/raw/SGO-ADS-crash-data.csv")

# clean up the column names
ads_data <- clean_names(ads_data)

