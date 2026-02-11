#!/usr/bin/env python3
"""
合并周记 Markdown 文件的脚本
功能：
1. 移除 01-38 篇文章开头的 YAML frontmatter
2. 使用文件名作为二级标题分隔每篇文章
3. 合并所有内容到一个文件中
"""

import os
import re
from pathlib import Path


def has_frontmatter(content: str) -> bool:
    """检查内容是否以 YAML frontmatter 开头"""
    return content.strip().startswith('---')


def remove_frontmatter(content: str) -> str:
    """移除 YAML frontmatter"""
    lines = content.split('\n')
    in_frontmatter = False
    content_start = 0

    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                # 第二个 ---，frontmatter 结束
                content_start = i + 1
                break

    return '\n'.join(lines[content_start:]).lstrip()


def get_title_from_filename(filename: str) -> str:
    """从文件名提取标题（移除序号前缀）"""
    # 移除 .md 扩展名
    name_without_ext = filename.replace('.md', '')

    # 尝试移除开头的数字序号（如 "01 ", "02 " 等）
    match = re.match(r'^\d+\s+(.+)$', name_without_ext)
    if match:
        return match.group(1)
    return name_without_ext


def merge_weekly_notes(output_file: str = 'merged_weekly.md'):
    """合并所有周记文件"""
    # 获取当前目录
    current_dir = Path(__file__).parent

    # 获取所有 .md 文件并按文件名排序
    md_files = sorted([f for f in current_dir.glob('*.md') if f.name != 'merged_weekly.md' and f.name != 'merge_weekly.py'])

    merged_content = []

    for md_file in md_files:
        # 读取文件内容
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 移除 frontmatter（如果有）
        if has_frontmatter(content):
            content = remove_frontmatter(content)

        # 获取标题
        title = get_title_from_filename(md_file.name)

        # 添加二级标题和内容
        merged_content.append(f'## {title}\n')
        merged_content.append(content)
        merged_content.append('\n\n')  # 文件之间添加空行

    # 写入合并后的文件
    output_path = current_dir / output_file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(merged_content))

    print(f'Successfully merged {len(md_files)} files to {output_file}')
    print(f'Output path: {output_path.absolute()}')


if __name__ == '__main__':
    merge_weekly_notes()
