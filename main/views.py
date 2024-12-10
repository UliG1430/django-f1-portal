import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
from django.conf import settings
from django.shortcuts import render

def home(request):
      # Ruta absoluta a los datasets
    drivers_path = os.path.join(settings.BASE_DIR, 'data', 'drivers.csv')
    races_path = os.path.join(settings.BASE_DIR, 'data', 'races.csv')

    # Cargar datasets
    drivers = pd.read_csv(drivers_path)
    races = pd.read_csv(races_path)

    # Gráfico 1: Número de conductores por nacionalidad
    nationality_counts = drivers['nationality'].value_counts()
    plt.figure(figsize=(8, 5))
    nationality_counts.plot(kind='bar', color='skyblue')
    plt.title('Conductores por Nacionalidad')
    plt.xlabel('Nacionalidad')
    plt.ylabel('Cantidad')
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph1 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Gráfico 2: Número de carreras por año
    races['year'] = pd.to_datetime(races['date']).dt.year
    races_per_year = races['year'].value_counts().sort_index()
    plt.figure(figsize=(8, 5))
    races_per_year.plot(kind='line', marker='o', color='green')
    plt.title('Carreras por Año')
    plt.xlabel('Año')
    plt.ylabel('Cantidad de Carreras')
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph2 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Pasar gráficos al template
    context = {
        'graph1': graph1,
        'graph2': graph2,
    }
    return render(request, 'main/home.html', context)
