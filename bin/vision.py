#!/usr/bin/env python3
"""
CoPaw 视觉识别工具
支持：OCR文字识别、图像分析
"""

import sys
import os

# 设置 Tesseract 数据路径
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract/tessdata/'

def ocr_image(image_path, lang='chi_sim+eng'):
    """使用 Tesseract OCR 识别图片中的文字"""
    import pytesseract
    from PIL import Image
    
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang=lang)
        return text.strip()
    except Exception as e:
        return f"Error: {e}"

def ocr_easy(image_path):
    """使用 EasyOCR 识别图片中的文字（更准确）"""
    import easyocr
    
    try:
        reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        results = reader.readtext(image_path)
        text = '\n'.join([r[1] for r in results])
        return text
    except Exception as e:
        return f"Error: {e}"

def analyze_image(image_path):
    """分析图片基本信息"""
    from PIL import Image
    
    try:
        img = Image.open(image_path)
        info = {
            'size': img.size,
            'mode': img.mode,
            'format': img.format,
            'width': img.width,
            'height': img.height
        }
        return info
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 vision.py <图片路径> [方法]")
        print("方法: tesseract(默认) | easy | analyze")
        sys.exit(1)
    
    image_path = sys.argv[1]
    method = sys.argv[2] if len(sys.argv) > 2 else 'tesseract'
    
    if not os.path.exists(image_path):
        print(f"文件不存在: {image_path}")
        sys.exit(1)
    
    print(f"=== 图片分析: {image_path} ===\n")
    
    # 先分析图片
    info = analyze_image(image_path)
    print(f"图片信息: {info}\n")
    
    if method == 'analyze':
        pass
    elif method == 'easy':
        print("=== EasyOCR 识别结果 ===\n")
        text = ocr_easy(image_path)
        print(text)
    else:
        print("=== Tesseract OCR 识别结果 ===\n")
        text = ocr_image(image_path)
        print(text)