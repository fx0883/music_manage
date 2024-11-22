from rest_framework import serializers
from chinese.models import Author, AuthorIntroduction

class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'name_pinyin', 'image']

class AuthorDetailSerializer(serializers.ModelSerializer):
    introduction = serializers.SerializerMethodField()
    poems = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'name', 'name_pinyin', 'image', 'introduction', 'poems']

    def get_introduction(self, obj):
        language = self.context.get('language')
        intro = obj.introductions.filter(language=language).first()
        return intro.content if intro else None

    def get_poems(self, obj):
        return [
            {
                'id': poem.id,
                'title': poem.title,
                'title_pinyin': poem.title_pinyin
            }
            for poem in obj.poem_set.all()
        ] 