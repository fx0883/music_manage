我来说明如何使用这两个命令文件：
导入诗词数据 (import_poem.py):

# 基本用法
python manage.py import_poem --file=doc/importData/tang_poem.json

# 导入多个诗词文件
python manage.py import_poem --file=doc/importData/poem1.json
python manage.py import_poem --file=doc/importData/poem2.json
导出诗词数据 (export_poem.py):

# 基本用法 - 通过标题导出诗词
python manage.py export_poem 静夜思

# 导出到文件
python manage.py export_poem 静夜思 > output.json
使用前的准备工作：
1. 确保已经创建并应用了所有数据库迁移：
确保已经导入了必要的基础数据：
使用示例：
注意事项：
1. 导入数据前确保JSON文件格式正确
导入前确保相关的语言、类型和体裁数据已存在
导出的数据会包含所有相关信息，包括注释、赏析和译文
如果诗词已存在，导入命令会更新相关信息而不是创建新记录
错误处理：
如果遇到错误，命令会显示详细的错误信息
可以查看Django日志获取更多信息
常见错误包括文件不存在、JSON格式错误、数据不完整等
这些命令可以帮助你管理诗词数据库，方便数据的导入导出和维护。


# 导入语言数据
python manage.py import_languages

# 导入诗词类型数据
python manage.py import_poem_types

# 导入诗词体裁数据
python manage.py import_poem_genres