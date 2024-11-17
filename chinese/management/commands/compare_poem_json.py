from django.core.management.base import BaseCommand
import json
from deepdiff import DeepDiff
import os
from pathlib import Path

class Command(BaseCommand):
    help = '比较原始JSON文件和导出的JSON文件'

    def add_arguments(self, parser):
        parser.add_argument('--original-dir', type=str, help='原始JSON文件目录', default='doc/importData/tang_shi')
        parser.add_argument('--exported-dir', type=str, help='导出的JSON文件目录', default='output/tang_shi')
        parser.add_argument('--file', type=str, help='单个文件名（可选）')
        parser.add_argument('--ignore-author', action='store_true', help='忽略作者字段的比较')

    def compare_files(self, original_file, exported_file, ignore_author=False):
        try:
            # 读取原始文件
            with open(original_file, 'r', encoding='utf-8') as f:
                original_data = json.load(f)

            # 读取导出文件
            with open(exported_file, 'r', encoding='utf-8') as f:
                exported_data = json.load(f)

            # 如果需要忽略作者字段
            if ignore_author:
                if 'author' in original_data:
                    del original_data['author']
                if 'author' in exported_data:
                    del exported_data['author']

            # 使用 DeepDiff 比较
            diff = DeepDiff(original_data, exported_data, ignore_order=True)

            if not diff:
                self.stdout.write(
                    self.style.SUCCESS(f'文件{"(忽略作者)" if ignore_author else ""} 完全一致: {os.path.basename(original_file)}')
                )
                return True
            else:
                self.stdout.write(
                    self.style.WARNING(f'\n发现差异{"(忽略作者)" if ignore_author else ""} - {os.path.basename(original_file)}:')
                )
                # 格式化输出差异
                if 'values_changed' in diff:
                    self.stdout.write('值发生改变的字段:')
                    for path, change in diff['values_changed'].items():
                        self.stdout.write(f"路径: {path}")
                        self.stdout.write(f"原值: {change['old_value']}")
                        self.stdout.write(f"新值: {change['new_value']}\n")

                if 'dictionary_item_added' in diff:
                    self.stdout.write('新增的字段:')
                    for item in diff['dictionary_item_added']:
                        self.stdout.write(f"  {item}")

                if 'dictionary_item_removed' in diff:
                    self.stdout.write('删除的字段:')
                    for item in diff['dictionary_item_removed']:
                        self.stdout.write(f"  {item}")
                return False

        except FileNotFoundError as e:
            self.stderr.write(
                self.style.ERROR(f'文件不存在: {str(e)}')
            )
            return False
        except json.JSONDecodeError as e:
            self.stderr.write(
                self.style.ERROR(f'JSON解析错误 {os.path.basename(original_file)}: {str(e)}')
            )
            return False
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f'比较失败 {os.path.basename(original_file)}: {str(e)}')
            )
            return False

    def handle(self, *args, **options):
        original_dir = options['original_dir']
        exported_dir = options['exported_dir']
        ignore_author = options['ignore_author']
        
        if not os.path.exists(original_dir):
            self.stderr.write(
                self.style.ERROR(f'原始目录不存在: {original_dir}')
            )
            return
            
        if not os.path.exists(exported_dir):
            self.stderr.write(
                self.style.ERROR(f'导出目录不存在: {exported_dir}')
            )
            return

        success_count = 0
        error_count = 0
        error_files = []

        if options['file']:
            # 比较单个文件
            original_file = os.path.join(original_dir, options['file'])
            exported_file = os.path.join(exported_dir, options['file'])
            if self.compare_files(original_file, exported_file, ignore_author):
                success_count += 1
            else:
                error_count += 1
                error_files.append(options['file'])
        else:
            # 比较目录下所有文件
            for file_name in os.listdir(original_dir):
                if file_name.endswith('.json'):
                    original_file = os.path.join(original_dir, file_name)
                    exported_file = os.path.join(exported_dir, file_name)
                    
                    if not os.path.exists(exported_file):
                        self.stderr.write(
                            self.style.ERROR(f'导出文件不存在: {file_name}')
                        )
                        error_count += 1
                        error_files.append(file_name)
                        continue

                    if self.compare_files(original_file, exported_file, ignore_author):
                        success_count += 1
                    else:
                        error_count += 1
                        error_files.append(file_name)

        # 输出统计信息
        self.stdout.write("\n比较统计:")
        self.stdout.write(f"完全一致: {success_count}")
        self.stdout.write(f"存在差异: {error_count}")
        
        if error_files:
            self.stdout.write("\n存在差异的文件:")
            for file_name in error_files:
                self.stdout.write(f"- {file_name}") 