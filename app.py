import os
import markdown
import sys
from flask import Flask, render_template, abort, request, redirect, url_for
from datetime import datetime, timedelta, date
from pathlib import Path
from collections import Counter
import flask

# 导入工具函数
from utils import (
    create_default_content,
    get_reading_time,
    format_date
)

# 创建Flask应用
app = Flask(__name__)
app.config.from_pyfile('config.py')

# 记录启动时间
app.start_time = datetime.now()

# 确保默认内容存在
create_default_content()

# Markdown扩展
MARKDOWN_EXTENSIONS = [
    'fenced_code',
    'tables',
    'footnotes',
    'toc'
]


def load_content(file_path):
    """读取和解析markdown文件"""
    path = Path(file_path)

    if not path.exists():
        return None

    try:
        content = path.read_text(encoding='utf-8')

        # 解析元数据
        metadata = {}
        body = content

        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                # 解析YAML格式的元数据
                try:
                    import yaml
                    metadata = yaml.safe_load(parts[1])
                    body = parts[2].strip()
                except ImportError:
                    # 如果没有yaml，使用简单解析
                    metadata_lines = parts[1].strip().split('\n')
                    for line in metadata_lines:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip()
                    body = parts[2].strip()
                except Exception as e:
                    print(f"YAML解析错误: {e}")
                    # YAML解析失败，回退到简单解析
                    metadata_lines = parts[1].strip().split('\n')
                    for line in metadata_lines:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip()
                    body = parts[2].strip()

        # 确保metadata是字典
        if not isinstance(metadata, dict):
            metadata = {'title': path.stem}

        # 转换markdown为HTML
        html_content = markdown.markdown(body, extensions=MARKDOWN_EXTENSIONS)

        # 计算阅读时间
        reading_time = get_reading_time(body)

        return {
            'metadata': metadata or {'title': path.stem},
            'content': html_content,
            'raw_content': body,
            'file_path': str(path),
            'reading_time': reading_time
        }

    except Exception as e:
        print(f"❌ 读取文件失败 {file_path}: {e}")
        return None


def get_posts():
    """获取所有博客文章"""
    posts = []

    for file_path in app.config['POSTS_DIR'].glob('*.md'):
        post_data = load_content(file_path)
        if post_data:
            post_data['slug'] = file_path.stem
            # 确保有日期字段
            if 'date' not in post_data['metadata']:
                # 从文件名或文件时间推断
                post_data['metadata']['date'] = datetime.fromtimestamp(
                    file_path.stat().st_mtime
                ).strftime('%Y-%m-%d')

            # 格式化日期显示
            post_data['formatted_date'] = format_date(
                post_data['metadata']['date'],
                '%Y-%m-%d',
                '%Y年%m月%d日'
            )

            posts.append(post_data)

    # 按日期排序
    def get_sort_key(post):
        date_val = post['metadata'].get('date', '')
        if isinstance(date_val, (datetime, date)):
            return date_val
        elif isinstance(date_val, str):
            try:
                return datetime.strptime(date_val, '%Y-%m-%d')
            except ValueError:
                return datetime.min
        else:
            return datetime.min

    posts.sort(key=get_sort_key, reverse=True)
    return posts


def get_pages():
    """获取所有静态页面"""
    pages = {}

    for file_path in app.config['PAGES_DIR'].glob('*.md'):
        page_data = load_content(file_path)
        if page_data:
            pages[file_path.stem] = page_data

    return pages


def safe_get_month(date_value):
    """安全地获取月份信息"""
    try:
        if isinstance(date_value, (date, datetime)):
            return date_value.strftime('%Y-%m')
        elif isinstance(date_value, str):
            # 尝试解析字符串日期
            for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']:
                try:
                    dt = datetime.strptime(date_value, fmt)
                    return dt.strftime('%Y-%m')
                except ValueError:
                    continue
            # 如果无法解析，尝试提取前7个字符
            if len(date_value) >= 7:
                return date_value[:7]
        return None
    except Exception:
        return None


def analyze_posts_data(posts):
    """分析文章数据，用于图表显示"""
    # 按月份统计
    posts_by_month = {}
    all_tags = []

    for post in posts:
        # 月度统计
        date_value = post['metadata'].get('date', '')
        month = safe_get_month(date_value)

        if month:
            posts_by_month[month] = posts_by_month.get(month, 0) + 1

        # 标签统计
        tags = post['metadata'].get('tags', [])
        if isinstance(tags, list):
            all_tags.extend([str(tag) for tag in tags])
        elif isinstance(tags, str):
            # 处理逗号分隔的标签
            all_tags.extend([tag.strip() for tag in tags.split(',')])

    # 生成月度数据（最近12个月）
    months = []
    monthly_counts = []

    end_date = datetime.now()
    for i in range(11, -1, -1):
        date_obj = end_date - timedelta(days=30 * i)
        month_key = date_obj.strftime('%Y-%m')
        months.append(date_obj.strftime('%Y年%m月'))
        monthly_counts.append(posts_by_month.get(month_key, 0))

    # 标签统计
    tag_counter = Counter(all_tags)
    top_tags = [{'tag': tag, 'count': count} for tag, count in tag_counter.most_common(8)]

    return {
        'months': months,
        'posts_by_month': monthly_counts,
        'top_tags': top_tags
    }


@app.route('/')
def index():
    """首页"""
    posts = get_posts()
    return render_template('index.html', posts=posts)


@app.route('/post/<slug>')
def show_post(slug):
    """显示文章"""
    file_path = app.config['POSTS_DIR'] / f'{slug}.md'
    post_data = load_content(file_path)

    if not post_data:
        abort(404)

    return render_template('post.html', post=post_data)


@app.route('/page/<slug>')
def show_page(slug):
    """显示页面"""
    file_path = app.config['PAGES_DIR'] / f'{slug}.md'
    page_data = load_content(file_path)

    if not page_data:
        abort(404)

    return render_template('page.html', page=page_data)


@app.route('/about')
def about():
    """关于页面"""
    return show_page('about')


@app.route('/archive')
def archive():
    """文章归档"""
    posts = get_posts()
    return render_template('archive.html', posts=posts)


@app.route('/_/info')
def dev_info():
    """开发信息页面"""
    if not app.config['DEBUG']:
        abort(404)

    try:
        posts = get_posts()
        pages = get_pages()

        # 分析文章数据
        chart_data = analyze_posts_data(posts)

        # 准备最近文章信息
        recent_posts = []
        for post in posts[:5]:  # 最近5篇文章
            # 处理日期显示
            date_value = post['metadata'].get('date', '未知')
            date_display = format_date(date_value, '%Y-%m-%d', '%Y-%m-%d')

            recent_posts.append({
                'title': post['metadata'].get('title', '无标题'),
                'date': date_display,
                'slug': post['slug'],
                'tags': post['metadata'].get('tags', [])
            })

        info = {
            'posts_count': len(posts),
            'pages_count': len(pages),
            'content_dir': str(app.config['CONTENT_DIR']),
            'debug_mode': app.config['DEBUG'],
            'recent_posts': recent_posts,
            'server_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'start_time': app.start_time.isoformat(),
            'python_version': sys.version.split()[0],
            'flask_version': flask.__version__,
            'chart_data': chart_data
        }

        return render_template('dev_info.html', info=info)

    except Exception as e:
        print(f"开发信息页面错误: {e}")
        # 返回简单的错误信息页面
        return f"""
        <h1>开发信息页面错误</h1>
        <p>错误信息: {str(e)}</p>
        <p>请检查控制台日志获取详细信息。</p>
        <a href="/">返回首页</a>
        """, 500


@app.errorhandler(404)
def page_not_found(e):
    """404页面"""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )