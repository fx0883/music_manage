import json
from django.core.management.base import BaseCommand
from chinese.models import Poem

class Command(BaseCommand):
    help = '导出诗词数据为JSON格式'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str, help='诗词标题')

    def handle(self, *args, **options):
        try:
            # 查找诗词
            poem = Poem.objects.get(title=options['title'])
            
            # 构建导出数据
            export_data = {
                'title': poem.title,
                'author': {
                    'name': poem.author.name,
                    'introduction': poem.author.introduction,
                    'image': poem.author.image.name if poem.author.image else ''
                },
                'type': {
                    'name': poem.poem_type.name,
                    'code': poem.poem_type.code
                },
                'content': poem.content,
                'pinyin': poem.pinyin,
                'annotations': {},
                'appreciations': {},
                'interpretations': {}
            }

            # 添加注释
            for annotation in poem.annotations.all():
                export_data['annotations'][annotation.language.code] = annotation.content

            # 添加赏析
            for appreciation in poem.appreciations.all():
                export_data['appreciations'][appreciation.language.code] = appreciation.content

            # 添加译文
            for interpretation in poem.interpretations.all():
                export_data['interpretations'][interpretation.language.code] = interpretation.content

            # 输出JSON
            formatted_json = json.dumps(export_data, ensure_ascii=False, indent=4)
            self.stdout.write(formatted_json)

        except Poem.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'未找到诗词: {options["title"]}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'导出失败: {e}')) 