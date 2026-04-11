---
name: douyin-publish
description: 自动化发布抖音视频/图文，支持定时发布。Use when 用户要求发布抖音视频、图文或定时发布时触发。
---

# douyin-publish - 抖音发布 Skill

## 推荐项目：social-auto-upload ⭐

**GitHub**：https://github.com/dreammis/dreammis/social-auto-upload  
**Stars**：9k+ ⭐⭐⭐⭐⭐

## 支持的功能

| 平台 | 视频上传 | 图文上传 | 定时发布 | CLI |
|------|---------|---------|---------|-----|
| 抖音 | ✅ | ✅ | ✅ | ✅ |
| 小红书 | ✅ | ✅ | ✅ | ✅ |
| 快手 | ✅ | ✅ | ✅ | ✅ |
| Bilibili | ✅ | ❌ | ✅ | ✅ |

## 安装步骤

```bash
git clone https://github.com/dreammis/social-auto-upload.git
cd social-auto-upload
uv sync

# 安装浏览器驱动
pip install patchright
patchright install chromium
```

## CLI 常用命令

**登录账号**：
```bash
sau douyin login --account my_account
```

**检查 Cookie**：
```bash
sau douyin check --account my_account
```

**上传视频**：
```bash
sau douyin upload-video --account my_account --file demo.mp4 --title "标题" --desc "简介"
```

**上传图文**：
```bash
sau douyin upload-note --account my_account --images 1.png 2.png --title "标题" --note "正文"
```

## 关键特性

- **无头模式**：支持服务器后台运行
- **多平台**：抖音、小红书、快手、B站等
- **定时发布**：支持定时任务
- **Skill 化**：项目自带 OpenClaw Skill