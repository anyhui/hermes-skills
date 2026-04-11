---
name: tikhub-sign
description: TikHub每日签到提醒与额度查询。Use when 用户要求"签到"、"每日签到"或定时任务触发时使用。
---

# tikhub-sign - TikHub 签到 Skill

## 触发条件

- "签到"、"每日签到"、"领免费额度"
- 定时任务触发（每天自动执行）

## 签到方式

### 方式一：网站签到（手动）

1. 访问 https://user.tikhub.io
2. 登录后进入个人中心
3. 每日签到可获取免费额度

### 方式二：API 查询使用量

⚠️ TikHub API 目前无公开签到接口，但可查询使用量：
```bash
curl -H "Authorization: Bearer $API_KEY" \
  https://api.tikhub.io/api/v1/tikhub/user/get_user_daily_usage
```

## 定时任务配置

已配置每日 9:00 飞书提醒：
```yaml
cron:
  - name: "tikhub-sign-reminder"
    schedule: "0 9 * * *"
    action: message
    to: feishu
    message: "🎯 TikHub 签到提醒！点击 https://user.tikhub.io 签到"
```

## 相关信息

- TikHub 官网：https://tikhub.io
- 用户中心：https://user.tikhub.io
- API 文档：https://api.tikhub.io/docs
- 邀请码：1wRL8eQk