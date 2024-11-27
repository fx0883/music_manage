from django.core.management.base import BaseCommand
from chinese.models import FontCategory

class Command(BaseCommand):
    help = '导入预定义的字体分类数据'

    def handle(self, *args, **options):
        # 预定义的字体分类
        FONT_FOLDERS = {
            'xingshu': '行书',
            'kaishu': '楷书', 
            'caoshu': '草书',
            'lishu': '隶书',
            'zhuanshu': '篆书',
            'maobi': '毛笔',
            'kaiti': '楷体',
            'songti': '宋体',
            'fangsong': '仿宋',
            'tongqu': '童趣'
        }

        # 记录导入结果
        created_count = 0
        updated_count = 0
        error_count = 0

        # 为每个分类设置默认的显示顺序
        default_order = {code: index for index, code in enumerate(FONT_FOLDERS.keys())}

        # 导入每个字体分类
        for code, name in FONT_FOLDERS.items():
            try:
                # 尝试获取或创建字体分类
                category, created = FontCategory.objects.update_or_create(
                    code=code,
                    defaults={
                        'name': name,
                        'description': f'{name}字体分类',
                        'order': default_order[code]
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'成功创建字体分类: {name} (code: {code})')
                    )
                else:
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'更新已存在的字体分类: {name} (code: {code})')
                    )

            except Exception as e:
                error_count += 1
                self.stderr.write(
                    self.style.ERROR(f'导入字体分类失败 {code}: {str(e)}')
                )

        # 输出统计信息
        self.stdout.write('\n导入统计:')
        self.stdout.write(f'新建: {created_count}')
        self.stdout.write(f'更新: {updated_count}')
        self.stdout.write(f'失败: {error_count}')

        if error_count == 0:
            self.stdout.write(self.style.SUCCESS('\n所有字体分类导入成功！'))
        else:
            self.stdout.write(self.style.WARNING('\n部分字体分类导入失败，请检查错误信息。')) 