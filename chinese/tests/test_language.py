import json
from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from chinese.models import Language

class LanguageModelTest(TestCase):
    def setUp(self):
        self.test_data = {
            "languages": [
                {"name": "Chinese", "code": "zh"},
                {"name": "English", "code": "en"},
                {"name": "Japanese", "code": "ja"}
            ]
        }

    def test_language_model_str(self):
        """测试Language模型的字符串表示"""
        lang = Language.objects.create(
            name="Chinese",
            code="zh",
            is_active=True
        )
        self.assertEqual(str(lang), "Chinese (zh)")

    def test_language_uniqueness(self):
        """测试语言代码的唯一性"""
        Language.objects.create(
            name="Chinese",
            code="zh",
            is_active=True
        )
        # 尝试创建相同代码的语言应该失败
        with self.assertRaises(Exception):
            Language.objects.create(
                name="Chinese 2",
                code="zh",
                is_active=True
            )

class ImportLanguageCommandTest(TestCase):
    def setUp(self):
        self.out = StringIO()

    def test_import_languages(self):
        """测试导入语言命令"""
        # 执行导入命令
        call_command('import_languages', stdout=self.out)
        
        # 验证数据
        self.assertEqual(Language.objects.count(), 3)
        
        # 验证每种语言
        languages = {
            'zh': 'Chinese',
            'en': 'English',
            'ja': 'Japanese'
        }
        for code, name in languages.items():
            lang = Language.objects.get(code=code)
            self.assertEqual(lang.name, name)
            self.assertTrue(lang.is_active)

    def test_reimport_languages(self):
        """测试重复导入语言"""
        # 第一次导入
        call_command('import_languages', stdout=self.out)
        self.assertEqual(Language.objects.count(), 3)
        
        # 清空输出
        self.out.seek(0)
        self.out.truncate()
        
        # 第二次导入
        call_command('import_languages', stdout=self.out)
        self.assertEqual(Language.objects.count(), 3) 