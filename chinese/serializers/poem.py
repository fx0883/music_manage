from rest_framework import serializers
from chinese.models import (
    Poem, Annotation, Interpretation, 
    Appreciation, PoemType, PoemGenre,
    Author
)

class PoemListSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source='author.id')
    author_name = serializers.CharField(source='author.name')
    author_pinyin = serializers.CharField(source='author.name_pinyin')
    author_image = serializers.ImageField(source='author.image')
    poem_type_name = serializers.CharField(source='poem_type.name')
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Poem
        fields = [
            'id', 'title', 'title_pinyin', 'content', 
            'author_id', 'author_name', 'author_pinyin', 'author_image',
            'poem_type_name', 'difficulty', 'image_url'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class AuthorSerializer(serializers.ModelSerializer):
    """作者信息序列化器"""
    introduction = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['name', 'name_pinyin', 'image', 'introduction']

    def get_introduction(self, obj):
        language = self.context.get('language')
        introductions = {
            intro.language.code: intro.content 
            for intro in obj.introductions.all()
        }
        return introductions

class PoemDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    annotations = serializers.SerializerMethodField()
    appreciations = serializers.SerializerMethodField()
    interpretations = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Poem
        fields = [
            'title', 'difficulty', 'author',
            'annotations', 'appreciations', 'interpretations',
            'genre', 'type', 'content', 'title_pinyin', 'pinyin',
            'image_url'
        ]

    def get_content_by_language(self, content_dict, current_language):
        """
        Helper method to get content in current language or fallback to English
        """
        if current_language.code in content_dict:
            return content_dict[current_language.code]
        return content_dict.get('en', '')  # 如果没有当前语言，返回英文，如果英文也没有，返回空字符串

    def get_author(self, obj):
        current_language = self.context.get('language')
        # 获取所有语言的介绍
        introductions = {
            intro.language.code: intro.content 
            for intro in obj.author.introductions.all()
        }
        # 只返回当前语言的介绍（或英文）
        introduction = self.get_content_by_language(introductions, current_language)
        
        return {
            'name': obj.author.name,
            'name_pinyin': obj.author.name_pinyin,
            'image': obj.author.image.name if obj.author.image else None,
            'introduction': introduction
        }

    def get_annotations(self, obj):
        current_language = self.context.get('language')
        annotations = {
            annotation.language.code: annotation.content
            for annotation in obj.annotations.all()
        }
        return self.get_content_by_language(annotations, current_language)

    def get_appreciations(self, obj):
        current_language = self.context.get('language')
        appreciations = {
            appreciation.language.code: appreciation.content
            for appreciation in obj.appreciations.all()
        }
        return self.get_content_by_language(appreciations, current_language)

    def get_interpretations(self, obj):
        current_language = self.context.get('language')
        
        # 收集所有语言的内容
        content_dict = {}
        title_translation_dict = {}
        
        for interpretation in obj.interpretations.all():
            content_dict[interpretation.language.code] = interpretation.content
            if interpretation.title_translation:
                title_translation_dict[interpretation.language.code] = interpretation.title_translation
        
        # 只返回当前语言的内容（或英文）
        return {
            'content': self.get_content_by_language(content_dict, current_language),
            'title_translation': self.get_content_by_language(title_translation_dict, current_language)
        }

    def get_genre(self, obj):
        genre_relation = obj.genre_relations.first()
        if genre_relation:
            return {
                'name': genre_relation.genre.name,
                'code': genre_relation.genre.code
            }
        return None

    def get_type(self, obj):
        if obj.poem_type:
            return {
                'name': obj.poem_type.name,
                'code': obj.poem_type.code
            }
        return None

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def to_representation(self, instance):
        result = super().to_representation(instance)
        
        ordered_fields = [
            'title', 'difficulty', 'author',
            'annotations', 'appreciations', 'interpretations',
            'genre', 'type', 'content', 'title_pinyin', 'pinyin',
            'image_url'
        ]
        
        return {
            key: result[key]
            for key in ordered_fields
            if key in result
        }