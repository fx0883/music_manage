import os

# 字体类型映射
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

def create_font_folders():
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 创建每个字体类型的文件夹
    for folder_name, chinese_name in FONT_FOLDERS.items():
        # 构建完整的文件夹路径
        folder_path = os.path.join(current_dir, folder_name)
        
        # 如果文件夹不存在则创建
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f'Created folder: {folder_name} ({chinese_name})')
        else:
            print(f'Folder already exists: {folder_name} ({chinese_name})')
            
        # 创建一个 README.md 文件，说明该文件夹的用途
        readme_path = os.path.join(folder_path, 'README.md')
        if not os.path.exists(readme_path):
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f'# {chinese_name}\n\n')
                f.write(f'This folder contains {chinese_name} fonts.\n')
                f.write('请将对应的字体文件放在这个文件夹中。\n')

if __name__ == '__main__':
    create_font_folders()
    print('\nAll font folders have been created successfully!') 