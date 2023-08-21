from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from webapp.models import Article


class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50, required=True)
    content = serializers.CharField(max_length=2000, required=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        return super().validate(attrs)

    def validate_title(self, value):
        if len(value) < 5:
            raise ValidationError("Длина меньше 5 символов не разрешена")
        return value

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    # test = serializers.CharField(max_length=15, write_only=True)


class ArticleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ("id", "author", "created_at", "updated_at")


    def validate_title(self, value):
        if len(value) < 5:
            raise ValidationError("Длина меньше 5 символов не разрешена")
        return value
