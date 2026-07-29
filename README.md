# Hermes Skills Collection

面向 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 的社区技能集合。当前仓库包含 35 个 tracked `SKILL.md`；完整名称、路径、描述和分类见 [CATALOG.md](CATALOG.md)。

## 安装

先安装并配置 Hermes：

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
```

然后克隆本仓库，并将需要的技能目录复制或软链接到 `~/.hermes/skills/`。例如：

```bash
git clone --no-recurse-submodules https://github.com/anyhui/hermes-skills.git
mkdir -p ~/.hermes/skills
cp -R hermes-skills/lark-calendar ~/.hermes/skills/
```

重启 Hermes 后可用 `/skills` 查看已发现技能。仅安装可信技能，并在执行前审阅其 `SKILL.md`、脚本和权限需求。

## 验证状态

`python3 scripts/validate_repo.py` 对 tracked 文件执行静态检查：技能 frontmatter、名称唯一性、本地 Markdown 链接、JSON、Python 编译、常见秘密特征、大文件和生成目录新鲜度。`CATALOG.md` 中的“静态检查”只表示这些规则通过，不表示技能已在 Hermes、飞书、抖音或其他外部服务中完成运行时测试。

运行仓库管理检查：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_repo.py
python3 scripts/generate_catalog.py --check
```

管理脚本仅依赖 Python 3.10+ 标准库和 Git。具体技能可能额外需要 Node.js、`lark-cli`、平台凭据、网络访问或其他工具，请以对应 `SKILL.md` 为准。

## Gitlinks

`deep-research`、`web-access`、`zhangxuefeng` 在 Git 索引中是 mode `160000` gitlink。仓库没有提供可用于初始化它们的 `.gitmodules` 映射，因此验证器将其报告为 gitlink 且不遍历其内容；它们不计入上述 35 个 tracked `SKILL.md`。如需使用，请先从各自来源取得内容并核验许可证与安全性。

## 参与和许可

贡献流程见 [CONTRIBUTING.md](CONTRIBUTING.md)，安全问题见 [SECURITY.md](SECURITY.md)，版本记录见 [CHANGELOG.md](CHANGELOG.md)。[LICENSE](LICENSE) 只覆盖本仓库新编写的管理层文件；既有技能及 gitlink 内容不被统一重新许可，详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
