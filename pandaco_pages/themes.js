/**
 * PandaCo 吃了么 - 主题切换系统
 * 支持四套主题：随和、科幻、女性化、赛博朋克
 */

class ThemeManager {
    constructor() {
        this.themes = ['warm', 'scifi', 'feminine', 'cyberpunk'];
        this.themeNames = {
            'warm': '随和',
            'scifi': '科幻',
            'feminine': '柔美',
            'cyberpunk': '赛博'
        };
        this.currentTheme = this.loadTheme();
        this.init();
    }

    /**
     * 初始化主题系统
     */
    init() {
        // 应用保存的主题
        this.applyTheme(this.currentTheme);
        
        // 创建主题切换器UI
        this.createThemeSwitcher();
        
        // 监听系统主题变化（可选）
        this.watchSystemTheme();
    }

    /**
     * 创建主题切换器UI
     */
    createThemeSwitcher() {
        const navbar = document.querySelector('.nav-links') || document.querySelector('nav ul');
        if (!navbar) return;

        // 创建主题切换器容器
        const switcher = document.createElement('div');
        switcher.className = 'theme-switcher';
        switcher.innerHTML = `<span class="theme-label" style="color: var(--text-muted); font-size: 14px;">主题:</span>`;

        // 为每个主题创建按钮
        this.themes.forEach(theme => {
            const btn = document.createElement('button');
            btn.className = `theme-btn ${theme === this.currentTheme ? 'active' : ''}`;
            btn.setAttribute('data-theme', theme);
            btn.setAttribute('data-label', this.themeNames[theme]);
            btn.title = this.themeNames[theme] + '主题';
            btn.onclick = () => this.switchTheme(theme);
            switcher.appendChild(btn);
        });

        // 插入到导航栏中（"功能"旁边）
        const firstLink = navbar.querySelector('li');
        if (firstLink) {
            firstLink.insertAdjacentElement('afterend', switcher);
        } else {
            navbar.appendChild(switcher);
        }
    }

    /**
     * 切换主题
     */
    switchTheme(theme) {
        if (!this.themes.includes(theme)) return;

        // 更新按钮状态
        document.querySelectorAll('.theme-btn').forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute('data-theme') === theme);
        });

        // 应用主题
        this.applyTheme(theme);

        // 保存主题偏好
        this.saveTheme(theme);

        // 触发主题变化事件
        window.dispatchEvent(new CustomEvent('themeChanged', { 
            detail: { theme, themeName: this.themeNames[theme] }
        }));

        // 显示主题切换提示
        this.showToast(`已切换到「${this.themeNames[theme]}」主题`);
    }

    /**
     * 应用主题
     */
    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.currentTheme = theme;

        // 更新 meta theme-color
        const metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (metaThemeColor) {
            const colors = {
                'warm': '#fef9f3',
                'scifi': '#0a0e17',
                'feminine': '#fff5f8',
                'cyberpunk': '#0d0d0d'
            };
            metaThemeColor.content = colors[theme];
        }
    }

    /**
     * 保存主题到本地存储
     */
    saveTheme(theme) {
        try {
            localStorage.setItem('pandaco-theme', theme);
        } catch (e) {
            console.warn('无法保存主题设置');
        }
    }

    /**
     * 加载保存的主题
     */
    loadTheme() {
        try {
            const saved = localStorage.getItem('pandaco-theme');
            return this.themes.includes(saved) ? saved : 'warm';
        } catch (e) {
            return 'warm';
        }
    }

    /**
     * 监听系统主题变化
     */
    watchSystemTheme() {
        // 如果用户没有手动设置过主题，则跟随系统
        if (!localStorage.getItem('pandaco-theme')) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            if (mediaQuery.matches) {
                this.switchTheme('scifi'); // 深色系统默认科幻主题
            }
        }
    }

    /**
     * 显示提示消息
     */
    showToast(message) {
        // 移除已有的toast
        const existingToast = document.querySelector('.theme-toast');
        if (existingToast) {
            existingToast.remove();
        }

        // 创建新toast
        const toast = document.createElement('div');
        toast.className = 'theme-toast';
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            padding: 12px 24px;
            background: var(--bg-card);
            color: var(--text-primary);
            border-radius: 30px;
            box-shadow: var(--shadow-card);
            border: 1px solid var(--border-color);
            z-index: 10000;
            animation: slideUp 0.3s ease, fadeOut 0.3s ease 2s forwards;
        `;

        document.body.appendChild(toast);

        // 3秒后移除
        setTimeout(() => toast.remove(), 2500);
    }

    /**
     * 获取当前主题
     */
    getTheme() {
        return this.currentTheme;
    }

    /**
     * 获取当前主题名称
     */
    getThemeName() {
        return this.themeNames[this.currentTheme];
    }
}

// 添加动画样式
const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateX(-50%) translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
    }
    
    @keyframes fadeOut {
        to {
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// 初始化主题管理器
let themeManager;

// DOM 加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        themeManager = new ThemeManager();
    });
} else {
    themeManager = new ThemeManager();
}

// 导出供其他模块使用
window.ThemeManager = ThemeManager;
window.themeManager = themeManager;