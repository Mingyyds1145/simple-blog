"""
工具函数模块
提供博客系统的辅助功能
"""

import os
import re
from datetime import datetime, date
from pathlib import Path


def slugify(text):
    """
    将文本转换为URL友好的slug格式

    Args:
        text (str): 要转换的文本

    Returns:
        str: 转换后的slug
    """
    # 转换为小写，移除特殊字符，用连字符替换空格
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
    return slug


def format_date(date_value, format_from='%Y-%m-%d', format_to='%Y年%m月%d日'):
    """
    格式化日期

    Args:
        date_value: 日期值，可以是字符串、datetime.date或datetime.datetime对象
        format_from (str): 原始格式（仅对字符串有效）
        format_to (str): 目标格式

    Returns:
        str: 格式化后的日期字符串
    """
    try:
        if isinstance(date_value, (datetime, date)):
            # 如果是日期对象，直接格式化
            return date_value.strftime(format_to)
        elif isinstance(date_value, str):
            # 如果是字符串，先解析再格式化
            try:
                date_obj = datetime.strptime(date_value, format_from)
                return date_obj.strftime(format_to)
            except ValueError:
                # 如果解析失败，返回原字符串
                return date_value
        else:
            return str(date_value)
    except (ValueError, TypeError, AttributeError) as e:
        print(f"日期格式化错误: {e}")
        return str(date_value)


def get_file_info(file_path):
    """
    获取文件的基本信息

    Args:
        file_path (str|Path): 文件路径

    Returns:
        dict: 文件信息字典
    """
    path = Path(file_path)
    if not path.exists():
        return None

    stat = path.stat()
    return {
        'name': path.name,
        'stem': path.stem,
        'size': stat.st_size,
        'created': datetime.fromtimestamp(stat.st_ctime),
        'modified': datetime.fromtimestamp(stat.st_mtime),
        'extension': path.suffix
    }


def truncate_text(text, length=150, suffix='...'):
    """
    截断文本到指定长度

    Args:
        text (str): 原始文本
        length (int): 最大长度
        suffix (str): 后缀

    Returns:
        str: 截断后的文本
    """
    if len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + suffix


def is_markdown_file(filename):
    """
    检查文件是否为Markdown文件

    Args:
        filename (str): 文件名

    Returns:
        bool: 是否为Markdown文件
    """
    return filename.lower().endswith(('.md', '.markdown'))


def get_reading_time(text, wpm=200):
    """
    估算阅读时间

    Args:
        text (str): 文本内容
        wpm (int): 每分钟阅读字数

    Returns:
        int: 估算的阅读分钟数
    """
    # 简单的中文字数统计（一个汉字算一个字）
    word_count = len(text.strip())
    reading_time = max(1, round(word_count / wpm))
    return reading_time


def validate_markdown_frontmatter(content):
    """
    验证Markdown文件的Frontmatter格式

    Args:
        content (str): Markdown内容

    Returns:
        tuple: (is_valid, error_message)
    """
    if not content.startswith('---'):
        return False, "Frontmatter必须以 '---' 开始"

    parts = content.split('---', 2)
    if len(parts) < 3:
        return False, "Frontmatter格式不完整"

    return True, "格式正确"


def create_default_content():
    """
    创建默认的内容文件（如果不存在）
    """
    content_dirs = ['content/posts', 'content/pages']

    for dir_path in content_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    # 创建默认的欢迎文章（如果不存在）
    welcome_post = Path('content/posts/welcome.md')
    if not welcome_post.exists():
        welcome_content = """---
title: 欢迎使用极简博客
date: 2024-01-15
tags: [博客, 开始, Python]
excerpt: 欢迎来到我的新博客！这是一个基于Flask的极简博客系统。
---

# 欢迎！

这是我的第一篇博客文章，使用**极简博客模板**创建。

## 功能特点

- 🚀 基于Markdown写作
- 🎨 响应式设计
- ⚡ 极简代码结构
- 🔧 易于自定义扩展

## 代码示例

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True) """