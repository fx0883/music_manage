from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from chinese.models import PoemGenre

class TestPoemGenreCommands(TestCase):
    def setUp(self):
        self.out = StringIO()
        self.err = StringIO()

    def test_import_poem_genres(self):
        # 执行导入命令
        call_command('import_poem_genres', stdout=self.out, stderr=self.err)
        
        # 验证数据是否正确导入
        self.assertEqual(PoemGenre.objects.count(), 6)  # 应该有6种体裁
        
        # 验证具体数据
        wu_yan_gu_shi = PoemGenre.objects.get(code='wu_yan_gu_shi')
        self.assertEqual(wu_yan_gu_shi.name, '五言古诗')
        
        qi_yan_jue_ju = PoemGenre.objects.get(code='qi_yan_jue_ju')
        self.assertEqual(qi_yan_jue_ju.name, '七言绝句')

    def test_import_duplicate_genres(self):
        # 先创建一个已存在的体裁
        PoemGenre.objects.create(
            code='wu_yan_gu_shi',
            name='五言古诗'
        )
        
        # 再次执行导入命令
        call_command('import_poem_genres', stdout=self.out, stderr=self.err)
        
        # 验证输出中包含跳过信息
        output = self.out.getvalue()
        self.assertIn('已存在', output)
        
        # 验证数据库中仍然只有6条记录
        self.assertEqual(PoemGenre.objects.count(), 6) 