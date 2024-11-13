import json
from django.core.management.base import BaseCommand
from chinese.models import Language

class Command(BaseCommand):
    help = '导入支持的语言'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='JSON文件路径')

    def handle(self, *args, **options):
        # 默认数据
        default_data = {
            "languages": [
                {"name": "Chinese", "code": "zh"},
                {"name": "English", "code": "en"},
                {"name": "Japanese", "code": "ja"}
            ]
        }

        # 如果提供了文件，从文件读取
        if options['file']:
            try:
                with open(options['file'], 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error reading file: {e}'))
                return
        else:
            data = default_data

        # 清空现有数据
        Language.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing languages'))

        # 导入新数据
        for lang in data['languages']:
            Language.objects.create(
                code=lang['code'],
                name=lang['name'],
                is_active=True
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created language "{lang["name"]}"')
            ) 