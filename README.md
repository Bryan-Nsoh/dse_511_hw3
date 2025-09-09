# Homework #3: Collaborative Data Wrangling & EDA

Minimal scaffolding for the assignment. Fill in dataset choice, cleaning steps, and EDA later.

## Dataset
- **Source:**
  
  National Highway Transporation Safety Asssociation's Standing General Order on Crash Reporting for Advanced Driving Systems (ADS) as of August 2025,
  Obtained September 2025,
  https://www.nhtsa.gov/laws-regulations/standing-general-order-crash-reporting#data

- **Description:**
  
  Self-reported crashes from car companies were physical damage occured involving a level 3 through 5 autonomous vehicle.

  The subset of data used consisted of the following:

| Variable               | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| `year`                 | The calendar year when the record/event was reported.                      |
| `month`                | The month of the record/event (1–12).                                       |
| `hour`                 | The hour of the day (0–23) when the event occurred.                        |
| `reporting_entity`     | The organization or agency that submitted the report.                      |
| `make`                 | The manufacturer of the vehicle (e.g., Toyota, Ford, Honda).                |
| `model`                | The specific vehicle model (e.g., Camry, F-150, Civic).                     |
| `model_year`           | The model year of the vehicle, usually defined by the manufacturer.         |
| `roadway_type`         | The classification of the road (e.g., highway, street, intersection).   |
| `sv_pre_crash_movement`| The vehicle’s movement just before the crash (e.g., going straight, turning right).|
| `sv_precrash_speed_mph`| The speed of the subject vehicle (in miles per hour) before the crash.      |

## Data Cleaning Steps:
  
1. Cleaned the column names
2. Filter the reports to version 1
3. Selected a subset of the data consisting mostly of the columns given in the table above
4. Derived the `year`, `month`, and `hour` columns from the `incident_date` and `incident_time_24_00` columns
5. Dropped the `incident_date` and `incident_time_24_00` columns
   
## How To Use
- Place raw data in `data/raw/`.
- Put cleaned/derived data in `data/cleaned/`.
- Add analysis code in `notebooks/eda.ipynb` or new notebooks.

## Collaboration
- Each partner: create a branch, make commits, open a PR.
- Intentionally create/resolve one small conflict (e.g., edit this intro).
