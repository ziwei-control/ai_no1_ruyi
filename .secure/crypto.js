/**
 * 本地敏感信息加密存储模块
 * 使用 AES-256-CBC 加密算法
 * 密钥基于本机特征生成，本机自动解密，外界无法访问
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const os = require('os');

const SECURE_DIR = path.join(os.homedir(), '.copaw', '.secure');
const VAULT_FILE = path.join(SECURE_DIR, 'vault.enc');
const KEY_FILE = path.join(SECURE_DIR, '.key');

// 生成本机特征密钥（基于本机信息）
function generateMachineKey() {
  const machineId = os.hostname() + os.userInfo().username + process.getuid?.() || '1000';
  return crypto.createHash('sha256').update(machineId + 'copaw_secure_vault').digest();
}

// 获取或创建密钥
function getKey() {
  if (fs.existsSync(KEY_FILE)) {
    return fs.readFileSync(KEY_FILE);
  }
  const key = generateMachineKey();
  fs.writeFileSync(KEY_FILE, key, { mode: 0o600 });
  return key;
}

// 加密数据
function encrypt(text) {
  const key = getKey();
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return iv.toString('hex') + ':' + encrypted;
}

// 解密数据
function decrypt(encryptedText) {
  const key = getKey();
  const parts = encryptedText.split(':');
  const iv = Buffer.from(parts[0], 'hex');
  const encrypted = parts[1];
  const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}

// 保存到保险库
function saveVault(data) {
  const json = JSON.stringify(data, null, 2);
  const encrypted = encrypt(json);
  fs.writeFileSync(VAULT_FILE, encrypted, { mode: 0o600 });
  console.log('✅ 保险库已加密保存');
}

// 读取保险库
function loadVault() {
  if (!fs.existsSync(VAULT_FILE)) {
    return null;
  }
  const encrypted = fs.readFileSync(VAULT_FILE, 'utf8');
  const decrypted = decrypt(encrypted);
  return JSON.parse(decrypted);
}

// 获取指定密钥的值（自动解密）
function get(key) {
  const vault = loadVault();
  return vault ? vault[key] : null;
}

// 设置指定密钥的值（自动加密保存）
function set(key, value) {
  let vault = loadVault() || {};
  vault[key] = value;
  saveVault(vault);
}

module.exports = { get, set, loadVault, saveVault, encrypt, decrypt };