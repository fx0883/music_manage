from io import StringIO
from django.test import TestCase
from django.core.management import call_command
import json

class PoemExportTest(TestCase):
    def setUp(self):
        # 先导入语言数据
        call_command('import_languages')
        
        # 再导入诗词数据
        call_command('import_poem', '--file=doc/importData/tang_poem.json')

    def test_export_poem(self):
        # 导出诗词
        out = StringIO()
        call_command('export_poem', '静夜思', stdout=out)
        
        # 获取输出的JSON
        exported_data = json.loads(out.getvalue())
        
        # 读取原始数据
        with open('doc/importData/tang_poem.json', 'r', encoding='utf-8') as f:
            original_data = json.load(f)
        
        # 验证基本信息
        self.assertEqual(exported_data['title'], original_data['title'])
        self.assertEqual(exported_data['content'], original_data['content'])
        self.assertEqual(exported_data['pinyin'], original_data['pinyin'])
        
        # 验证作者信息
        self.assertEqual(exported_data['author']['name'], original_data['author']['name'])
        
        # 验证多语言内容
        self.assertEqual(len(exported_data['annotations']), 3)
        self.assertEqual(len(exported_data['appreciations']), 3)
        self.assertEqual(len(exported_data['interpretations']), 3) 