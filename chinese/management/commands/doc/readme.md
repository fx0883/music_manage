
##导入诗词
导入整个目录：
python manage.py import_poem_json
导入指定目录：
python manage.py import_poem_json --dir=path/to/json/dir
导入单个文件：
python manage.py import_poem_json --file=path/to/poem.json


##导出诗词
使用方法：
导出所有诗词：
python manage.py export_poem_json --all
导出单首诗词：
python manage.py export_poem_json --title="静夜思"
比较所有诗词：
python manage.py compare_poem_json
比较单首诗词：
python manage.py compare_poem_json --file="静夜思.json"


我来修改比较脚本，添加忽略作者字段的选项：
使用方法：
正常比较（包括作者字段）：
python manage.py compare_poem_json
忽略作者字段比较：
python manage.py compare_poem_json --ignore-author
比较单个文件并忽略作者字段：
python manage.py compare_poem_json --file="静夜思.json" --ignore-author
