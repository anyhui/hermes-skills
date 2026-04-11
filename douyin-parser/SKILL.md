---
name: douyin-parser
description: 解析抖音链接，获取无水印视频/图集下载地址。Use when 用户发送抖音链接、要求"解析抖音"、"下载抖音"或分析抖音视频时触发。
---

# douyin-parser - 抖音解析 Skill

## 触发条件

- 抖音链接（douyin.com、v.douyin.com）
- "解析抖音"、"下载抖音"
- 抖音视频分析请求

## 验证可用的技术方案

### 方案：jiji262/douyin-downloader + Cookie（✅ 已验证可用）

**已部署位置**：`/root/.openclaw/workspace/douyin-downloader/`

**使用方法**：

1. **获取 Cookie**：浏览器登录抖音 → F12 → Application → Cookies → 复制值
   - `msToken`, `ttwid`, `odin_tt`, `passport_csrf_token`, `sid_guard`

2. **配置 Cookie**（更新 config.yml）：
   ```yaml
   cookies:
     msToken: "你的msToken值"
     ttwid: "你的ttwid值"
     # ...
   ```

3. **解析视频**：
   ```bash
   cd /root/.openclaw/workspace/douyin-downloader
   source .venv/bin/activate
   python run.py -c config.yml -u "抖音链接" -p /tmp/douyin_output
   ```

4. **从 JSON 提取地址**：
   ```bash
   find /tmp/douyin_output -name "*_data.json" -type f
   cat "/tmp/douyin_output/作者名/视频标题文件夹/*_data.json" | python3 -c "
   import json, sys
   data = json.load(sys.stdin)
   if 'video' in data and 'play_addr' in data['video']:
       urls = data['video']['play_addr'].get('url_list', [])
       if urls: print(urls[0])
   "
   ```

## 解析流程

1. **短链转正式链接**：
   ```bash
   curl -sL "https://v.douyin.com/xxx/" -w "%{url_effective}" -o /dev/null
   ```

2. **调用 douyin-downloader 下载**

3. **从 JSON 提取无水印地址**：
   - video 类型: `data['video']['play_addr']['url_list'][0]`
   - image_album 类型: `data['images'][0]['download_url_list'][0]`

4. **验证地址可下载**：
   ```bash
   curl -sI "提取的地址" | head -3
   ```

## 常见问题

- **地址打不开？** 尝试 `url_list` 中的其他 URL
- **Cookie 过期？** 重新获取并更新 config.yml