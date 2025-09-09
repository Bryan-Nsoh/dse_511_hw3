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

# make the time columns
subset_df <- subset_df %>% 
  mutate(date = my(incident_date),
         month = month(date), # make month column
         year = year(date), # make year column
         hour = hour(round_date(as.POSIXct(subset_df$incident_time_24_00,       # make hour column
                                           format="%H:%M:%S"), unit = "hour"))) |>
  select(-c(incident_date, incident_time_24_00, date)) |> # drop these columns
  relocate(year, month, hour, .before = reporting_entity) # move year, month, and hour to be the first columns in the df


# write subset to CSV
write_csv(subset_df, "./data/cleaned/SGO-ADS-crash-data-clean.csv")
