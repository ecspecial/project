from rest_framework import serializers
from .models import Users, Stok, Oem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'login', 'dis', 'ch']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Убираем лишние пробелы в строке
        for field in ret:
            if isinstance(ret[field], str):
                ret[field] = ret[field].strip()
        return ret

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stok
        fields = ['article', 'nam', 'oem', 'price', 'quantity', 'brand']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Убираем лишние пробелы в строке
        for field in ret:
            if isinstance(ret[field], str):
                ret[field] = ret[field].strip()
        return ret

class OemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oem
        fields = ['art','oem']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Убираем лишние пробелы в строке
        for field in ret:
            if isinstance(ret[field], str):
                ret[field] = ret[field].strip()
        return ret