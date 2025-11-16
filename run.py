#!/usr/bin/env python3
"""
PyCharm优化启动脚本
在PyCharm中右键 -> Run 'run' 即可启动
"""

import os
import sys
from app import app


def main():
    """主启动函数"""
    print("🚀 启动极简博客...")
    print(f"📁 工作目录: {os.getcwd()}")
    print(f"🐍 Python版本: {sys.version.split()[0]}")
    print(f"🌐 访问地址: http://{app.config['HOST']}:{app.config['PORT']}")
    print("⏹️  按 Ctrl+C 停止服务器")
    print("-" * 50)

    try:
        app.run(
            host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'],
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()