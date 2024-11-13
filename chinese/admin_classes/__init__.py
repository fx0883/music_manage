from django.contrib import admin
from chinese.models import (
    Author, Poem, PoemType, Language, 
    Annotation, Interpretation, Appreciation, PoemGenre, PoemGenreRelation
)
from .author_admin import AuthorAdmin
from .poem_admin import PoemAdmin
from .poem_type_admin import PoemTypeAdmin
from .language_admin import LanguageAdmin
from .annotation_admin import AnnotationAdmin
from .interpretation_admin import InterpretationAdmin
from .appreciation_admin import AppreciationAdmin
from .poem_genre_admin import PoemGenreAdmin
from .poem_genre_relation_admin import PoemGenreRelationAdmin


# 注册所有模型和对应的管理类
# admin.site.register(Author, AuthorAdmin)
# admin.site.register(Poem, PoemAdmin)
# admin.site.register(PoemType, PoemTypeAdmin)
# admin.site.register(Language, LanguageAdmin)
# admin.site.register(Annotation, AnnotationAdmin)
# admin.site.register(Interpretation, InterpretationAdmin)
# admin.site.register(Appreciation, AppreciationAdmin)
# admin.site.register(PoemGenre, PoemGenreAdmin)
# admin.site.register(PoemGenreRelation, PoemGenreRelationAdmin)

__all__ = [
    'AuthorAdmin',
    'PoemAdmin',
    'PoemTypeAdmin',
    'LanguageAdmin',
    'InterpretationAdmin',
    'AppreciationAdmin',
    'AnnotationAdmin',
    'PoemGenreAdmin',
    'PoemGenreRelationAdmin'
]
