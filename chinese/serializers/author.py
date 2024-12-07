from rest_framework import serializers
from chinese.models import Author, AuthorIntroduction

class AuthorListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Author
        fields = ['id', 'name', 'name_pinyin', 'image']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class AuthorDetailSerializer(serializers.ModelSerializer):
    introduction = serializers.SerializerMethodField()
    poems = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField('get_image')
    class Meta:
        model = Author
        fields = ['id', 'name', 'name_pinyin', 'image', 'introduction', 'poems']

    def get_introduction(self, obj):
        language = self.context.get('language')
        intro = obj.introductions.filter(language=language).first()
        return intro.content if intro else None

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_poems(self, obj):
        return [
            {
                'id': poem.id,
                'title': poem.title,
                'title_pinyin': poem.title_pinyin
            }
            for poem in obj.poem_set.all()
        ] 