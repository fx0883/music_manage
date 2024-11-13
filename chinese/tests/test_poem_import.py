import json
from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from chinese.models import Author, Poem, PoemType, Annotation, Appreciation, Interpretation, Language

class PoemImportTest(TestCase):
    def setUp(self):
        # 创建测试用的语言数据
        self.zh = Language.objects.create(code='zh', name='Chinese')
        self.en = Language.objects.create(code='en', name='English')
        self.ja = Language.objects.create(code='ja', name='Japanese')
        
        # 读取测试数据
        with open('doc/importData/tang_poem.json', 'r', encoding='utf-8') as f:
            self.test_data = json.load(f)

    def test_import_poem(self):
        # 执行导入命令
        out = StringIO()
        call_command('import_poem', '--file=doc/importData/tang_poem.json', stdout=out)
        
        # 验证基础数据
        self.assertEqual(Poem.objects.count(), 1)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(PoemType.objects.count(), 1)
        
        # 获取导入的诗词
        poem = Poem.objects.first()
        
        # 验证诗词信息
        self.assertEqual(poem.title, '静夜思')
        self.assertEqual(poem.author.name, '李白')
        self.assertEqual(poem.content, self.test_data['content'])
        self.assertEqual(poem.pinyin, self.test_data['pinyin'])
        
        # 验证注释
        self.assertEqual(poem.annotations.count(), 3)
        for lang in [self.zh, self.en, self.ja]:
            self.assertTrue(
                poem.annotations.filter(language=lang).exists()
            )
            
        # 验证赏析
        self.assertEqual(poem.appreciations.count(), 3)
        for lang in [self.zh, self.en, self.ja]:
            self.assertTrue(
                poem.appreciations.filter(language=lang).exists()
            )
            
        # 验证译文
        self.assertEqual(poem.interpretations.count(), 3)
        for lang in [self.zh, self.en, self.ja]:
            self.assertTrue(
                poem.interpretations.filter(language=lang).exists()
            )

    def test_reimport_poem(self):
        # 第一次导入
        call_command('import_poem', '--file=doc/importData/tang_poem.json')
        
        # 第二次导入
        out = StringIO()
        call_command('import_poem', '--file=doc/importData/tang_poem.json', stdout=out)
        
        # 验证数据没有重复
        self.assertEqual(Poem.objects.count(), 1)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(PoemType.objects.count(), 1)
        
        # 验证输出包含已存在的提示
        output = out.getvalue()
        self.assertIn('已存在', output) 