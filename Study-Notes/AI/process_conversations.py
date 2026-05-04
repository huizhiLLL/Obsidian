"""
AI对话记录整理脚本
将chat-gemini3pro文件夹中的对话整理成结构化总结文档
"""

import os
import re
from datetime import datetime
from pathlib import Path

INPUT_DIR = r'C:\Users\31691\huizhiL\document\md-note\Obsidian\AI\chat-gemini3pro'
OUTPUT_DIR = r'C:\Users\31691\huizhiL\document\md-note\Obsidian\AI\Gemini-Summary'

def get_conversations():
    """获取所有对话单元"""
    conversations = []

    # 遍历输入目录
    for item in os.listdir(INPUT_DIR):
        item_path = os.path.join(INPUT_DIR, item)

        if os.path.isdir(item_path):
            # 子文件夹
            chat_file = os.path.join(item_path, 'chat.md')
            if os.path.exists(chat_file):
                mtime = datetime.fromtimestamp(os.path.getmtime(chat_file))
                name = item
                conversations.append({
                    'type': 'folder',
                    'name': name,
                    'path': chat_file,
                    'date': mtime
                })
        elif item.endswith('.md'):
            # 独立md文件
            mtime = datetime.fromtimestamp(os.path.getmtime(item_path))
            name = item.replace('.md', '')
            conversations.append({
                'type': 'file',
                'name': name,
                'path': item_path,
                'date': mtime
            })

    # 按日期排序
    conversations.sort(key=lambda x: x['date'])
    return conversations

def read_chat_content(filepath):
    """读取对话内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取元数据
    date_match = re.search(r'\*\*Date\*\*: (.+)', content)
    turns_match = re.search(r'\*\*Turns\*\*: (\d+)', content)
    source_match = re.search(r'\*\*Source\*\*: (.+)', content)

    date = date_match.group(1) if date_match else ''
    turns = int(turns_match.group(1)) if turns_match else 0
    source = source_match.group(1) if source_match else ''

    # 提取标题
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else ''

    return {
        'title': title,
        'date': date,
        'turns': turns,
        'source': source,
        'content': content
    }

def extract_conversation_summary(content):
    """提取对话摘要信息"""
    # 提取所有用户问题和AI回答
    turns = []
    current_turn = {}

    lines = content.split('\n')
    in_turn = False
    turn_num = 0

    for line in lines:
        if line.startswith('## Turn '):
            if current_turn and 'user' in current_turn:
                turns.append(current_turn)
            turn_num = int(line.split()[-1])
            current_turn = {'turn': turn_num}
            in_turn = True
        elif in_turn and line.startswith('### 👤'):
            current_turn['user'] = True
        elif in_turn and line.startswith('### 🤖'):
            if 'user' in current_turn and 'assistant' not in current_turn:
                current_turn['assistant'] = True

    if current_turn and 'user' in current_turn:
        turns.append(current_turn)

    return turns

def generate_summary_filename(date_str):
    """生成总结文件夹名称"""
    date_obj = datetime.strptime(date_str.replace(' at ', ' '), '%B %d, %Y %H:%M %p')
    return date_obj.strftime('%Y-%m-%d')

def main():
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 获取所有对话
    conversations = get_conversations()

    print(f"共找到 {len(conversations)} 个对话单元\n")

    for i, conv in enumerate(conversations, 1):
        print(f"处理 {i}/{len(conversations)}: {conv['name']}")

        # 读取对话内容
        info = read_chat_content(conv['path'])

        # 生成输出文件夹名
        date_str = info['date']
        try:
            # 解析日期如 "March 2, 2026 at 10:24 AM"
            date_obj = datetime.strptime(date_str.replace(' at ', ' '), '%B %d, %Y %H:%M %p')
            folder_date = date_obj.strftime('%Y-%m-%d')
        except:
            folder_date = '2026-03-02'

        # 提取主题（从标题或名称）
        topic = info['title'] or conv['name']
        # 简化主题名
        topic = re.sub(r'[\/\\:*?"<>|]', '', topic)[:30]

        output_folder = os.path.join(OUTPUT_DIR, f"{folder_date}_{topic}")
        os.makedirs(output_folder, exist_ok=True)

        print(f"  -> {output_folder}")

        # 生成总结文档
        summary_content = f"""# {info['title'] or conv['name']}

**日期**: {info['date']}
**对话轮数**: {info['turns']}
**来源**: {info['source']}

---

## 对话背景与目标

（待填写）

## 核心问题与需求

（待填写）

## 解决过程

（待填写）

## 最终结果与结论

（待填写）

## 反思与延伸

（待填写）
"""

        knowledge_content = f"""# {info['title'] or conv['name']} - 知识梳理

## 涉及的技术栈/工具

（待填写）

## 关键概念与方法

（待填写）

## 重要的代码片段或命令

（待填写）

## 参考资源

- {info['source']}

## 可复用的经验/最佳实践

（待填写）
"""

        # 写入文件
        with open(os.path.join(output_folder, '01_对话总结回顾.md'), 'w', encoding='utf-8') as f:
            f.write(summary_content)

        with open(os.path.join(output_folder, '02_知识梳理.md'), 'w', encoding='utf-8') as f:
            f.write(knowledge_content)

    print(f"\n完成！共处理 {len(conversations)} 个对话")

if __name__ == '__main__':
    main()