#!/usr/bin/env python3
"""Validate the shaoxingshiye skill without third-party packages."""

from __future__ import annotations

import re
import subprocess
import sys
from math import ceil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
SKILL_MAX_LINES = 150
SKILL_MAX_CHARACTERS = 6_000
SKILL_MAX_APPROX_TOKENS = 4_500

REQUIRED_KNOWLEDGE = (
    "01-证据分级与使用边界.md",
    "02-领导关系：LMX、家长式领导、信任与追随.md",
    "03-影响与说服：上行影响、议题销售、政治技能与谈判.md",
    "04-反馈、冲突与情绪调节的科学.md",
    "05-职场自我保护：劳动法、证据与依法退出.md",
    "06-霸凌、骚扰与毒性环境.md",
    "07-中国职场文化：人情、面子与公文规范.md",
    "08-古典进谏智慧与伦理转译.md",
    "09-核心书单与论文索引.md",
)

REQUIRED_PRACTICAL = (
    "00-导读与使用分级.md",
    "01-向上汇报与请示.md",
    "02-表达分歧与向上提意见.md",
    "03-跨部门协作与催办.md",
    "04-难相处同事与毒性领导应对.md",
    "05-被批评、背锅与情绪急救.md",
    "06-证据留存与防背锅清单.md",
    "07-离职、裁员与谈判.md",
    "08-职场档案与长期记忆.md",
    "09-求职面试与入职适应.md",
    "10-加薪晋升与向上谈判.md",
    "11-会议发言与团队协作.md",
    "12-待人接物：做客待客与人情往来.md",
    "13-展示价值与可见度.md",
    "14-带团队：新经理与管理基本功.md",
    "15-行业语境速查：工程建设与通信网络.md",
    "16-沉默的艺术：何时不说与不回复.md",
    "17-对话演练：预演、陪练与复盘.md",
    "18-话术骨架速查总库.md",
    "19-拒绝与摊派：体面说不与守边界.md",
    "20-请假、婚育与个人事务.md",
    "21-办公IM适配：企业微信、飞书与钉钉.md",
    "22-语体校准：口语与正式话术.md",
)

RED_LINE_PATTERNS = (
    r"代.{0,2}受过.{0,6}隐瞒",
    r"伪造证据.{0,10}(方案|步骤|话术)",
)

# 回归标记：SKILL.md 中不允许在改版时无声丢失的行为边界。
# 每条都对应一项安全或交付承诺（对齐狗头军师的 regression_markers 设计）。
REGRESSION_MARKERS = (
    "佐治而不弄权",
    "目标是**待人接物**",
    "先接住情绪，再分清事实，最后给能执行的选择",
    "给判断但不读心",
    "当前对话没有档案时先发紧凑问卷",
    "只把可见原文、发件人、时间与顺序当事实",
    "不补语气、线下动作或内心",
    "## 每次分析",
    "**情绪落地**",
    "**事实拆分**",
    "**利益判断**",
    "**明确建议**",
    "**行动收束**",
    "第一屏先给一条可复制成品",
    "一条消息尽量只承载一个主动作",
    "默认只读取当前问题直接需要的 1–3 份参考",
    "不因性别、年龄、地域、学历",
    "自伤/自杀风险优先于一切",
    "12356",
    "一律不设计、不代拟并劝阻",
    "像人说话",
)

# 关键模块必须留在 SKILL.md 的路由表里，防止按需加载链路断掉。
REQUIRED_ROUTES = (
    "references/practical/00-导读与使用分级.md",
    "references/practical/08-职场档案与长期记忆.md",
    "references/practical/17-对话演练：预演、陪练与复盘.md",
    "references/practical/18-话术骨架速查总库.md",
    "references/practical/19-拒绝与摊派：体面说不与守边界.md",
    "references/practical/20-请假、婚育与个人事务.md",
    "references/practical/21-办公IM适配：企业微信、飞书与钉钉.md",
    "references/practical/22-语体校准：口语与正式话术.md",
)


def require(path: str) -> Path:
    p = ROOT / path
    if not p.is_file():
        ERRORS.append(f"缺少必需文件: {path}")
    return p


def check_skill_md() -> None:
    skill = require("SKILL.md")
    if not skill.is_file():
        return
    raw = skill.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if not m:
        ERRORS.append("SKILL.md 缺少 frontmatter")
        return
    block = m.group(1)
    name = re.search(r"^name:\s*(\S+)", block, re.M)
    desc = re.search(r"^description:\s*(.+)", block, re.M)
    if not name or not desc:
        ERRORS.append("SKILL.md frontmatter 缺少 name 或 description")
        return
    if name.group(1) != "shaoxingshiye":
        ERRORS.append(f"name 应为 shaoxingshiye，当前 {name.group(1)}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name.group(1)):
        ERRORS.append("name 不符合 kebab-case")
    if ": " in desc.group(1):
        ERRORS.append("description 含半角冒号+空格，可能破坏 YAML")
    body = raw[m.end():]
    if (lines := body.count("\n")) > SKILL_MAX_LINES:
        ERRORS.append(f"SKILL.md 正文 {lines} 行，超过预算 {SKILL_MAX_LINES}")
    if len(raw) > SKILL_MAX_CHARACTERS:
        ERRORS.append(f"SKILL.md 总字符 {len(raw)}，超过预算 {SKILL_MAX_CHARACTERS}")


def check_routing() -> None:
    skill = ROOT / "SKILL.md"
    if not skill.is_file():
        return
    raw = skill.read_text(encoding="utf-8")
    refs = set(re.findall(r"`(references/[^`]+?\.md)`", raw))
    files = {str(p.relative_to(ROOT)) for p in ROOT.glob("references/**/*.md")}
    for r in sorted(refs - files):
        ERRORS.append(f"SKILL.md 路由指向不存在的文件: {r}")
    for f in sorted(files):
        txt = (ROOT / f).read_text(encoding="utf-8")
        for r in re.findall(r"`(references/[^`]+?\.md)`", txt):
            if r not in files:
                ERRORS.append(f"{f} 内断链: {r}")


def check_red_lines() -> None:
    for p in ROOT.glob("references/**/*.md"):
        txt = p.read_text(encoding="utf-8")
        for pat in RED_LINE_PATTERNS:
            if re.search(pat, txt):
                ERRORS.append(f"{p.name} 疑似红线表述: {pat}")


# 上下文预算：普通参考文件单份不超过 8KB（约 4K tokens），
# 按需加载一次读 1–3 份也不超预算；书目索引 09 是唯一例外（仅在用户索要来源时
# 整份读取，不进常规加载路径），上限放宽到 32KB。
REF_MAX_CHARACTERS = 8_000
REF_INDEX_MAX_CHARACTERS = 32_000


def check_context_budget() -> None:
    for p in sorted(ROOT.glob("references/**/*.md")):
        size = len(p.read_text(encoding="utf-8"))
        cap = REF_INDEX_MAX_CHARACTERS if p.name.startswith("09-") else REF_MAX_CHARACTERS
        if size > cap:
            ERRORS.append(f"{p.name} 体积 {size} 字符，超过按需加载预算 {cap}——请拆分文件")


def check_regression_markers() -> None:
    skill = ROOT / "SKILL.md"
    if not skill.is_file():
        return
    content = skill.read_text(encoding="utf-8")
    for marker in REGRESSION_MARKERS:
        if marker not in content:
            ERRORS.append(f"SKILL.md 缺少行为边界回归标记: {marker}")
    for route in REQUIRED_ROUTES:
        if route not in content:
            ERRORS.append(f"SKILL.md 缺少关键路由: {route}")


def check_codex_adapter() -> None:
    agent = require("agents/openai.yaml")
    if not agent.is_file():
        return
    txt = agent.read_text(encoding="utf-8")
    if "$shaoxingshiye" not in txt:
        ERRORS.append("agents/openai.yaml default_prompt 必须包含 $shaoxingshiye")
    for field in ("display_name", "short_description", "default_prompt"):
        if field not in txt:
            ERRORS.append(f"agents/openai.yaml 缺少 interface.{field}")


def approximate_token_count(content: str) -> int:
    """中英混排的保守 token 估算，不依赖第三方库。"""
    cjk = len(re.findall(r"[㐀-䶿一-鿿豈-﫿]", content))
    latin_words = len(re.findall(r"[A-Za-z0-9_]+", content))
    other = len(re.findall(r"[^\sA-Za-z0-9_㐀-䶿一-鿿豈-﫿]", content))
    return cjk + ceil(latin_words * 1.3) + ceil(other / 4)


def check_token_budget() -> None:
    skill = ROOT / "SKILL.md"
    if not skill.is_file():
        return
    tokens = approximate_token_count(skill.read_text(encoding="utf-8"))
    if tokens > SKILL_MAX_APPROX_TOKENS:
        ERRORS.append(
            f"SKILL.md 约 {tokens} tokens，超过预算 {SKILL_MAX_APPROX_TOKENS}——请精简或下沉到参考文件"
        )


def check_markdown_links() -> None:
    link_pattern = re.compile(r"\]\(([^)]+)\)")
    for markdown in ROOT.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or re.match(r"^(?:https?://|mailto:)", target):
                continue
            resolved = (markdown.parent / target).resolve()
            if not resolved.exists():
                ERRORS.append(f"{markdown.relative_to(ROOT)} 坏链: {raw_target}")


# 占位符用拼接构造，避免校验脚本自身命中字面量。
PLACEHOLDER_MARKERS = (
    "[" + "TODO",
    "[" + "FIXME",
    "（待" + "补）",
    "（待" + "定）",
    "（待" + "填）",
)


def check_placeholders() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".yaml", ".yml", ".py", ".sh"}:
            continue
        text = path.read_text(encoding="utf-8")
        for marker in PLACEHOLDER_MARKERS:
            if marker in text:
                ERRORS.append(f"{path.relative_to(ROOT)} 残留占位符: {marker}")


def check_runtime_boundaries() -> None:
    if (ROOT / ".git").exists():
        tracked = subprocess.run(
            ["git", "ls-files", "--", "research", "职场知识库", "恋爱知识库"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        for path in tracked:
            ERRORS.append(f"原始调研内容不得进入仓库: {path}")

    runtime_roots = (ROOT / "SKILL.md", ROOT / "agents", ROOT / "references", ROOT / "scripts", ROOT / "assets")
    forbidden_parts = {"research", "documentation", ".git", "__pycache__", "职场知识库", "恋爱知识库"}
    for runtime_root in runtime_roots:
        if not runtime_root.exists():
            continue
        paths = (runtime_root,) if runtime_root.is_file() else runtime_root.rglob("*")
        for path in paths:
            if forbidden_parts.intersection(path.relative_to(ROOT).parts):
                ERRORS.append(f"运行时目录内出现非运行时内容: {path.relative_to(ROOT)}")
            if path.is_file() and path.suffix in {".pyc", ".pyo"}:
                ERRORS.append(f"运行时目录内出现编译产物: {path.relative_to(ROOT)}")


def main() -> int:
    # --runtime：校验白名单安装副本（SKILL.md/agents/references/scripts/assets），
    # 不要求仓库治理文件（LICENSE/CHANGELOG/CI 等）存在。
    runtime_only = "--runtime" in sys.argv
    if not runtime_only:
        require("LICENSE")
        require("README_EN.md")
        require("CHANGELOG.md")
        require("CONTRIBUTING.md")
        require("SECURITY.md")
        require("CODE_OF_CONDUCT.md")
        require(".gitignore")
        require(".github/workflows/validate.yml")
    for f in REQUIRED_KNOWLEDGE:
        require(f"references/knowledge/{f}")
    for f in REQUIRED_PRACTICAL:
        require(f"references/practical/{f}")
    check_skill_md()
    check_routing()
    check_red_lines()
    check_context_budget()
    check_regression_markers()
    check_codex_adapter()
    check_token_budget()
    check_markdown_links()
    check_placeholders()
    check_runtime_boundaries()
    if ERRORS:
        print("shaoxingshiye 校验失败：")
        for e in ERRORS:
            print(f"  - {e}")
        return 1
    print("shaoxingshiye validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
