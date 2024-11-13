from django.contrib import admin
from chinese.models import (
    Author, Poem, PoemType, Language, 
    Annotation, Interpretation, Appreciation, 
    PoemTypeInterpretation
)
from .author_admin import AuthorAdmin
from .poem_admin import PoemAdmin
from .poem_type_admin import PoemTypeAdmin
from .language_admin import LanguageAdmin
from .annotation_admin import AnnotationAdmin
from .interpretation_admin import InterpretationAdmin
from .appreciation_admin import AppreciationAdmin


# 注册所有模型和对应的管理类
admin.site.register(Author, AuthorAdmin)
admin.site.register(Poem, PoemAdmin)
admin.site.register(PoemType, PoemTypeAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Interpretation, InterpretationAdmin)
admin.site.register(Appreciation, AppreciationAdmin)
admin.site.register(PoemTypeInterpretation) 