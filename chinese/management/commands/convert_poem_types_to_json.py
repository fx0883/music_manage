import json
from pypinyin import pinyin, Style

class PoemTypeConverter:
    def __init__(self):
        self.types = []
        
    def to_pinyin(self, chinese):
        # 将中文转换为拼音，并用下划线连接
        py_list = pinyin(chinese, style=Style.NORMAL)
        return '_'.join([''.join(p) for p in py_list])
        
    def clean_text(self, text):
        # 去除特殊符号和多余空格
        text = text.replace('**', '').strip()
        return text
        
    def parse_types(self, content):
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # 处理类型行
            if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.')):
                type_name = self.clean_text(line.split('：')[0].split('.')[1])
                if type_name:
                    self.types.append({
                        'code': self.to_pinyin(type_name),
                        'name': type_name
                    })
                            
    def convert_to_json(self, input_file, output_file):
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 解析类型
        self.parse_types(content)
        
        # 写入JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.types, f, ensure_ascii=False, indent=2)
            
        return len(self.types)

def run():
    converter = PoemTypeConverter()
    input_file = 'doc/importData/tang_poems_300.txt'
    output_file = 'doc/importData/poem_types.json'
    count = converter.convert_to_json(input_file, output_file)
    print(f'Successfully converted {count} poem types to JSON format')

if __name__ == '__main__':
    run() 