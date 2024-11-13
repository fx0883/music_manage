from django.core.management.base import BaseCommand
import json
from chinese.models import PoemGenre

class Command(BaseCommand):
    help = '从JSON文件导入诗歌体裁数据'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='doc/importData/poem_types.json', help='JSON文件路径')

    def handle(self, *args, **options):
        try:
            # 读取JSON文件
            with open(options['file'], 'r', encoding='utf-8') as f:
                genres = json.load(f)

            # 记录成功和失败的数量
            success_count = 0
            skip_count = 0

            # 导入每个体裁
            for genre in genres:
                try:
                    # 使用get_or_create避免重复导入
                    obj, created = PoemGenre.objects.get_or_create(
                        code=genre['code'],
                        defaults={
                            'name': genre['name'],
                            'description': f'唐诗体裁：{genre["name"]}'  # 添加默认描述
                        }
                    )

                    if created:
                        success_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'成功导入体裁: {obj.name} (code: {obj.code})')
                        )
                    else:
                        skip_count += 1
                        self.stdout.write(
                            self.style.WARNING(f'体裁已存在，跳过: {obj.name} (code: {obj.code})')
                        )

                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(f'导入体裁失败 {genre.get("name", "未知")}: {str(e)}')
                    )

            # 输出总结信息
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n导入完成！\n'
                    f'成功导入: {success_count}\n'
                    f'已存在跳过: {skip_count}\n'
                    f'总计处理: {success_count + skip_count}'
                )
            )

        except FileNotFoundError:
            self.stderr.write(
                self.style.ERROR(f'找不到文件: {options["file"]}')
            )
        except json.JSONDecodeError:
            self.stderr.write(
                self.style.ERROR(f'JSON格式错误: {options["file"]}')
            )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f'导入过程中发生错误: {str(e)}')
            ) 