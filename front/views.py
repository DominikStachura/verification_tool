from django.shortcuts import render
from databaseloader.models import Item, ImageItem, SignType, SignShape
from databaseloader.utils import get_type_and_shape
from pathlib import Path

import pandas as pd
import numpy as np
import glob
import csv

#TODO
#wartosc comment z kolumny w bazie ma byc wyswietlana i na jej podstawie checkbox ma byc ustawiany,
#domysna wartosc to correct i tylko jeden moze byc zaznaczony w danym momencie
#ddatkowo wartosc do combo boxa powinna byc tez z bazy danych a nie None
# Create your views here.


def index(request):
    uploaded_file = None
    # delete previous database objects
    df_images = _get_list_images()

    if request.method == 'POST':
        SignType.objects.all().delete()
        SignShape.objects.all().delete()
        Item.objects.all().delete()
        ImageItem.objects.all().delete()
        uploaded_file = request.FILES['csv_file']
        df = pd.read_csv(uploaded_file, sep=',')
        df['id'] = np.arange(1, len(df) + 1)

        for _, row in df_images.iterrows():
            temp_obj = ImageItem(
                id=row['id'],
                image_name=row['image_reference'])
            temp_obj.save()

        queryset_images = ImageItem.objects.all().values()

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
                # url_image=r'127.0.0.1/8000/usa/' + f"{_get_image_index(queryset_images, str(row['frame']))}"
                url_image=r'http://127.0.0.1:8000/images/' + r'{}/{}'.format(row["region"], row["frame"].split('.')[0]),
            )

            temp_obj.save()

        sign_types, sign_shapes = get_type_and_shape()
        for sign_type in sign_types:
            SignType(sign_type=sign_type).save()

        SignShape(sign_shape='None').save()
        for sign_shape in sign_shapes:
            SignShape(sign_shape=sign_shape).save()

    return render(request, 'app/index.html')


def validator(request):
    # print(Item.objects.get_by_url(id=1).file_name)
    # print(Item.objects.all().get_by_url(id=1).file_name)
    items = Item.objects.all()
    types = SignType.objects.all()
    shapes = SignShape.objects.all()
    return render(request, 'app/validator.html', context={'items': items,
                                                          'types': types,
                                                          'shapes': shapes})


def tables(request):
    df = pd.DataFrame(list(Item.objects.all().values()))
    df = df.to_html(index=False)

    return render(request, 'app/tables.html', {'df': df})


def update(request):
    values = dict(request.POST)
    for value in values.values():
        if len(value) > 1:
            url = value[0]
            comment = value[1]
            type = value[2]
            shape = value[3]
            instance = Item.objects.get_by_url(url=url)
            instance.comments = comment
            if type != 'None':
                instance.item_cat = type
            if shape != 'None':
                instance.item_shape = shape
            instance.save()

    fields = Item._meta.fields
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # write your header first
        writer.writerow([str(field).split('.')[2] for field in fields])
        for obj in Item.objects.all():
            writer.writerow([getattr(obj, field.name) for field in fields])

    return render(request, 'app/index.html')


def _get_list_images():
    images = glob.glob(r'C:\repos\tool\static\logs\usa\*.jpg')
    df_images = pd.DataFrame(images, columns=["image_reference"])
    df_images['id'] = np.arange(1, len(images) + 1)
    df_images['api_link'] = "https:/api_link/images/"

    return df_images


def _get_image_index(query_set, image_name):
    try:
        return next(query['id'] for query in query_set if
                    Path(query['image_name'].split('/')[-1]) == Path(image_name.split('/')[-1]))
    except Exception as e:
        return 'not found'
