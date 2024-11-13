from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from chinese.models import Language

class ImportLanguagesCommandTest(TestCase):
    def setUp(self):
        self.out = StringIO()
        Language.objects.all().delete()  # 清空已有数据

    def test_import_languages_command(self):
        # 执行导入命令
        call_command('import_languages', stdout=self.out)
        
        # 验证数据库中的语言数量
        self.assertEqual(Language.objects.count(), 3)
        
        # 验证每种语言都被正确创建
        languages = {
            'zh': 'Chinese',
            'en': 'English',
            'ja': 'Japanese'
        }
        
        for code, name in languages.items():
            lang = Language.objects.get(code=code)
            self.assertEqual(lang.name, name)
            self.assertTrue(lang.is_active) 