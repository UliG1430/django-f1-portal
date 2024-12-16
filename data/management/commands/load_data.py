from django.core.management.base import BaseCommand
import pandas as pd
from main.models import Driver, Circuit, Climate, Constructor, Race, RaceResult, RaceWeather

class Command(BaseCommand):
    help = "Carga y transforma los datos para el modelo dimensional"

    def handle(self, *args, **kwargs):
        # Cargar los datasets
        f1_data = pd.read_csv("path_to/formula1_dataset.csv")
        weather_data = pd.read_csv("path_to/weather_dataset.csv")

        # LIMPIEZA Y TRANSFORMACIÓN

        # Limpieza de datos de Fórmula 1
        f1_data['driver_name'] = f1_data['driver_name'].str.strip().str.title()
        f1_data['race_id'] = f1_data['season'].astype(str) + "_" + f1_data['round'].astype(str)

        # Limpieza de datos climáticos
        weather_data['condition'] = weather_data['condition'].str.lower()
        weather_data['race_id'] = weather_data['date'].str[:10]  # Ajustar según el formato

        # CREAR DIMENSIONES

        # Dimensión Pilotos
        dim_pilotos = f1_data[['driver_id', 'driver_name', 'nationality', 'constructor']].drop_duplicates()
        for _, row in dim_pilotos.iterrows():
            Driver.objects.update_or_create(
                driver_id=row['driver_id'],
                defaults={
                    'name': row['driver_name'],
                    'nationality': row['nationality'],
                    'constructor': row['constructor']
                }
            )

        # Dimensión Circuitos
        dim_circuitos = f1_data[['circuit_id', 'circuit_name', 'location', 'country']].drop_duplicates()
        for _, row in dim_circuitos.iterrows():
            Circuit.objects.update_or_create(
                circuit_id=row['circuit_id'],
                defaults={
                    'name': row['circuit_name'],
                    'location': row['location'],
                    'country': row['country']
                }
            )

        # Dimensión Clima
        dim_clima = weather_data[['condition', 'temperature', 'wind_speed']].drop_duplicates()
        for _, row in dim_clima.iterrows():
            Climate.objects.update_or_create(
                condition=row['condition'],
                defaults={
                    'temperature': row['temperature'],
                    'wind_speed': row['wind_speed']
                }
            )

        # Dimensión Constructores
        dim_constructores = f1_data[['constructor', 'constructor_country']].drop_duplicates()
        for _, row in dim_constructores.iterrows():
            Constructor.objects.update_or_create(
                constructor_id=row['constructor'],
                defaults={'name': row['constructor'], 'country': row['constructor_country']}
            )

        # Dimensión Carreras
        dim_races = f1_data[['race_id', 'season', 'round', 'circuit_id']].drop_duplicates()
        for _, row in dim_races.iterrows():
            circuit = Circuit.objects.get(circuit_id=row['circuit_id'])
            Race.objects.update_or_create(
                race_id=row['race_id'],
                defaults={
                    'season': row['season'],
                    'round_number': row['round'],
                    'circuit': circuit
                }
            )

        # CREAR TABLAS DE HECHOS

        # Tabla de Hechos: Resultados de Carreras
        fact_results = f1_data
        for _, row in fact_results.iterrows():
            driver = Driver.objects.get(driver_id=row['driver_id'])
            constructor = Constructor.objects.get(constructor_id=row['constructor'])
            race = Race.objects.get(race_id=row['race_id'])

            RaceResult.objects.update_or_create(
                race=race,
                driver=driver,
                constructor=constructor,
                defaults={
                    'position': row['position'],
                    'points': row['points'],
                    'fastest_lap': row.get('fastest_lap', None),
                    'time': row.get('time', None)
                }
            )

        # Tabla de Hechos: Condiciones de Clima
        fact_weather = weather_data
        for _, row in fact_weather.iterrows():
            race = Race.objects.get(race_id=row['race_id'])
            climate = Climate.objects.filter(condition=row['condition']).first()

            RaceWeather.objects.update_or_create(
                race=race,
                climate=climate,
                defaults={
                    'date': row['date'],
                    'temperature': row['temperature'],
                    'wind_speed': row['wind_speed']
                }
            )

        self.stdout.write(self.style.SUCCESS("Datos cargados y transformados exitosamente."))