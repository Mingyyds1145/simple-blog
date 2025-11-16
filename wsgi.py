"""
生产环境WSGI入口点
用于部署到服务器
"""
from app import app

if __name__ == '__main__':
    app.run()