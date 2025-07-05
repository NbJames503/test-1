import os
import re
from datetime import datetime
from PIL import Image, ExifTags
import piexif

def get_exif_date(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                decoded_tag = ExifTags.TAGS.get(tag, tag)
                if decoded_tag == 'DateTimeOriginal':
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"读取EXIF信息失败: {e}")
    return None

def rename_photos(folder_path):
    try:
        print(f"正在处理目录: {folder_path}")
        
        # 列出所有.jpg文件
        jpg_files = [f for f in os.listdir(folder_path) 
                    if f.lower().endswith('.jpg')]
        print(f"找到 {len(jpg_files)} 个JPG文件")
        
        for filename in jpg_files:
            try:
                file_path = os.path.join(folder_path, filename)
                
                # 优先获取EXIF拍摄时间
                photo_date = get_exif_date(file_path)
                
                # 如果没有EXIF信息，使用文件创建时间
                if not photo_date:
                    timestamp = os.path.getctime(file_path)
                    photo_date = datetime.fromtimestamp(timestamp)
                
                # 构造新文件名（仅使用日期）
                date_str = photo_date.strftime("%Y-%m-%d")
                new_name = f"{date_str}.jpg"
                
                # 处理重名文件
                counter = 1
                while os.path.exists(os.path.join(folder_path, new_name)):
                    new_name = f"{date_str}_{counter}.jpg"
                    counter += 1
                
                # 执行重命名
                new_path = os.path.join(folder_path, new_name)
                os.rename(file_path, new_path)
                print(f"已重命名: {filename} -> {new_name}")
                
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {e}")
                continue
                
    except Exception as e:
        print(f"程序运行出错: {e}")
    finally:
        print("处理完成")

if __name__ == "__main__":
    folder_path = r"e:\测试文件夹\工作照片"
    rename_photos(folder_path)