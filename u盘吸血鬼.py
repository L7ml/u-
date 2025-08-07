import os
import shutil
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    filename='file_copy_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)


def copy_specific_files(source_dir, target_dir, file_extensions):
    """
    复制指定目录下的特定类型文件到目标目录

    参数:
        source_dir: 源目录路径
        target_dir: 目标目录路径
        file_extensions: 需要复制的文件扩展名列表
    """
    # 确保目标目录存在
    os.makedirs(target_dir, exist_ok=True)
    logging.info(f"目标目录已准备: {target_dir}")

    copied_count = 0
    skipped_count = 0

    try:
        # 遍历源目录
        for root, _, files in os.walk(source_dir):
            # 跳过目标目录，避免循环复制
            if root.startswith(target_dir):
                continue

            for file in files:
                # 检查文件扩展名
                if any(file.lower().endswith(ext) for ext in file_extensions):
                    source_path = os.path.join(root, file)
                    target_path = os.path.join(target_dir, file)

                    # 处理同名文件
                    counter = 1
                    while os.path.exists(target_path):
                        name, ext = os.path.splitext(file)
                        target_path = os.path.join(target_dir, f"{name}_{counter}{ext}")
                        counter += 1

                    try:
                        # 复制文件
                        shutil.copy2(source_path, target_path)  # 保留文件元数据
                        copied_count += 1
                        print(f"已复制 {copied_count} 个文件: {file}")
                        logging.info(f"复制成功: {source_path} -> {target_path}")
                    except Exception as e:
                        skipped_count += 1
                        print(f"无法复制 {file}: {str(e)}")
                        logging.error(f"复制失败 {source_path}: {str(e)}")

    except PermissionError:
        logging.error(f"权限不足，无法访问目录: {source_dir}")
        print(f"错误: 没有访问 {source_dir} 的权限")
    except Exception as e:
        logging.error(f"执行过程中发生错误: {str(e)}", exc_info=True)
        print(f"错误: {str(e)}")

    # 输出统计信息
    total_processed = copied_count + skipped_count
    print(f"\n处理完成 - 总计 {total_processed} 个文件")
    print(f"成功复制: {copied_count} 个")
    print(f"跳过/失败: {skipped_count} 个")
    logging.info(f"处理完成 - 成功: {copied_count}, 失败: {skipped_count}")


if __name__ == "__main__":
    # 配置参数
    SOURCE_DIR = "D:\\"
    TARGET_DIR = "E:\\"  # 修正了原代码中的WANNING拼写错误
    FILE_EXTENSIONS = (".docx", ".pdf", ".jpg", ".mp4")  # 需要复制的文件类型

    print(f"开始从 {SOURCE_DIR} 复制文件到 {TARGET_DIR}")
    print(f"文件类型: {', '.join(FILE_EXTENSIONS)}")

    start_time = datetime.now()
    copy_specific_files(SOURCE_DIR, TARGET_DIR, FILE_EXTENSIONS)
    end_time = datetime.now()

    print(f"耗时: {end_time - start_time}")
