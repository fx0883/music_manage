import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

# 创建目标目录
if not os.path.exists('static/tabbar'):
    os.makedirs('static/tabbar')

# 诗词图标 SVG
poem_svg = '''
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M19 3H5C3.89 3 3 3.9 3 5V19C3 20.1 3.89 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM19 19H5V5H19V19Z" fill="currentColor"/>
  <path d="M7 7H17V9H7V7ZM7 11H17V13H7V11ZM7 15H13V17H7V15Z" fill="currentColor"/>
</svg>
'''

# 推荐图标 SVG
recommend_svg = '''
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 17.27L18.18 21L16.54 13.97L22 9.24L14.81 8.63L12 2L9.19 8.63L2 9.24L7.46 13.97L5.82 21L12 17.27Z" fill="currentColor"/>
</svg>
'''

# 游戏图标 SVG
game_svg = '''
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M21 6H3C1.9 6 1 6.9 1 8V16C1 17.1 1.9 18 3 18H21C22.1 18 23 17.1 23 16V8C23 6.9 22.1 6 21 6ZM11 13H8V16H6V13H3V11H6V8H8V11H11V13ZM15.5 15C14.67 15 14 14.33 14 13.5C14 12.67 14.67 12 15.5 12C16.33 12 17 12.67 17 13.5C17 14.33 16.33 15 15.5 15ZM19.5 12C18.67 12 18 11.33 18 10.5C18 9.67 18.67 9 19.5 9C20.33 9 21 9.67 21 10.5C21 11.33 20.33 12 19.5 12Z" fill="currentColor"/>
</svg>
'''

# 用户图标 SVG
user_svg = '''
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z" fill="currentColor"/>
</svg>
'''

def create_png_from_svg(svg_content, output_path, color):
    # 替换SVG中的颜色
    svg_content = svg_content.replace('currentColor', color)
    
    # 创建临时文件保存SVG
    with open('temp.svg', 'w') as f:
        f.write(svg_content)
    
    try:
        # 转换SVG为PNG
        drawing = svg2rlg('temp.svg')
        renderPM.drawToFile(drawing, output_path, fmt='PNG')
    finally:
        # 删除临时文件
        if os.path.exists('temp.svg'):
            os.remove('temp.svg')

# 生成所有图标
def generate_icons():
    icons = {
        'poem': poem_svg,
        'recommend': recommend_svg,
        'game': game_svg,
        'user': user_svg
    }
    
    normal_color = '#7A7E83'  # 未选中颜色
    active_color = '#3cc51f'  # 选中颜色
    
    for name, svg in icons.items():
        # 生成普通图标
        create_png_from_svg(
            svg,
            f'static/tabbar/{name}.png',
            normal_color
        )
        
        # 生成选中状态图标
        create_png_from_svg(
            svg,
            f'static/tabbar/{name}-active.png',
            active_color
        )

if __name__ == '__main__':
    generate_icons()
    print('图标生成完成')