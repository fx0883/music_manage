from django.contrib import admin
from chinese.models import (
    Author, Poem, PoemType, Language, 
    Annotation, Interpretation, Appreciation, PoemGenre, PoemGenreRelation, FontCategory, FontInfo,
    ImageCategory, ImageInfo
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
from .font_category_admin import FontCategoryAdmin
from .font_info_admin import FontInfoAdmin
from .image_admin import ImageCategoryAdmin, ImageInfoAdmin

__all__ = [
    'AuthorAdmin',
    'PoemAdmin',
    'PoemTypeAdmin',
    'LanguageAdmin',
    'AnnotationAdmin',
    'InterpretationAdmin',
    'AppreciationAdmin',
    'PoemGenreAdmin',
    'PoemGenreRelationAdmin',
    'FontCategoryAdmin',
    'FontInfoAdmin',
    'ImageCategoryAdmin',
    'ImageInfoAdmin'
]
