# 贡献指南

## 提交变更

1. 保持改动聚焦；不要在未确认来源和许可的情况下复制第三方技能。
2. 技能 `name` 使用唯一的 lowercase kebab-case，`description` 清楚说明用途和触发场景。
3. 不提交令牌、密码、私钥、个人数据或真实生产凭据；测试只能使用明确的合成夹具。
4. 修改技能或管理逻辑后重新生成 `CATALOG.md`。
5. 使用 Conventional Commits，例如 `feat: add repository validation` 或 `fix: repair local skill link`。

## 本地检查

需要 Python 3.10+ 和 Git，无第三方 Python 依赖：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/generate_catalog.py
python3 scripts/generate_catalog.py --check
python3 scripts/validate_repo.py
python3 -m compileall -q scripts tests
```

新增验证规则时先添加失败测试，再实现最小修复。目录必须由生成器更新，不接受手工维护。

## 第三方内容

提交者必须保留上游作者、来源、许可证和通知。来源不明或许可证不兼容的内容应先在 issue 中讨论；本仓库的管理层许可证不会自动覆盖技能内容。
