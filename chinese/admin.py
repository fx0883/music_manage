from django.contrib import admin
from django.apps import apps
from .models import (
    Author, Poem, PoemType, Language,
    Annotation, Interpretation, Appreciation,
    PoemGenre, PoemGenreRelation, FontCategory, FontInfo
)
from .admin_classes import (
    AuthorAdmin, PoemAdmin, PoemTypeAdmin,
    LanguageAdmin, AnnotationAdmin, InterpretationAdmin,
    AppreciationAdmin, PoemGenreAdmin, PoemGenreRelationAdmin,
    FontCategoryAdmin, FontInfoAdmin
)

# 注册所有模型和对应的管理类
admin.site.register(Author, AuthorAdmin)
admin.site.register(Poem, PoemAdmin)
admin.site.register(PoemType, PoemTypeAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Interpretation, InterpretationAdmin)
admin.site.register(Appreciation, AppreciationAdmin)
admin.site.register(PoemGenre, PoemGenreAdmin)
admin.site.register(PoemGenreRelation, PoemGenreRelationAdmin)
admin.site.register(FontCategory, FontCategoryAdmin)
admin.site.register(FontInfo, FontInfoAdmin)
