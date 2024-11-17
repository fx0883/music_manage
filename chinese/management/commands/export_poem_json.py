from django.core.management.base import BaseCommand
import json
import os
from chinese.models import Poem
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = '将诗词数据导出为JSON格式'

    def add_arguments(self, parser):
        parser.add_argument('--title', type=str, help='诗词标题（可选）')
        parser.add_argument('--output-dir', type=str, help='输出目录路径', default='output/tang_shi')
        parser.add_argument('--all', action='store_true', help='导出所有诗词')

    def export_poem(self, poem, output_dir):
        try:
            # 构建导出数据
            export_data = {
                "title": poem.title,
                "difficulty": poem.difficulty,
                "author": {
                    "name": poem.author.name,
                    "name_pinyin": poem.author.name_pinyin,
                    "image": poem.author.image.name if poem.author.image else None,
                    "introduction": {}
                },
                "annotations": {},
                "appreciations": {},
                "interpretations": {
                    "content": {},
                    "title_translation": {}
                },
                "genre": {
                    "name": None,
                    "code": None
                },
                "type": {
                    "name": poem.poem_type.name if poem.poem_type else None,
                    "code": poem.poem_type.code if poem.poem_type else None
                },
                "content": poem.content,
                "title_pinyin": poem.title_pinyin,
                "pinyin": poem.pinyin
            }

            # 处理作者介绍
            for intro in poem.author.introductions.all():
                export_data["author"]["introduction"][intro.language.code] = intro.content

            # 处理注释
            for annotation in poem.annotations.all():
                export_data["annotations"][annotation.language.code] = annotation.content

            # 处理赏析
            for appreciation in poem.appreciations.all():
                export_data["appreciations"][appreciation.language.code] = appreciation.content

            # 处理译文
            for interpretation in poem.interpretations.all():
                export_data["interpretations"]["content"][interpretation.language.code] = interpretation.content
                if interpretation.title_translation:
                    export_data["interpretations"]["title_translation"][interpretation.language.code] = interpretation.title_translation

            # 处理体裁
            genre_relation = poem.genre_relations.first()
            if genre_relation:
                export_data["genre"]["name"] = genre_relation.genre.name
                export_data["genre"]["code"] = genre_relation.genre.code

            # 格式化JSON输出
            formatted_json = json.dumps(export_data, ensure_ascii=False, indent=4)

            # 构建输出文件路径
            output_file = os.path.join(output_dir, f"{poem.title}.json")
            
            # 写入文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(formatted_json)
            
            self.stdout.write(
                self.style.SUCCESS(f'成功导出诗词: {poem.title}')
            )
            return True

        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f'导出失败 {poem.title}: {str(e)}')
            )
            return False

    def handle(self, *args, **options):
        # 确保输出目录存在
        output_dir = options['output_dir']
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            self.stdout.write(
                self.style.SUCCESS(f'创建输出目录: {output_dir}')
            )

        success_count = 0
        error_count = 0
        error_poems = []

        if options['all']:
            # 导出所有诗词
            poems = Poem.objects.all()
            total = poems.count()
            self.stdout.write(f'开始导出所有诗词，共 {total} 首...')
            
            for poem in poems:
                if self.export_poem(poem, output_dir):
                    success_count += 1
                else:
                    error_count += 1
                    error_poems.append(poem.title)

        elif options['title']:
            # 导出单首诗词
            try:
                poem = Poem.objects.get(title=options['title'])
                if self.export_poem(poem, output_dir):
                    success_count = 1
                else:
                    error_count = 1
                    error_poems.append(poem.title)
            except ObjectDoesNotExist:
                self.stderr.write(
                    self.style.ERROR(f'未找到标题为 "{options["title"]}" 的诗词')
                )
                return

        # 输出统计信息
        self.stdout.write("\n导出统计:")
        self.stdout.write(f"成功: {success_count}")
        self.stdout.write(f"失败: {error_count}")
        
        if error_poems:
            self.stdout.write("\n导出失败的诗词:")
            for title in error_poems:
                self.stdout.write(f"- {title}") 