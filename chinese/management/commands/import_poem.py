import json
from django.core.management.base import BaseCommand
from chinese.models import (
    Author, Poem, PoemType, PoemGenre, PoemGenreRelation,
    Annotation, Appreciation, Interpretation, Language
)

class Command(BaseCommand):
    help = '从JSON文件导入诗词数据'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='JSON文件路径')

    def handle(self, *args, **options):
        # 检查文件参数
        if not options['file']:
            self.stderr.write('需要提供JSON文件路径')
            return

        try:
            with open(options['file'], 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.stderr.write(f'读取文件失败: {e}')
            return

        try:
            # 获取或创建作者
            author, _ = Author.objects.get_or_create(
                name=data['author']['name'],
                defaults={
                    'introduction': data['author']['introduction'],
                    'image': data['author']['image']
                }
            )

            # 获取或创建诗词类型
            poem_type, _ = PoemType.objects.get_or_create(
                code=data['type']['code'],
                defaults={'name': data['type']['name']}
            )

            # 获取或创建诗歌体裁
            genre, _ = PoemGenre.objects.get_or_create(
                code=data['genre']['code'],
                defaults={'name': data['genre']['name']}
            )

            # 获取或创建诗词
            poem, created = Poem.objects.get_or_create(
                title=data['title'],
                author=author,
                defaults={
                    'title_pinyin': data['title_pinyin'],
                    'content': data['content'],
                    'pinyin': data['pinyin'],
                    'difficulty': data['difficulty'],
                    'poem_type': poem_type
                }
            )

            # 创建诗歌与体裁的关联
            PoemGenreRelation.objects.get_or_create(
                poem=poem,
                genre=genre
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'成功创建诗词: {poem.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'诗词已存在: {poem.title}'))

            # 获取所有支持的语言
            languages = {lang.code: lang for lang in Language.objects.all()}

            # 创建注释
            for lang_code, content in data['annotations'].items():
                if lang_code in languages:
                    Annotation.objects.get_or_create(
                        poem=poem,
                        language=languages[lang_code],
                        defaults={'content': content}
                    )

            # 创建赏析
            for lang_code, content in data['appreciations'].items():
                if lang_code in languages:
                    Appreciation.objects.get_or_create(
                        poem=poem,
                        language=languages[lang_code],
                        defaults={'content': content}
                    )

            # 创建译文
            # for lang_code, content_data in data['interpretations'].items():
            #     if lang_code in languages:
            #         Interpretation.objects.get_or_create(
            #             poem=poem,
            #             language=languages[lang_code],
            #             defaults={
            #                 'content': content_data['content'],
            #                 'title_translation': content_data['title_translation']
            #             }
            #         )

            if 'interpretations' in data:
                content_data = data['interpretations']['content']
                title_translations = data['interpretations']['title_translation']
                
                for lang_code, content in content_data.items():
                    if lang_code in languages:
                        Interpretation.objects.get_or_create(
                            poem=poem,
                            language=languages[lang_code],
                            defaults={
                                'content': content,
                                'title_translation': title_translations.get(lang_code, '')
                            }
                        )

            self.stdout.write(self.style.SUCCESS('数据导入完成'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'导入失败: {e}')) 