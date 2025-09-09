library(tidyverse)
library(janitor)

# read in the data
ads_data <- read_csv("./data/raw/SGO-ADS-crash-data.csv")

# clean up the column names
ads_data <- clean_names(ads_data)

# get a subset of the data
subset_df <- ads_data |> 
  filter(
    report_version == 1   # get just the first version of earch report
  ) |> 
  select(                 # select the columns we want
    reporting_entity,
    make,
    model,
    model_year,
    incident_date,
    incident_time_24_00,
    roadway_type,
    sv_pre_crash_movement,
    sv_precrash_speed_mph
  )

