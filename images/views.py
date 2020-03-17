from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
import os

regions = os.listdir('static/logs/')

def default_page(request):
    return render(request, 'default.html')

def hello_page(request):
    return render(request, 'hello.html')


# class country(DetailView):
#     template_name = 'country.html'
#
#     def get_object(self, *args, **kwargs):
#         country = self.kwargs.get('country')
#         exist = True if country in regions else False
#         return country, exist

# class country(DetailView):
#     template_name = 'country.html'

def country(request, *args, **kwargs):
    country = kwargs.get('country')
    exist = True if country in regions else False
    return render(request, 'country.html', context={'country': country, 'exist': exist})


def render_photo(request, *args, **kwargs):
    country = kwargs.get('country')
    name = kwargs.get('name')
    photo_dir = r'logs/{country}/{name}.jpg'.format(country=country, name=name)
    exist = True if country in regions else False
    context = {'country': country,
               'exist': exist,
               'dir': photo_dir}
    image_path = r'static/logs/{country}/{name}.jpg'.format(country=country, name=name)
    if os.path.exists(image_path):
        image = open(image_path, 'rb').read()
        return HttpResponse(image, content_type='image/jpg')
    else:
        return render(request, 'images/render_photo.html', context=context)

def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        print(myfile)
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'images/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'images/upload.html')
