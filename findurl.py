import json
import re
import requests
import sys
import os

# 获取目标目录路径
target_dir = sys.argv[1]

# 创建输出目录（如果不存在）
output_dir = target_dir.rstrip('/').split('/')[-1]  # 取目录名作为输出目录名
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

paths = []

# 递归遍历所有文件
for dirpath, dirnames, filenames in os.walk(target_dir):
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)
        try:
            with open(file_path, "r", encoding='gb18030', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 提取所有引号内的字符串
                    matches = re.findall(r"""['"](.*?)['"]""", line)
                    for match in matches:
                        if '/' in match:  # 只保留包含斜杠的字符串
                            paths.append(match)
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

# 去重并写入结果文件
output_file = os.path.join(output_dir, f"{output_dir}_param1123.txt")
with open(output_file, "w", encoding='gb18030', errors='ignore') as out_f:
    for path in sorted(set(paths)):
        out_f.write(path + '\n')

print(f"Processing completed! Results saved to: {output_file}")