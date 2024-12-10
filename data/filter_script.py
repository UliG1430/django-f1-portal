
import os
import pandas as pd

# Directory for saving filtered datasets
output_dir = "filtered_datasets"
os.makedirs(output_dir, exist_ok=True)

def filter_datasets():
    # Filter years
    start_year = 2018
    end_year = 2023

    # Filter races
    races_file = "races.csv"
    print(f"Filtering {races_file}...")
    races_df = pd.read_csv(races_file)
    filtered_races = races_df[(races_df['year'] >= start_year) & (races_df['year'] <= end_year)]
    filtered_races.to_csv(os.path.join(output_dir, "filtered_races.csv"), index=False)
    relevant_race_ids = filtered_races['raceId'].tolist()

    # Tables to filter by raceId
    race_id_tables = {
        "results.csv": "filtered_results.csv",
        "driver_standings.csv": "filtered_driver_standings.csv",
        "constructor_standings.csv": "filtered_constructor_standings.csv",
        "constructor_results.csv": "filtered_constructor_results.csv",
        "qualifying.csv": "filtered_qualifying.csv",
        "lap_times.csv": "filtered_lap_times.csv",
        "pit_stops.csv": "filtered_pit_stops.csv",
        "sprint_results.csv": "filtered_sprint_results.csv"
    }

    for file, output in race_id_tables.items():
        print(f"Filtering {file}...")
        df = pd.read_csv(file)
        filtered_df = df[df['raceId'].isin(relevant_race_ids)]
        filtered_df.to_csv(os.path.join(output_dir, output), index=False)

    # Filter dependent tables (drivers, constructors, circuits)
    filter_independent_tables(relevant_race_ids)

    # Filter seasons
    filter_seasons()

def filter_seasons():
    print("Filtering seasons.csv...")
    seasons_df = pd.read_csv("seasons.csv")
    filtered_seasons = seasons_df[(seasons_df['year'] >= 2018) & (seasons_df['year'] <= 2023)]
    filtered_seasons.to_csv(os.path.join(output_dir, "filtered_seasons.csv"), index=False)

def filter_independent_tables(relevant_race_ids):
    # Filter drivers based on driverId in filtered results
    print("Filtering drivers.csv...")
    results_df = pd.read_csv(os.path.join(output_dir, "filtered_results.csv"))
    relevant_driver_ids = results_df['driverId'].unique()
    drivers_df = pd.read_csv("drivers.csv")
    filtered_drivers = drivers_df[drivers_df['driverId'].isin(relevant_driver_ids)]
    filtered_drivers.to_csv(os.path.join(output_dir, "filtered_drivers.csv"), index=False)

    # Filter constructors based on constructorId in filtered results
    print("Filtering constructors.csv...")
    relevant_constructor_ids = results_df['constructorId'].unique()
    constructors_df = pd.read_csv("constructors.csv")
    filtered_constructors = constructors_df[constructors_df['constructorId'].isin(relevant_constructor_ids)]
    filtered_constructors.to_csv(os.path.join(output_dir, "filtered_constructors.csv"), index=False)

    # Filter circuits based on circuitId in filtered races
    print("Filtering circuits.csv...")
    races_df = pd.read_csv(os.path.join(output_dir, "filtered_races.csv"))
    relevant_circuit_ids = races_df['circuitId'].unique()
    circuits_df = pd.read_csv("circuits.csv")
    filtered_circuits = circuits_df[circuits_df['circuitId'].isin(relevant_circuit_ids)]
    filtered_circuits.to_csv(os.path.join(output_dir, "filtered_circuits.csv"), index=False)

if __name__ == "__main__":
    print("Starting dataset filtering...")
    filter_datasets()
    print(f"Filtered datasets saved in '{output_dir}'")

