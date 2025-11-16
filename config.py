import os
from pathlib import Path

# 基础路径
BASE_DIR = Path(__file__).parent

# Flask配置
SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'

# 博客信息
BLOG_INFO = {
    'title': "我的技术博客",
    'description': "分享技术与生活",
    'author': "开发者",
    'email': "your-email@example.com",
    'github': "your-github-username"
}

# 服务器配置
HOST = os.environ.get('HOST', '127.0.0.1')
PORT = int(os.environ.get('PORT', 5000))
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# 内容配置
CONTENT_DIR = BASE_DIR / 'content'
POSTS_DIR = CONTENT_DIR / 'posts'
PAGES_DIR = CONTENT_DIR / 'pages'

# 确保目录存在
for directory in [CONTENT_DIR, POSTS_DIR, PAGES_DIR]:
    directory.mkdir(exist_ok=True)

# 尝试加载本地配置（如果存在）
try:
    from local_config import *
except ImportError:
    pass