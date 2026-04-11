# Hermes Skills Collection

Hermes Agent 精选技能集合，包含飞书集成、抖音运营、数据访问等核心能力。

## 技能列表

### 🎬 抖音相关

| 技能 | 功能 | 说明 |
|------|------|------|
| `douyin-parser` | 抖音解析 | 解析抖音链接，获取无水印视频/图集下载地址 |
| `douyin-publish` | 抖音发布 | 自动化发布抖音视频/图文，支持定时发布 |
| `douyin-ecommerce-operations` | 抖音电商运营 | 基于专业运营方法论，涵盖店铺运营、直播带货、短视频营销 |
| `douyin-drama-commerce-skill` | 剧情带货脚本 | 生成有故事深度、视觉张力、情感共鸣的带货脚本 |

### 📱 飞书/Lark 集成

| 技能 | 功能 | 说明 |
|------|------|------|
| `feishu-card` | 飞书卡片 | 发送富交互卡片消息 |
| `feishu-toolkit` | 飞书工具集 | 完整的飞书集成工具包 |
| `lark-doc` | 飞书文档 | 创建和编辑飞书云文档 |
| `lark-sheets` | 飞书表格 | 操作飞书在线电子表格 |
| `lark-base` | 飞书多维表格 | 管理多维表格数据 |
| `lark-calendar` | 飞书日历 | 日程和会议管理 |
| `lark-im` | 飞书即时通讯 | 消息收发和群聊管理 |
| `lark-minutes` | 飞书妙记 | 获取妙记信息和AI产物 |
| `lark-vc` | 飞书视频会议 | 会议纪要和记录 |
| `lark-wiki` | 飞书知识库 | 管理知识空间和文档节点 |

### 🌐 数据访问

| 技能 | 功能 | 说明 |
|------|------|------|
| `web-access` | 网页访问 | 搜索、网页抓取、浏览器自动化 |
| `deep-research` | 深度研究 | 多源深度研究智能体 |

### 🔧 工具类

| 技能 | 功能 | 说明 |
|------|------|------|
| `tikhub-sign` | TikHub签到 | 每日签到提醒和额度查询 |
| `zhangxuefeng` | 张雪峰思维 | 基于张雪峰方法论的表达框架 |
| `btclawscan` | 安全扫描 | OpenClaw本地安全体检 |

### 🤖 MLops 训练

| 技能 | 功能 | 说明 |
|------|------|------|
| `mlops/training/peft` | PEFT微调 | 使用LoRA/QLoRA进行参数高效微调 |
| `mlops/training/pytorch-fsdp` | FSDP训练 | PyTorch完全分片数据并行训练 |

### 📚 小说创作

| 技能 | 功能 | 说明 |
|------|------|------|
| `novel-creator` | 全能创作引擎 | 设定管理、伏笔追踪、6维度评分、飞书同步 |

## 技能规范

所有技能遵循 **skill-creator 三级加载框架**：

```
┌─────────────────────────────────────────────────────┐
│ Meta Layer (始终加载, ~100字)                        │
│ - name: hyphen-case, ≤64字符                         │
│ - description: 含触发场景, ≤1024字符                 │
├─────────────────────────────────────────────────────┤
│ Body Layer (触发时加载, <5KB)                        │
│ - SKILL.md 核心内容                                  │
│ - 快速入门、核心概念、常用模式                        │
├─────────────────────────────────────────────────────┤
│ Resources Layer (按需加载)                           │
│ - scripts/ 可执行脚本                                │
│ - references/ 参考文档                               │
│ - assets/ 输出资源                                   │
└─────────────────────────────────────────────────────┘
```

## 更新日志

### 2026-04-11
- ✅ 为 `douyin-parser`、`douyin-publish`、`tikhub-sign` 添加标准frontmatter
- ✅ 修复 `lark-minutes` description格式
- ✅ 精简 `pytorch-fsdp` (160KB → 3.4KB)
- ✅ 修复 `feishu-card` frontmatter
- ✅ 新建 `novel-creator` 技能（融合多技能核心能力）

### 2026-04-10
- 初始导入OpenClaw技能集合
- 创建技能仓库

## 安装方法

```bash
# 克隆到本地
git clone https://github.com/anyhui/hermes-skills.git

# 或使用skillhub安装单个技能
skillhub install <skill-name>
```

## 许可证

MIT License