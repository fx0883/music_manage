import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from pypinyin import pinyin, Style
import logging
import svgwrite
import tempfile
from cairosvg import svg2png
import base64
import time

# 添加日志配置
logger = logging.getLogger(__name__)

# 定义临时文件夹路径
FONTS_ROOT = os.path.join('media', 'fonts')
TEMP_DIR = os.path.join(FONTS_ROOT, 'temp')

def ensure_temp_dir():
    """确保临时文件夹存在"""
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        logger.info(f"Created temporary directory: {TEMP_DIR}")

def generate_font_preview(font_file, text, font_size=64):
    """生成字体预览图"""
    try:
        # 创建临时字体文件（PIL需要文件路径）
        with tempfile.NamedTemporaryFile(suffix='.ttf', delete=False) as tmp_font:
            for chunk in font_file.chunks():
                tmp_font.write(chunk)
            tmp_font_path = tmp_font.name

        try:
            # 加载字体
            font = ImageFont.truetype(tmp_font_path, size=font_size)
            
            # 计算文本大小
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # 添加padding
            padding = 40
            img_width = text_width + padding * 2
            img_height = text_height + padding * 2
            
            # 创建透明背景的PNG图像
            img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # 在图像中心绘制文字
            x = padding
            y = padding
            draw.text((x, y), text, font=font, fill=(0, 0, 0, 255))
            
            return img

        finally:
            # 清理临时字体文件
            if os.path.exists(tmp_font_path):
                os.unlink(tmp_font_path)
                
    except Exception as e:
        logger.error(f"Error generating font preview: {str(e)}")
        # 返回一个默认的错误图片
        error_img = Image.new('RGBA', (400, 100), (0,0,0,0))
        draw = ImageDraw.Draw(error_img)
        try:
            default_font = ImageFont.load_default()
            draw.text((200, 50), f"Error: {str(e)}", font=default_font, fill='black', anchor='mm')
        except Exception:
            draw.text((200, 50), f"Error: {str(e)}", fill='black', anchor='mm')
        return error_img

def get_pinyin_code(text):
    """将文本转换为拼音代码"""
    try:
        py_list = pinyin(text, style=Style.NORMAL)
        return '_'.join([''.join(p) for p in py_list])
    except Exception as e:
        logger.error(f"Error generating pinyin code: {str(e)}")
        return text  # 如果转换失败，返回原文本

def get_filename_without_extension(filepath):
    """获取文件名（不含扩展名）"""
    try:
        return os.path.splitext(os.path.basename(filepath))[0]
    except Exception as e:
        logger.error(f"Error getting filename: {str(e)}")
        return filepath  # 如果处理失败，返回原始路径
    