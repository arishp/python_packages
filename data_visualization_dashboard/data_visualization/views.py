import matplotlib
matplotlib.use('Agg') # use the Agg backend

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import io
import base64

def dashboard(request):
    data = None
    plot_html = None
    plotly_html = None
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        uploaded_file_url = fs.url(filename)
        data = pd.read_csv(fs.path(filename))

        # Matplotlib/Seaborn Example (Line Plot)
        plt.figure(figsize=(8, 6))
        if len(data.columns) >= 2:
            sns.lineplot(data=data.iloc[:, 3:5])
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plot_base64 = base64.b64encode(buffer.getvalue()).decode()
            plot_html = f'<img src="data:image/png;base64,{plot_base64}" alt="Line Plot">'
            plt.close()

        # Plotly Example (Interactive Scatter Plot)
        if len(data.columns) >= 2:
            try:
                fig = px.scatter(data, x=data.columns[3], y=data.columns[4], title="Interactive Scatter Plot")
                plotly_html = fig.to_html(full_html=False)
            except Exception as e:
                plotly_html = f"Plotly Error: {e}"

    return render(request, 'data_visualization/dashboard.html', {'data': data, 'plot_html': plot_html, 'plotly_html': plotly_html})