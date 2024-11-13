from django.test import TestCase
from chinese.models.poem_type import PoemType
from chinese.models.poem_type_interpretation import PoemTypeInterpretation
from chinese.models.language import Language

class PoemModelTest(TestCase):
    def setUp(self):
        # 创建中文语言对象
        self.zh_lang = Language.objects.create(
            code='zh',
            name='Chinese'
        )

        # 创建英文语言对象
        self.en_lang = Language.objects.create(
            code='en',
            name='English'
        )

    def test_create_poem_type_with_interpretations(self):
        # 创建诗词类型
        poem_type = PoemType.objects.create(
            code='shi_jing',
            name='诗经'
        )

        # 创建中文解释
        PoemTypeInterpretation.objects.create(
            poem_type=poem_type,
            language=self.zh_lang,
            name='诗经',
            description='中国最早的诗歌总集，收集了从西周初年至春秋中叶的诗歌，共311篇。'
        )

        # 创建英文解释
        PoemTypeInterpretation.objects.create(
            poem_type=poem_type,
            language=self.en_lang,
            name='Book of Songs',
            description='The oldest existing collection of Chinese poetry, comprising 311 works dating from the 11th to 7th centuries BC.'
        )

        # 验证数据
        self.assertEqual(PoemType.objects.count(), 1)
        saved_type = PoemType.objects.first()
        self.assertEqual(saved_type.name, '诗经')
        
        # 验证译文
        self.assertEqual(saved_type.interpretations.count(), 2)
        zh_interpretation = saved_type.interpretations.get(language=self.zh_lang)
        en_interpretation = saved_type.interpretations.get(language=self.en_lang)
        self.assertEqual(zh_interpretation.name, '诗经')
        self.assertEqual(en_interpretation.name, 'Book of Songs') 