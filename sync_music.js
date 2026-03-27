#!/usr/bin/env node
/**
 * 🎵 音乐双库同步工具
 * 自动将本地音乐同步到 GitHub 和 Gitee
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const MUSIC_DIR = '/root/pandaco-music';
const LOCAL_MUSIC = '/root/eat/public/music';
const LOCAL_DATA = '/root/eat/data/music.json';

console.log('🎵 开始同步音乐到双库...\n');

// 递归复制目录
function copyDir(src, dest) {
    if (!fs.existsSync(dest)) {
        fs.mkdirSync(dest, { recursive: true });
    }
    const entries = fs.readdirSync(src, { withFileTypes: true });
    for (const entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);
        if (entry.isDirectory()) {
            copyDir(srcPath, destPath);
        } else if (entry.name.endsWith('.mp3') || entry.name.endsWith('.mp4') || entry.name.endsWith('.wav') || entry.name.endsWith('.json')) {
            fs.copyFileSync(srcPath, destPath);
            console.log(`  ✅ ${path.relative(LOCAL_MUSIC, srcPath) || entry.name}`);
        }
    }
}

// 1. 复制音乐文件
console.log('📁 复制音乐文件...');
try {
    copyDir(LOCAL_MUSIC, MUSIC_DIR);
} catch (e) {
    console.error('❌ 复制失败:', e.message);
}

// 2. 复制 music.json
fs.copyFileSync(LOCAL_DATA, path.join(MUSIC_DIR, 'music.json'));
console.log('  ✅ music.json\n');

// 3. Git 操作
process.chdir(MUSIC_DIR);

console.log('📤 推送到 GitHub...');
try {
    execSync('git add .', { stdio: 'inherit' });
    execSync('git commit -m "🎵 同步音乐库 - ' + new Date().toLocaleString('zh-CN') + '"', { stdio: 'inherit' });
    execSync('git push github main', { stdio: 'inherit' });
    console.log('✅ GitHub 同步成功\n');
} catch (e) {
    console.log('⚠️ GitHub 无变更或失败\n');
}

console.log('📤 推送到 Gitee...');
try {
    execSync('git push gitee main', { stdio: 'inherit' });
    console.log('✅ Gitee 同步成功\n');
} catch (e) {
    console.log('⚠️ Gitee 同步失败\n');
}

console.log('🎉 双库同步完成！');
console.log('  GitHub: https://github.com/ziwei-control/pandaco-music');
console.log('  Gitee:  https://gitee.com/pandac0/pandaco-music');