import os
from PIL import Image

def jpg_to_pdf(input_path, output_path, pdfname):
    """
    将指定目录及其1级和2级子目录下的所有JPG图片合并为一个PDF文件。

    参数:
    input_path (str): 输入目录路径。
    output_path (str): 输出目录路径。
    pdfname (str): 生成的PDF文件名（不含扩展名）。
    """
    # 创建输出目录（如果不存在）
    os.makedirs(output_path, exist_ok=True)

    # 收集所有符合条件的图片路径
    image_paths = []

    for dirpath, _, filenames in os.walk(input_path):
        # 计算当前目录相对于输入目录的深度
        rel_path = os.path.relpath(dirpath, input_path)
        depth = rel_path.count(os.sep)

        # 限制遍历深度为0、1或2
        if depth > 2:
            continue

        # 获取当前目录中所有的JPG文件，并按名称排序
        jpg_files = sorted(
            [f for f in filenames if f.lower().endswith(".jpg")]
        )
        for f in jpg_files:
            image_paths.append(os.path.join(dirpath, f))

    if not image_paths:
        print("未找到任何JPG文件")
        return

    # 转换图片为PDF
    try:
        images = []
        for img_path in image_paths:
            try:
                img = Image.open(img_path).convert("RGB")
                images.append(img)
            except Exception as e:
                print(f"跳过无法处理的文件 {img_path}: {str(e)}")

        if not images:
            print("没有有效的图片可转换")
            return

        # 生成输出PDF文件的完整路径
        pdf_fullpath = os.path.join(output_path, f"{pdfname}.pdf")
        images[0].save(
            pdf_fullpath,
            save_all=True,
            append_images=images[1:],
            resolution=100.0
        )
        print(f"成功生成PDF文件：{pdf_fullpath}")

    except Exception as e:
        print(f"生成PDF时发生错误：{str(e)}")


# 示例用法
# jpg_to_pdf("/path/to/input", "/path/to/output", "combined_pdf")