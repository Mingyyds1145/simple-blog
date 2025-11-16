// 极简博客 JavaScript 功能

document.addEventListener('DOMContentLoaded', function() {
    // 代码块处理
    enhanceCodeBlocks();

    // 表格处理
    enhanceTables();

    // 链接处理
    enhanceLinks();

    console.log('🚀 极简博客加载完成');
});

/**
 * 增强代码块显示
 */
function enhanceCodeBlocks() {
    const codeBlocks = document.querySelectorAll('pre code');

    codeBlocks.forEach((block) => {
        // 添加复制按钮
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-code-btn';
        copyButton.textContent = '复制';
        copyButton.title = '复制代码';

        copyButton.addEventListener('click', function() {
            copyToClipboard(block.textContent);
            copyButton.textContent = '已复制!';
            setTimeout(() => {
                copyButton.textContent = '复制';
            }, 2000);
        });

        const pre = block.parentElement;
        pre.style.position = 'relative';
        pre.appendChild(copyButton);

        // 简单的语法高亮（基础实现）
        highlightSyntax(block);
    });
}

/**
 * 复制文本到剪贴板
 */
function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();

    try {
        document.execCommand('copy');
    } catch (err) {
        console.error('复制失败:', err);
    }

    document.body.removeChild(textarea);
}

/**
 * 基础语法高亮
 */
function highlightSyntax(codeBlock) {
    const code = codeBlock.textContent;
    let highlighted = code;

    // 简单的关键词高亮（实际项目中建议使用highlight.js等库）
    const patterns = {
        'keyword': /\b(function|if|else|for|while|return|var|let|const|class)\b/g,
        'string': /('.*?'|".*?")/g,
        'comment': /(\/\/.*|\/\*[\s\S]*?\*\/)/g,
        'number': /\b\d+\b/g
    };

    Object.entries(patterns).forEach(([type, pattern]) => {
        highlighted = highlighted.replace(pattern, '<span class="hljs-' + type + '">$&</span>');
    });

    codeBlock.innerHTML = highlighted;
}

/**
 * 增强表格显示
 */
function enhanceTables() {
    const tables = document.querySelectorAll('table');

    tables.forEach((table) => {
        // 为表格添加响应式包装
        const wrapper = document.createElement('div');
        wrapper.className = 'table-wrapper';
        wrapper.style.overflowX = 'auto';

        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    });
}

/**
 * 增强链接处理
 */
function enhanceLinks() {
    const links = document.querySelectorAll('a[href^="http"]');

    links.forEach((link) => {
        // 为外部链接添加标识
        if (link.hostname !== window.location.hostname) {
            link.target = '_blank';
            link.rel = 'noopener noreferrer';

            // 添加外部链接图标
            const icon = document.createElement('span');
            icon.innerHTML = ' ↗';
            icon.style.fontSize = '0.8em';
            link.appendChild(icon);
        }
    });
    // 开发信息页面功能
function initDevInfoPage() {
    // 如果不在开发信息页面，直接返回
    if (!document.querySelector('.dev-info')) {
        return;
    }

    console.log('📊 初始化开发信息页面');

    // 这里可以添加开发信息页面特有的JavaScript功能
    // 比如实时数据更新、图表交互等

    // 示例：添加图表容器响应式调整
    window.addEventListener('resize', function() {
        // 图表会自动响应，这里可以添加额外的调整
        console.log('窗口大小改变，图表已自动调整');
    });
}

// 在DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 原有的功能
    enhanceCodeBlocks();
    enhanceTables();
    enhanceLinks();

    // 初始化开发信息页面
    initDevInfoPage();

    console.log('🚀 极简博客加载完成');
});
}

// 添加复制按钮的CSS样式
const style = document.createElement('style');
style.textContent = `
.copy-code-btn {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    background: #007acc;
    color: white;
    border: none;
    padding: 0.25rem 0.5rem;
    border-radius: 3px;
    font-size: 0.8rem;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.3s ease;
}

pre:hover .copy-code-btn {
    opacity: 1;
}

.copy-code-btn:hover {
    background: #005a9e;
}

.table-wrapper {
    margin: 1rem 0;
    border-radius: 4px;
}
`;
document.head.appendChild(style);