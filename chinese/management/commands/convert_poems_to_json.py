import json

class PoemConverter:
    def __init__(self):
        self.poems = []
        
    def clean_text(self, text):
        # 去除特殊符号和多余空格
        text = text.replace('**', '').replace('《', '').replace('》', '')
        text = text.replace('·其一', '一').replace('·其二', '二')
        text = text.replace('·其三', '三').replace('·其四', '四')
        text = text.replace('·其五', '五').replace('·其六', '六')
        text = text.replace('·其七', '七')
        text = text.strip()
        return text
        
    def parse_poems(self, content):
        current_type = None
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # 处理类型行
            if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.')):
                current_type = self.clean_text(line.split('：')[0].split('.')[1])
                continue
                
            # 跳过非诗歌行
            if not line.startswith('- '):
                continue
                
            # 处理作者和诗名
            line = line.strip('- ')
            if '《' in line:
                parts = line.split('《')
                author = parts[0].strip()
                
                for poem_part in parts[1:]:
                    poem_names = poem_part.split('》')[0].split('·')
                    for poem_name in poem_names:
                        if poem_name and poem_name.strip():
                            clean_name = self.clean_text(poem_name)
                            if clean_name:
                                self.poems.append({
                                    'type': current_type,
                                    'author': author.strip(),
                                    'name': clean_name
                                })
                            
    def convert_to_json(self, input_file, output_file):
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 解析诗歌
        self.parse_poems(content)
        
        # 写入JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.poems, f, ensure_ascii=False, indent=2)
            
        return len(self.poems)

def run():
    converter = PoemConverter()
    input_file = 'doc/importData/tang_poems_300.txt'
    output_file = 'doc/importData/tang_poems_300.json'
    count = converter.convert_to_json(input_file, output_file)
    print(f'Successfully converted {count} poems to JSON format')

if __name__ == '__main__':
    run() 