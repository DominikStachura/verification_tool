from rest_framework import serializers
from databaseloader.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'file_name', 'item_type', 'item_shape', 'item_cat', 'item_value', 'x_1', 'y_1', 'x_2', 'y_2',
                  'frame', 'cropped_frame', 'region', 'url_image', 'comments']