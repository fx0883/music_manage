from django.core.management.base import BaseCommand
import json
from chinese.models import PoemType

class Command(BaseCommand):
    help = '导出所有诗词类型数据'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='导出的JSON文件路径（可选）')

    def handle(self, *args, **options):
        try:
            # 获取所有诗词类型
            poem_types = PoemType.objects.all()
            
            # 构建导出数据
            export_data = [
                {
                    'name': pt.name,
                    'code': pt.code
                }
                for pt in poem_types
            ]

            # 格式化JSON输出
            formatted_json = json.dumps(export_data, ensure_ascii=False, indent=4)

            # 如果指定了文件，则写入文件
            if options['file']:
                with open(options['file'], 'w', encoding='utf-8') as f:
                    f.write(formatted_json)
                self.stdout.write(self.style.SUCCESS(f'数据已导出到: {options["file"]}'))
            else:
                # 否则打印到控制台
                self.stdout.write(formatted_json)

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'导出失败: {e}')) 