from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from chinese.models import PoemType

class PoemTypeCommandsTest(TestCase):
    def setUp(self):
        self.out = StringIO()
        self.err = StringIO()

    def test_import_poem_types(self):
        # 执行导入命令
        call_command('import_poem_types', stdout=self.out, stderr=self.err)
        
        # 验证数据是否正确导入
        self.assertEqual(PoemType.objects.count(), 16)  # 文件中有16个类型
        
        # 验证特定类型是否存在
        shi_jing = PoemType.objects.get(code='shi_jing')
        self.assertEqual(shi_jing.name, '诗经')

    def test_export_poem_types(self):
        # 先创建一些测试数据
        PoemType.objects.create(code='test_code', name='测试类型')
        
        # 执行导出命令
        call_command('export_poem_types', stdout=self.out, stderr=self.err)
        
        # 验证输出
        output = self.out.getvalue()
        self.assertIn('测试类型', output)
        self.assertIn('test_code', output) 