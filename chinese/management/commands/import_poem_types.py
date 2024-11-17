from django.core.management.base import BaseCommand
import json
from chinese.models import PoemType

class Command(BaseCommand):
    help = '从JSON文件导入诗词类型数据'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='doc/importData/poem_types.json', help='JSON文件路径')

    def handle(self, *args, **options):
        try:
            # 读取JSON文件
            with open(options['file'], 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 导入每个诗词类型
            for item in data:
                # 将空格替换为下划线，作为系统内部代码
                code = item['code'].replace(' ', '_')
                
                # 获取或创建诗词类型
                poem_type, created = PoemType.objects.get_or_create(
                    code=code,
                    defaults={'name': item['name']}
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'成功创建诗词类型: {poem_type.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'诗词类型已存在: {poem_type.name}'))

            self.stdout.write(self.style.SUCCESS('导入完成'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'导入失败: {e}')) 