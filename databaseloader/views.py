
from django.shortcuts import render

import pandas as pd
import numpy as np

from .models import Item


def upload_database(request):
    uploaded_file = None
    # delete previous database objects
    Item.objects.all().delete()

    if request.method == 'POST':
        uploaded_file = request.FILES['csv_file']
        df = pd.read_csv(uploaded_file, sep=',')
        df['id'] = np.arange(1, len(df) + 1)

        for _, row in df.iterrows():
            temp_obj = Item(
                id=row['id'],
                file_name=row['file_name'],
                item_type=row['item_type'],
                item_shape=row['item_shape'],
                item_cat=row['item_cat'],
                item_value=int(row['item_value']),
                x_1=int(row['x1']),
                y_1=int(row['y1']),
                x_2=int(row['x2']),
                y_2=int(row['y2']),
                frame=row['frame'],
                cropped_frame=row['cropped_frame'],
                region=row['region'],
            )

            temp_obj.save()

        df = pd.DataFrame(list(Item.objects.all().values()))
        df = df.to_html(index=False)

        return render(request, 'loader.html', {'df': df})
    else:
        return render(request, 'loader.html')