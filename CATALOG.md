# 技能目录

> 此文件由 `python3 scripts/generate_catalog.py` 生成，请勿手工编辑。
> 状态仅表示仓库静态检查通过，不代表技能已完成运行时或外部服务集成测试。

共 36 个 tracked 技能。

## 飞书与 Lark

| 技能 | 路径 | 状态 | 描述 |
|---|---|---|---|
| `feishu-card` | [`feishu-card/SKILL.md`](feishu-card/SKILL.md) | 静态检查 | Send rich interactive cards to Feishu (Lark) users or groups. Supports Markdown, titles, color headers, and buttons. Use when sending rich-formatted messages to Feishu with visual elements. |
| `feishu-doc-editor` | [`feishu-doc-editor/SKILL.md`](feishu-doc-editor/SKILL.md) | 静态检查 | Feishu document creation and editing operations using OpenAPI. Activate when user needs to create, edit, or read Feishu documents programmatically. |
| `feishu-doc-manager` | [`feishu-doc-manager/SKILL.md`](feishu-doc-manager/SKILL.md) | 静态检查 | 📄 Feishu Doc Manager \| 飞书文档管理器 Seamlessly publish Markdown content to Feishu Docs with automatic formatting. Solves key pain points: Markdown table conversion, permission management, batch writing. 将 Markdown 内容无缝发布到飞书文档，自动渲染格式。 解决核心痛点：Markdown 表格转换、权限管理、批量写入。 |
| `feishu-file-sender` | [`feishu-file-sender/SKILL.md`](feishu-file-sender/SKILL.md) | 静态检查 | 飞书文件发送器 — 补齐飞书渠道缺失的文件投递能力，通过飞书 OpenAPI 上传并发送 agent 生成的本地文件。\| Feishu File Sender — Upload & send files via Feishu OpenAPI, filling the channel's missing file delivery. |
| `feishu-sheets` | [`feishu-sheets-skill/SKILL.md`](feishu-sheets-skill/SKILL.md) | 静态检查 | Feishu online spreadsheet (Sheets) operations including create, read, write, append data, manage worksheets. Use when user mentions Feishu Sheets, online spreadsheet, electronic spreadsheet (not Bitable/multi-dimensional table). Supports: create spreadsheet, write/read cell values, append rows, insert/delete rows/columns, manage worksheets. |
| `feishu-toolkit` | [`feishu-toolkit/SKILL.md`](feishu-toolkit/SKILL.md) | 静态检查 | Complete Feishu (Lark) integration toolkit for AI agents. Read/write documents, fetch chat history, send files & screenshots, manage permissions, and create scheduled reminders. Supports Wiki, Docs, Sheets, Bitable, and IM operations. Triggers: "飞书", "feishu", "lark", "读文档", "群聊记录", "发文件", "截屏发飞书", "文档权限", "定时提醒". |
| `lark-approval` | [`lark-approval/SKILL.md`](lark-approval/SKILL.md) | 静态检查 | 飞书审批 API：审批实例、审批任务管理。 |
| `lark-base` | [`lark-base/SKILL.md`](lark-base/SKILL.md) | 静态检查 | 当需要用 lark-cli 操作飞书多维表格（Base）时调用：适用于建表、字段管理、记录读写、视图配置、历史查询，以及角色/表单/仪表盘管理/工作流；也适用于把旧的 +table / +field / +record 写法改成当前命令写法。涉及字段设计、公式字段、查找引用、跨表计算、行级派生指标、数据分析需求时也必须使用本 skill。 |
| `lark-calendar` | [`lark-calendar/SKILL.md`](lark-calendar/SKILL.md) | 静态检查 | 飞书日历（calendar）：提供日历与日程（会议）的全面管理能力。核心场景包括：查看/搜索日程、创建/更新日程、管理参会人、查询忙闲状态及推荐空闲时段。高频操作请优先使用 Shortcuts：+agenda（快速概览今日/近期行程）、+create（创建日程并按需邀请参会人）、+freebusy（查询用户主日历的忙闲信息和rsvp的状态）、+rsvp（回复日程邀请）、+suggestion（针对时间未确定的预约日程需求，提供多个时间推荐方案）。 |
| `lark-contact` | [`lark-contact/SKILL.md`](lark-contact/SKILL.md) | 静态检查 | 飞书通讯录：查询组织架构、人员信息和搜索员工。获取当前用户或指定用户的详细信息、通过关键词搜索员工（姓名/邮箱/手机号）。当用户需要查看个人信息、查找同事 open_id 或联系方式、按姓名搜索员工、查询部门结构时使用。 |
| `lark-doc` | [`lark-doc/SKILL.md`](lark-doc/SKILL.md) | 静态检查 | 飞书云文档：创建和编辑飞书文档。从 Markdown 创建文档、获取文档内容、更新文档（追加/覆盖/替换/插入/删除）、上传和下载文档中的图片和文件、搜索云空间文档。当用户需要创建或编辑飞书文档、读取文档内容、在文档中插入图片、搜索云空间文档时使用；如果用户是想按名称或关键词先定位电子表格、报表等云空间对象，也优先使用本 skill 的 docs +search 做资源发现。 |
| `lark-drive` | [`lark-drive/SKILL.md`](lark-drive/SKILL.md) | 静态检查 | 飞书云空间：管理云空间中的文件和文件夹。上传和下载文件、创建文件夹、复制/移动/删除文件、查看文件元数据、管理文档评论、管理文档权限、订阅用户评论变更事件；也负责把本地 Word/Markdown/Excel/CSV 导入为飞书在线云文档（docx、sheet、bitable）。当用户需要上传或下载文件、整理云空间目录、查看文件详情、管理评论、管理文档权限、订阅用户评论变更事件，或要把本地文件导入成新版文档、电子表格、多维表格/Base 时使用。 |
| `lark-event` | [`lark-event/SKILL.md`](lark-event/SKILL.md) | 静态检查 | 飞书事件订阅：通过 WebSocket 长连接实时监听飞书事件（消息、通讯录变更、日历变更等），输出 NDJSON 到 stdout，支持 compact Agent 友好格式、正则路由、文件输出。当用户需要实时监听飞书事件、构建事件驱动管道时使用。 |
| `lark-im` | [`lark-im/SKILL.md`](lark-im/SKILL.md) | 静态检查 | 飞书即时通讯：收发消息和管理群聊。发送和回复消息、搜索聊天记录、管理群聊成员、上传下载图片和文件、管理表情回复。当用户需要发消息、查看或搜索聊天记录、下载聊天中的文件、查看群成员时使用。 |
| `lark-mail` | [`lark-mail/SKILL.md`](lark-mail/SKILL.md) | 静态检查 | 飞书邮箱 — draft, compose, send, reply, forward, read, and search emails; manage drafts, folders, labels, contacts, attachments, and mail rules. Use when user mentions 起草邮件, 写一封邮件, 拟邮件, 草稿, 发通知邮件, 发送邮件, 发邮件, 回复邮件, 转发邮件, 查看邮件, 看邮件, 读邮件, 搜索邮件, 查邮件, 收件箱, 邮件会话, 编辑草稿, 管理草稿, 下载附件, 邮件文件夹, 邮件标签, 邮件联系人, 监听新邮件, 收信规则, 邮件规则, draft, compose, send email, reply, forward, inbox, mail thread, mail rules. |
| `lark-minutes` | [`lark-minutes/SKILL.md`](lark-minutes/SKILL.md) | 静态检查 | 飞书妙记：获取妙记基础信息（标题、封面、时长）和相关的 AI 产物（总结、待办、章节），下载妙记音视频文件。Use when 用户需要查看妙记信息、下载妙记音视频或搜索妙记列表时触发。 |
| `lark-openapi-explorer` | [`lark-openapi-explorer/SKILL.md`](lark-openapi-explorer/SKILL.md) | 静态检查 | 飞书/Lark 原生 OpenAPI 探索：从官方文档库中挖掘未经 CLI 封装的原生 OpenAPI 接口。当用户的需求无法被现有 lark-* skill 或 lark-cli 已注册命令满足，需要查找并调用原生飞书 OpenAPI 时使用。 |
| `lark-shared` | [`lark-shared/SKILL.md`](lark-shared/SKILL.md) | 静态检查 | 飞书/Lark CLI 共享基础：应用配置初始化、认证登录（auth login）、身份切换（--as user/bot）、权限与 scope 管理、Permission denied 错误处理、安全规则。当用户需要第一次配置(`lark-cli config init`)、使用登录授权(`lark-cli auth login`)、遇到权限不足、切换 user/bot 身份、配置 scope、或首次使用 lark-cli 时触发。 |
| `lark-sheets` | [`lark-sheets/SKILL.md`](lark-sheets/SKILL.md) | 静态检查 | 飞书电子表格：创建和操作电子表格。创建表格并写入表头和数据、读取和写入单元格、追加行数据、在已知电子表格中查找单元格内容、导出表格文件。当用户需要创建电子表格、批量读写数据、在已知表格中查找内容、导出或下载表格时使用。若用户是想按名称或关键词搜索云空间里的表格文件，请改用 lark-doc 的 docs +search 先定位资源。 |
| `lark-skill-maker` | [`lark-skill-maker/SKILL.md`](lark-skill-maker/SKILL.md) | 静态检查 | 创建 lark-cli 的自定义 Skill。当用户需要把飞书 API 操作封装成可复用的 Skill（包装原子 API 或编排多步流程）时使用。 |
| `lark-task` | [`lark-task/SKILL.md`](lark-task/SKILL.md) | 静态检查 | 飞书任务：管理任务和清单。创建待办任务、查看和更新任务状态、拆分子任务、组织任务清单、分配协作成员。当用户需要创建待办事项、查看任务列表、跟踪任务进度、管理项目清单或给他人分配任务时使用。 |
| `lark-vc` | [`lark-vc/SKILL.md`](lark-vc/SKILL.md) | 静态检查 | 飞书视频会议：查询会议记录、获取会议纪要产物（总结、待办、章节、逐字稿）。1. 查询已经结束的会议数量或详情时使用本技能(如昨天 \| 上周 \| 今天已经开过的会议等场景)，查询未开始的会议日程使用 lark-calendar 技能。2. 支持通过关键词、时间范围、组织者、参与者、会议室等筛选条件搜索会议记录。3. 获取或整理会议纪要时使用本技能。 |
| `lark-whiteboard` | [`lark-whiteboard/SKILL.md`](lark-whiteboard/SKILL.md) | 静态检查 | 当用户要求在飞书云文档中绘制图表，或使用飞书画板绘制架构图、流程图、思维导图、时序图或其他可视化图表时使用此 skill。 |
| `lark-wiki` | [`lark-wiki/SKILL.md`](lark-wiki/SKILL.md) | 静态检查 | 飞书知识库：管理知识空间和文档节点。创建和查询知识空间、管理节点层级结构、在知识库中组织文档和快捷方式。当用户需要在知识库中查找或创建文档、浏览知识空间结构、移动或复制节点时使用。 |
| `lark-workflow-meeting-summary` | [`lark-workflow-meeting-summary/SKILL.md`](lark-workflow-meeting-summary/SKILL.md) | 静态检查 | 会议纪要整理工作流：汇总指定时间范围内的会议纪要并生成结构化报告。当用户需要整理会议纪要、生成会议周报、回顾一段时间内的会议内容时使用。 |
| `lark-workflow-standup-report` | [`lark-workflow-standup-report/SKILL.md`](lark-workflow-standup-report/SKILL.md) | 静态检查 | 日程待办摘要：编排 calendar +agenda 和 task +get-my-tasks，生成指定日期的日程与未完成任务摘要。适用于了解今天/明天/本周的安排。 |
| `skill-feishu-manager` | [`skill-feishu-manager/SKILL.md`](skill-feishu-manager/SKILL.md) | 静态检查 | Comprehensive Feishu (飞书) management toolkit for documents, knowledge bases, bitables, and cloud storage. |

## 内容与电商

| 技能 | 路径 | 状态 | 描述 |
|---|---|---|---|
| `douyin-ecommerce-operations` | [`douyin-ecommerce-operations/SKILL.md`](douyin-ecommerce-operations/SKILL.md) | 静态检查 | 抖音电商运营专家 - 基于王总飞书知识库的专业运营方法论，涵盖店铺运营、直播带货、短视频营销、用户分层运营、货品管理等全链路能力。 |
| `douyin-parser` | [`douyin-parser/SKILL.md`](douyin-parser/SKILL.md) | 静态检查 | 解析抖音链接，获取无水印视频/图集下载地址。Use when 用户发送抖音链接、要求"解析抖音"、"下载抖音"或分析抖音视频时触发。 |
| `douyin-publish` | [`douyin-publish/SKILL.md`](douyin-publish/SKILL.md) | 静态检查 | 自动化发布抖音视频/图文，支持定时发布。Use when 用户要求发布抖音视频、图文或定时发布时触发。 |
| `tikhub-sign` | [`tikhub-sign/SKILL.md`](tikhub-sign/SKILL.md) | 静态检查 | TikHub每日签到提醒与额度查询。Use when 用户要求"签到"、"每日签到"或定时任务触发时使用。 |

## 机器学习

| 技能 | 路径 | 状态 | 描述 |
|---|---|---|---|
| `peft-fine-tuning` | [`mlops/training/peft/SKILL.md`](mlops/training/peft/SKILL.md) | 静态检查 | Parameter-efficient fine-tuning for LLMs using LoRA, QLoRA, and 25+ methods. Use when fine-tuning large models (7B-70B) with limited GPU memory, when you need to train <1% of parameters with minimal accuracy loss, or for multi-adapter serving. HuggingFace's official library integrated with transformers ecosystem. |
| `pytorch-fsdp` | [`mlops/training/pytorch-fsdp/SKILL.md`](mlops/training/pytorch-fsdp/SKILL.md) | 静态检查 | Expert guidance for Fully Sharded Data Parallel training with PyTorch FSDP - parameter sharding, mixed precision, CPU offloading, FSDP2. Use when training large models on multiple GPUs, implementing distributed training, or debugging FSDP issues. |

## 通用工具

| 技能 | 路径 | 状态 | 描述 |
|---|---|---|---|
| `agent-handoff` | [`agent-handoff/SKILL.md`](agent-handoff/SKILL.md) | 静态检查 | 智能体交接协议：两个 AI 智能体通过一个共享交接区异步协作——文件放在共享云盘文件夹，任务登记在共享看板。当需要查看对方交接给你的任务、认领并处理任务、把成果交付回交接区、向对方发起新任务，或执行首次连接握手时使用。 |
| `btclawscan` | [`btclawscan/SKILL.md`](btclawscan/SKILL.md) | 静态检查 | OpenClaw 本地安全体检助手。一键全面扫描 OpenClaw 不安全配置、恶意 Skill 与漏洞；支持配置审计、技能审查、版本基线、隐私评估、网络出口扫描。纯本地检测，不依赖外部 API。 |
| `novel-creator` | [`creative/novel-creator/SKILL.md`](creative/novel-creator/SKILL.md) | 静态检查 | 全能小说创作引擎。融合设定管理、伏笔追踪、多模型审阅、6维度评分、飞书同步。Use when 用户要求写小说、创作故事、规划大纲、设定角色、评分作品、管理长篇连载时触发。 |
