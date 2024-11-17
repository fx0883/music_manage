from django.core.management.base import BaseCommand
import json
import os
from chinese.models import (
    Author, AuthorIntroduction, Poem, PoemType, 
    Language, Annotation, Appreciation, Interpretation,
    PoemGenre, PoemGenreRelation
)
from django.db import transaction
from pathlib import Path

class Command(BaseCommand):
    help = '从JSON文件导入诗词数据'

    def add_arguments(self, parser):
        parser.add_argument('--dir', type=str, help='JSON文件目录路径', default='doc/importData/tang_shi')
        parser.add_argument('--file', type=str, help='单个JSON文件路径（可选）')

    def import_poem(self, file_path):
        try:
            # 读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            with transaction.atomic():  # 使用事务确保数据一致性
                # 1. 处理作者信息
                author_data = data['author']
                author, author_created = Author.objects.update_or_create(
                    name=author_data['name'],
                    defaults={
                        'name_pinyin': author_data['name_pinyin'],
                        'image': author_data['image'] if 'image' in author_data else None
                    }
                )
                
                # 2. 处理作者介绍
                for lang_code, intro_content in author_data['introduction'].items():
                    language = Language.objects.get(code=lang_code)
                    AuthorIntroduction.objects.update_or_create(
                        author=author,
                        language=language,
                        defaults={'content': intro_content}
                    )

                # 3. 处理诗词类型
                poem_type, _ = PoemType.objects.get_or_create(
                    code=data['type']['code'],
                    defaults={'name': data['type']['name']}
                )

                # 4. 创建或更新诗词
                poem, poem_created = Poem.objects.update_or_create(
                    title=data['title'],
                    defaults={
                        'author': author,
                        'content': data['content'],
                        'pinyin': data['pinyin'],
                        'title_pinyin': data['title_pinyin'],
                        'difficulty': data['difficulty'],
                        'poem_type': poem_type
                    }
                )

                # 5. 处理注释
                for lang_code, content in data['annotations'].items():
                    language = Language.objects.get(code=lang_code)
                    Annotation.objects.update_or_create(
                        poem=poem,
                        language=language,
                        defaults={'content': content}
                    )

                # 6. 处理赏析
                for lang_code, content in data['appreciations'].items():
                    language = Language.objects.get(code=lang_code)
                    Appreciation.objects.update_or_create(
                        poem=poem,
                        language=language,
                        defaults={'content': content}
                    )

                # 7. 处理译文
                for lang_code, trans_data in data['interpretations']['content'].items():
                    language = Language.objects.get(code=lang_code)
                    title_trans = data['interpretations']['title_translation'].get(lang_code, '')
                    Interpretation.objects.update_or_create(
                        poem=poem,
                        language=language,
                        defaults={
                            'content': trans_data,
                            'title_translation': title_trans
                        }
                    )

                # 8. 处理诗歌体裁
                if 'genre' in data:
                    genre, _ = PoemGenre.objects.get_or_create(
                        code=data['genre']['code'],
                        defaults={'name': data['genre']['name']}
                    )
                    PoemGenreRelation.objects.get_or_create(
                        poem=poem,
                        genre=genre
                    )

                action = "更新" if not poem_created else "导入"
                self.stdout.write(
                    self.style.SUCCESS(f'成功{action}诗词: {data["title"]}')
                )

        except json.JSONDecodeError as e:
            self.stderr.write(
                self.style.ERROR(f'JSON解析错误 {file_path}: {str(e)}')
            )
            return False
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f'导入失败 {file_path}: {str(e)}')
            )
            return False
        return True

    def handle(self, *args, **options):
        error_files = []
        success_count = 0
        update_count = 0
        error_count = 0

        if options['file']:
            # 导入单个文件
            file_path = options['file']
            if self.import_poem(file_path):
                success_count += 1
            else:
                error_files.append(file_path)
                error_count += 1
        else:
            # 导入目录下所有JSON文件
            dir_path = options['dir']
            if not os.path.exists(dir_path):
                self.stderr.write(
                    self.style.ERROR(f'目录不存在: {dir_path}')
                )
                return

            for file_name in os.listdir(dir_path):
                if file_name.endswith('.json'):
                    file_path = os.path.join(dir_path, file_name)
                    if self.import_poem(file_path):
                        success_count += 1
                    else:
                        error_files.append(file_path)
                        error_count += 1

        # 输出统计信息
        self.stdout.write("\n导入统计:")
        self.stdout.write(f"成功: {success_count}")
        self.stdout.write(f"失败: {error_count}")
        
        if error_files:
            self.stdout.write("\n失败的文件:")
            for file_path in error_files:
                self.stdout.write(f"- {file_path}") 