---
name: btclawscan
description: OpenClaw 本地安全体检助手。一键全面扫描 OpenClaw 不安全配置、恶意 Skill 与漏洞；支持配置审计、技能审查、版本基线、隐私评估、网络出口扫描。纯本地检测，不依赖外部 API。
metadata: {"openclaw":{"homepage":"https://github.com/openclaw/openclaw","requires":{"bins":["openclaw","node","python3"]}}}
---

# BTclawScan - OpenClaw 本地安全体检助手

## 定位

纯本地 OpenClaw 安全扫描工具，不依赖任何外部 API，所有检测在本地完成。

## 触发边界

### 触发全面体检
- `开始安全体检` / `做一次安全体检`
- `开始安全扫描` / `全面安全检查`
- `给 OpenClaw 做安全体检`
- `BTclawScan` / `btclawscan`
- `安全体检` / `安全检查`

### 触发技能审查
- `这个技能安全吗`
- `帮我审查 XXX 技能`
- `预安装安全检查`
- `扫描 XXX 技能`

### 不触发
- 普通开发任务、环境配置、项目调试

## 运行方式

```bash
# 方式 1: 直接运行（推荐）
python3 <(grep -A 1000 '^```python$' ~/.openclaw/workspace/skills/btclawscan/SKILL.md | grep -B 1000 '^```$' | head -n -1 | tail -n +2)

# 方式 2: 提取后运行
grep -A 1000 '^```python$' SKILL.md | grep -B 1000 '^```$' | head -n -1 | tail -n +2 > scanner.py
python3 scanner.py
```

## 配置说明

所有配置内嵌在代码中，可在代码顶部修改：
- **RED_FLAGS** - 红旗行为检测规则
- **BLACKLIST_DOMAINS** - 恶意域名黑名单
- **WHITELIST_DOMAINS** - 可信域名白名单
- **VERSION_BASELINES** - 版本基线要求

## 风险评级

| 等级 | 标识 | 定义 | 行动 |
|------|------|------|------|
| 极高 | ⛔ | 发现严重恶意行为 | 立即禁用 |
| 高 | 🔴 | 存在严重风险 | 立即修复 |
| 中 | 🟡 | 需关注 | 审查后决定 |
| 低 | 🟢 | 安全 | 无需操作 |

## 隐私声明

本技能**纯本地运行**，不发送任何数据到外部服务器。

---

Paranoia is a feature. 🔒🦀

---

```python
#!/usr/bin/env python3
"""
BTclawScan - OpenClaw 本地安全体检助手
纯本地检测，不依赖外部 API
单文件设计 - 代码嵌入 SKILL.md
"""

import os
import re
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# ═══════════════════════════════════════════════════════
# 配置数据（内嵌，无需外部文件）
# ═══════════════════════════════════════════════════════

WORKSPACE_DIR = Path.home() / ".openclaw" / "workspace"
OPENCLAW_DIR = Path.home() / ".openclaw"

RISK_CRITICAL = "⛔"
RISK_HIGH = "🔴"
RISK_MEDIUM = "🟡"
RISK_LOW = "🟢"

# 红旗规则 (等级 | 正则模式 | 说明)
# 优化原则：只检测真正的风险行为，不过度告警正常功能
RED_FLAGS = [
    # 🚨 极高危 - 明确恶意行为
    (RISK_CRITICAL, r"subprocess\.call.*bash.*rm\s+-rf|os\.system.*rm\s+-rf", "危险删除命令"),
    (RISK_CRITICAL, r"~/.ssh/.*id_rsa|~/.aws/credentials", "敏感凭证文件访问"),
    (RISK_CRITICAL, r"eval\s*\([^)]*input\(|exec\s*\([^)]*input\(", "动态执行用户输入"),
    (RISK_CRITICAL, r"curl.*-d.*password|curl.*-d.*token|curl.*-d.*secret", "外传凭证"),
    
    # 🔴 高危 - 需重点审查
    (RISK_HIGH, r"sessions_history.*send|transcript.*exfil|history.*upload", "会话历史外传"),
    (RISK_HIGH, r"\bpassword\s*=\s*['\"][A-Za-z0-9]{8,}['\"]", "硬编码密码"),
    (RISK_HIGH, r"api_key\s*=\s*['\"][A-Za-z0-9]{16,}['\"]", "硬编码 API 密钥"),
    
    # 🟡 中危 - 高权限能力（但可能是正常的）
    (RISK_MEDIUM, r"subprocess\.call\s*\(|os\.system\s*\(", "系统命令执行"),
    (RISK_MEDIUM, r"MEMORY\.md.*write|USER\.md.*write", "核心文件写入"),
]

BLACKLIST_DOMAINS = {"malicious-domain.com", "evil-api.net"}
WHITELIST_DOMAINS = {
    "github.com", "36kr.com", "infoq.cn", "openclaw.ai",
    "clawhub.ai", "discord.com", "tencent.com", "aliyuncs.com"
}

CORE_FILES = ["MEMORY.md", "USER.md", "SOUL.md", "IDENTITY.md", "TOOLS.md", "AGENTS.md"]


class BTclawScan:
    def __init__(self):
        self.config_issues = []
        self.skill_issues = []
        self.network_issues = []
        self.counts = {RISK_CRITICAL: 0, RISK_HIGH: 0, RISK_MEDIUM: 0, RISK_LOW: 0}
        self.score = 100
    
    def get_system_info(self) -> Tuple[str, str, str]:
        """获取系统信息"""
        openclaw_ver = "未知"
        node_ver = "未知"
        os_info = "Linux"
        
        try:
            result = subprocess.run(["openclaw", "--version"], capture_output=True, text=True)
            openclaw_ver = result.stdout.strip().replace("OpenClaw ", "")
        except: pass
        
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            node_ver = result.stdout.strip()
        except: pass
        
        return openclaw_ver, node_ver, os_info
    
    def scan_config(self) -> List[Dict]:
        """模块 1: 配置审计"""
        results = []
        
        try:
            result = subprocess.run(["openclaw", "gateway", "status"], capture_output=True, text=True, timeout=10)
            if "running: true" in result.stdout:
                results.append({"status": "✅", "item": "Gateway 状态", "desc": "运行中"})
            else:
                results.append({"status": "⚠️", "item": "Gateway 状态", "desc": "未运行"})
                self.counts[RISK_MEDIUM] += 1
                self.score -= 5
        except:
            results.append({"status": "⚠️", "item": "Gateway 状态", "desc": "检查超时"})
            self.counts[RISK_MEDIUM] += 1
            self.score -= 5
        
        config_file = OPENCLAW_DIR / "config.json"
        if config_file.exists():
            try:
                with open(config_file) as f:
                    config = json.load(f)
                if "api_key" in config and config["api_key"]:
                    results.append({"status": "🔴", "item": "凭证存储", "desc": "发现明文 API key"})
                    self.config_issues.append("配置文件中存在明文 API key")
                    self.counts[RISK_HIGH] += 1
                    self.score -= 15
                else:
                    results.append({"status": "✅", "item": "凭证存储", "desc": "未发现明文 API key"})
            except: pass
        
        openclaw_json = WORKSPACE_DIR / "openclaw.json"
        if openclaw_json.exists():
            try:
                with open(openclaw_json) as f:
                    config = json.load(f)
                if config.get("elevated") is True:
                    results.append({"status": "🔴", "item": "会话安全", "desc": "elevated 模式已启用"})
                    self.config_issues.append("elevated 模式启用，存在提权风险")
                    self.counts[RISK_HIGH] += 1
                    self.score -= 15
                else:
                    results.append({"status": "✅", "item": "会话安全", "desc": "elevated 模式未启用"})
            except: pass
        
        return results
    
    def scan_skills(self) -> Tuple[List[Dict], int, int, int]:
        """模块 2: 技能审查"""
        skills_dir = WORKSPACE_DIR / "skills"
        if not skills_dir.exists():
            return [], 0, 0, 0
        
        skills = [d for d in skills_dir.iterdir() if d.is_dir()]
        safe_count = 0
        warning_count = 0
        dangerous_count = 0
        skill_details = []
        
        for skill_dir in skills:
            skill_name = skill_dir.name
            if skill_name == "btclawscan":
                continue
            
            skill_risk = "safe"
            skill_issues = []
            
            scripts_dir = skill_dir / "scripts"
            if scripts_dir.exists():
                for script_file in scripts_dir.rglob("*"):
                    if script_file.is_file():
                        try:
                            content = script_file.read_text(errors="ignore")
                            for level, pattern, desc in RED_FLAGS:
                                if re.search(pattern, content, re.IGNORECASE):
                                    skill_issues.append(f"{level} {desc}")
                                    if level == RISK_CRITICAL:
                                        skill_risk = "critical"
                                        self.counts[RISK_CRITICAL] += 1
                                    elif level == RISK_HIGH:
                                        if skill_risk != "critical":
                                            skill_risk = "high"
                                        self.counts[RISK_HIGH] += 1
                                    elif level == RISK_MEDIUM:
                                        if skill_risk == "safe":
                                            skill_risk = "medium"
                                        self.counts[RISK_MEDIUM] += 1
                        except: pass
            
            if skill_risk == "safe":
                safe_count += 1
            elif skill_risk in ["medium", "warning"]:
                warning_count += 1
                skill_details.append({"name": skill_name, "risk": "⚠️", "issues": skill_issues[:2]})
            else:
                dangerous_count += 1
                skill_details.append({"name": skill_name, "risk": "🔴", "issues": skill_issues[:2]})
                self.skill_issues.append(f"{skill_name}: {', '.join(skill_issues[:2])}")
                self.score -= 10
        
        return skill_details, safe_count, warning_count, dangerous_count
    
    def scan_versions(self) -> List[Dict]:
        """模块 3: 版本基线"""
        results = []
        
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            results.append({"status": "✅", "item": "Node.js", "desc": result.stdout.strip()})
        except:
            results.append({"status": "⚠️", "item": "Node.js", "desc": "未安装"})
            self.counts[RISK_MEDIUM] += 1
            self.score -= 5
        
        try:
            result = subprocess.run(["google-chrome", "--version"], capture_output=True, text=True)
            results.append({"status": "✅", "item": "Chrome", "desc": result.stdout.strip()})
        except:
            results.append({"status": "⚠️", "item": "Chrome", "desc": "未安装"})
        
        try:
            result = subprocess.run(["openclaw", "--version"], capture_output=True, text=True)
            results.append({"status": "✅", "item": "OpenClaw", "desc": result.stdout.strip()})
        except:
            results.append({"status": "⚠️", "item": "OpenClaw", "desc": "版本未知"})
        
        return results
    
    def scan_privacy(self) -> List[Dict]:
        """模块 4: 隐私评估"""
        results = []
        
        for file in CORE_FILES:
            file_path = WORKSPACE_DIR / file
            if file_path.exists():
                perms = oct(file_path.stat().st_mode)[-3:]
                if perms[0] in ["6", "7"]:
                    results.append({"status": "✅", "item": f"{file} 权限", "desc": f"{perms} (正常)"})
                else:
                    results.append({"status": "⚠️", "item": f"{file} 权限", "desc": f"{perms} (建议 644)"})
                    self.counts[RISK_MEDIUM] += 1
                    self.score -= 3
        
        if WORKSPACE_DIR.exists():
            perms = oct(WORKSPACE_DIR.stat().st_mode)[-3:]
            results.append({"status": "✅", "item": "Workspace 权限", "desc": f"{perms}"})
        
        return results
    
    def scan_network(self) -> Tuple[List[str], List[Dict]]:
        """模块 5: 网络出口"""
        skills_dir = WORKSPACE_DIR / "skills"
        if not skills_dir.exists():
            return [], []
        
        urls = set()
        url_pattern = re.compile(r'https?://[a-zA-Z0-9.-]+')
        
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and skill_dir.name != "btclawscan":
                scripts_dir = skill_dir / "scripts"
                if scripts_dir.exists():
                    for script_file in scripts_dir.rglob("*"):
                        if script_file.is_file():
                            try:
                                content = script_file.read_text(errors="ignore")
                                urls.update(url_pattern.findall(content))
                            except: pass
        
        network_details = []
        if urls:
            for url in sorted(urls):
                domain = url.replace("http://", "").replace("https://", "").split("/")[0]
                if domain in WHITELIST_DOMAINS:
                    network_details.append({"url": url, "status": "✅", "label": "白名单"})
                elif domain in BLACKLIST_DOMAINS:
                    network_details.append({"url": url, "status": "🔴", "label": "黑名单"})
                    self.network_issues.append(f"黑名单域名：{url}")
                    self.counts[RISK_HIGH] += 1
                    self.score -= 10
                else:
                    network_details.append({"url": url, "status": "⚠️", "label": "未分类"})
                    self.counts[RISK_MEDIUM] += 1
                    self.score -= 2
        
        return sorted(urls), network_details
    
    def get_overall_risk(self) -> str:
        """计算总体风险等级"""
        if self.score >= 90:
            return f"{RISK_LOW} 极低"
        elif self.score >= 70:
            return f"{RISK_LOW} 低"
        elif self.score >= 50:
            return f"{RISK_MEDIUM} 中等"
        elif self.score >= 30:
            return f"{RISK_HIGH} 高"
        else:
            return f"{RISK_CRITICAL} 极高"
    
    def generate_report(self) -> str:
        """生成专业格式报告"""
        openclaw_ver, node_ver, os_info = self.get_system_info()
        scan_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        skill_details, safe_count, warning_count, dangerous_count = self.scan_skills()
        network_urls, network_details = self.scan_network()
        
        report = []
        
        # 报告头部
        report.append("# 🏥 BTclawScan OpenClaw 安全体检报告")
        report.append("")
        report.append(f"📅 {scan_time}")
        report.append(f"🖥️ OpenClaw {openclaw_ver} · Node {node_ver} · {os_info}")
        report.append(f"📦 **安全评分：{self.score}/100** — 基于配置、技能、隐私、网络四维评估")
        report.append("")
        
        # 总览表格
        config_status = "⚠️ 风险" if self.config_issues else "✅ 通过"
        skill_status = "🔴 风险" if dangerous_count > 0 else ("⚠️ 需关注" if warning_count > 0 else "✅ 当前未见高风险")
        privacy_status = "⚠️ 需关注" if self.counts[RISK_MEDIUM] > 3 else "✅ 当前未见明显风险"
        overall = self.get_overall_risk()
        
        report.append("| 检查项 | 状态 | 详情 |")
        report.append("|--------|------|------|")
        report.append(f"| **配置审计** | {config_status} | {len(self.config_issues)} 项配置问题 |")
        report.append(f"| **Skill 风险** | {skill_status} | {dangerous_count} 个高危、{warning_count} 个需关注、{safe_count} 个安全 |")
        report.append(f"| **隐私泄露风险** | {privacy_status} | {self.counts[RISK_MEDIUM]} 项需关注 |")
        report.append(f"| **网络出口** | {'⚠️ 需关注' if network_details else '✅ 安全'} | {len(network_urls)} 个出口，{len([n for n in network_details if n['status']=='✅'])} 个白名单 |")
        report.append(f"| **综合评估** | **{overall}** | 建议优先修复高危配置问题 |")
        report.append("")
        
        # Step 1: 配置审计
        report.append("## Step 1: 配置审计")
        report.append("")
        config_results = self.scan_config()
        if config_results:
            report.append("| 状态 | 检查内容 | 风险与建议 |")
            report.append("|------|----------|------------|")
            for r in config_results:
                desc = r["desc"]
                if r["status"] == "✅":
                    report.append(f"| {r['status']} | {r['item']} | {desc} |")
                else:
                    report.append(f"| {r['status']} | {r['item']} | **需关注**：{desc}，建议检查配置 |")
        report.append("")
        
        # Step 2: Skill 供应链风险
        report.append("## Step 2: Skill 供应链风险（按风险等级排序）")
        report.append("")
        report.append(f"已检查 {safe_count + warning_count + dangerous_count} 个技能")
        report.append("")
        
        if skill_details:
            report.append("| Skill | 安全性 | 风险说明 |")
            report.append("|-------|--------|----------|")
            for skill in sorted(skill_details, key=lambda x: 0 if x["risk"]=="🔴" else 1):
                issues = "; ".join(skill["issues"]) if skill["issues"] else "未发现明确高风险"
                report.append(f"| `{skill['name']}` | {skill['risk']} | {issues} |")
        else:
            report.append("✅ 当前未发现明确高风险技能")
        report.append("")
        
        # Step 3: 版本基线
        report.append("## Step 3: 版本基线")
        report.append("")
        version_results = self.scan_versions()
        for r in version_results:
            report.append(f"- {r['status']} {r['item']}: {r['desc']}")
        report.append("")
        
        # Step 4: 隐私泄露风险检测
        report.append("## Step 4: 隐私泄露风险检测")
        report.append("")
        privacy_results = self.scan_privacy()
        if privacy_results:
            report.append("| 状态 | 检查内容 | 风险与建议 |")
            report.append("|------|----------|------------|")
            for r in privacy_results:
                if r["status"] == "✅":
                    report.append(f"| {r['status']} | {r['item']} | {r['desc']} |")
                else:
                    report.append(f"| {r['status']} | {r['item']} | **建议**：修改权限为 644 |")
        report.append("")
        
        # Step 5: 网络出口
        report.append("## Step 5: 网络出口")
        report.append("")
        if network_details:
            report.append("| 状态 | URL | 分类 |")
            report.append("|------|-----|------|")
            for n in network_details:
                report.append(f"| {n['status']} | `{n['url']}` | {n['label']} |")
        else:
            report.append("✅ 未发现网络出口")
        report.append("")
        
        # 修复建议
        report.append("---")
        report.append("")
        if self.config_issues or self.skill_issues or self.network_issues:
            report.append("## 🔧 修复建议")
            report.append("")
            report.append("**优先处理：**")
            for i, issue in enumerate(self.config_issues[:3], 1):
                report.append(f"{i}. {issue}")
            for i, issue in enumerate(self.skill_issues[:2], len(self.config_issues)+1):
                report.append(f"{i}. 审查技能：{issue}")
            for i, issue in enumerate(self.network_issues[:2], len(self.config_issues)+len(self.skill_issues)+1):
                report.append(f"{i}. {issue}")
        else:
            report.append("## ✅ 总结")
            report.append("")
            report.append("当前配置状态良好，继续保持！")
        
        report.append("")
        report.append("---")
        report.append("")
        report.append("*本报告由 BTclawScan 生成 · 纯本地检测，数据不出设备* 🔒")
        
        return "\n".join(report)
    
    def run(self) -> str:
        """执行扫描"""
        return self.generate_report()


if __name__ == "__main__":
    scanner = BTclawScan()
    print(scanner.run())
```
