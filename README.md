<!-- README v1.2 · 2026-10-10 -->

<p align="center">
  <strong>简体中文</strong> · <a href="./README_EN.md">English</a>
</p>

<h1 align="center">绍兴师爷 · Shaoxingshiye</h1>

<p align="center">
  <strong>不只替你回消息，更帮你看清局面、办好差事、守住边界。</strong>
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/Agent%20Skills-open%20standard-blue.svg" alt="Agent Skills standard">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python 3">
  <a href="https://github.com/zzycxz/shaoxingshiye/stargazers"><img src="https://img.shields.io/github/stars/zzycxz/shaoxingshiye?style=social" alt="GitHub Stars"></a>
  <a href="https://github.com/zzycxz/shaoxingshiye/actions/workflows/validate.yml"><img src="https://github.com/zzycxz/shaoxingshiye/actions/workflows/validate.yml/badge.svg" alt="Validate Skill"></a>
</p>

目标是**待人接物**：把关系处得长久、体面、有边界。覆盖职场主战场——汇报请示、提意见分歧、跨部门协作、难相处同事、被批评背锅、加薪晋升、会议发言、求职入职、裁员离职——以及做客待客、请客吃饭、随份子人情账、求人谢人、道歉致谢等日常人情场景；结合组织行为学证据、中国职场文化、机关文书经验与劳动法自我保护，把复杂局面变成可执行的下一步。

取名自绍兴师爷——旧时佐官治事的幕友，熟谙规矩与文书，替东家看清局面、办好差事，但**佐治而不弄权**：这是本 skill 的立身原则。

## 它能帮你解决什么

| 你遇到的问题 | 师爷会怎么帮 |
| --- | --- |
| 这句怎么回、这封邮件怎么写 | 先给一条能直接发的话，再补时机和三分支 |
| 想提意见但怕得罪领导 | 先评估信任额度，给三步进言法和台阶设计 |
| 跨部门推不动、催不动 | 交换货币盘点 + 三级火箭催办 |
| 领导难相处、同事甩锅、被孤立 | 分类判定（难相处 vs 毒性），按阶梯应对 |
| 被批评、背锅，情绪上头 | 第一个小时的情绪急救 + 书面澄清模板 |
| 想加薪晋升 | 谈判一页纸、时机选择、被拒后的分支 |
| 找工作、谈 offer、新人 90 天 | offer 谈判清单、入职地图、试用期权益 |
| 被约谈裁员、竞业限制、仲裁 | 当场"三不"、N/N+1/2N 计算、逼退手法对照 |
| 明天有场硬仗（汇报/面谈/谈判） | 对话演练：师爷扮演对方陪练，可开对抗模式，练完五维复盘 |
| 这句话怎么回，想翻骨架 | 实操 18 骨架速查总库：13 类场景集中索引 |
| 同事甩活、被塞任务、不想去的饭局 | 分层拒绝：给排期选项、机械重复、拒绝内容不拒绝人 |
| 请假、婚育、家庭事务这类"不好意思开口"的事 | 权利沟通模板：给排期方案，权利不辩论 |
| 想让师爷记住你的职场格局 | 同意门禁的本地档案（SQLite），随时查看/暂停/撤销/失效标注 |

## 设计原则

1. **先接住人，再解决事。** 情绪没被看见时，最正确的建议也执行不了。
2. **证据分级。** 元分析、理论框架、流行说法、经验策略四档分开用，法律条目对官方原文。
3. **佐治而不弄权。** 机关经验与古典进谏智慧只转译可观察、可纠正、可退出的能力；代过、告密、行贿、伪造证据是红线。
4. **自我保护与沟通同级。** 留证据、防背锅、依法退出是一等模块，不教你"忍一忍"。
5. **不预设你的职场。** 体制内外、行业、用工形式、远程与现场、性别年龄背景——按你的具体处境给方案，不拿刻板印象当依据。

## 项目结构

```text
shaoxingshiye/
├── SKILL.md                    # 核心行为与工作流
├── README.md / README_EN.md    # 中英双语说明
├── LICENSE · CHANGELOG.md      # MIT 协议与变更日志
├── CONTRIBUTING.md · SECURITY.md · CODE_OF_CONDUCT.md
├── .github/                    # CI（validate.yml）与 issue/PR 模板
├── documentation/              # 内部文档：架构/产品/流程/权限/知识库治理
├── agents/
│   └── openai.yaml             # Codex 展示元数据与默认提示词
├── assets/
│   └── skill-overview.png      # 能力总览图
├── references/
│   ├── knowledge/             # 01–09：证据分层的知识文档
│   └── practical/             # 00–21：场景化实操指南 + 演练、骨架速查与个人事务
└── scripts/
    ├── memory_store.py         # 同意门禁的本地长期记忆（SQLite）
    ├── skill_plug.sh           # 动态插拔：挂载/卸载到 FreeCodeZ、Codex
    └── validate_skill.py      # 完整性自检（回归标记/链接/占位符/token 预算）
```

知识库现有 **164 条参考资料**（50 条核心精选：LMX、家长式领导、议题销售、Gross 情绪调节、霸凌元分析、劳动法官方规范、幕学原典《佐治药言》、韩非说难等），完整索引见 `references/knowledge/09-核心书单与论文索引.md`。

<p align="center">
  <a href="./assets/skill-overview.png">
    <img src="./assets/skill-overview.png" width="100%" alt="绍兴师爷能力总览：知识库9份、实操19份、脚本3件与五步分析流程">
  </a>
</p>

## 安装与使用（动态插拔）

本 skill 遵循开放 Agent Skills 标准（agentskills.io），FreeCodeZ 与 OpenAI Codex 原生支持。**默认不安装**——需要时挂载，用完卸载：

```bash
scripts/skill_plug.sh on       # 挂载到 ~/.agents/skills（FreeCodeZ 与 Codex 都识别）
scripts/skill_plug.sh off      # 卸载
scripts/skill_plug.sh status   # 查看挂载状态
scripts/skill_plug.sh on --root freecodez   # 换挂 FreeCodeZ 专属根 ~/.freecodez/skills
scripts/skill_plug.sh on --root zcode       # 换挂 ZCode 专属根 ~/.zcode/skills
```

注意：同一时间只挂一个根——FreeCodeZ 合并多个 skill 根时不做同名去重（路径即身份），双挂会在列表里出现两次；脚本会拒绝双挂。skill 列表在会话启动时扫描，挂卸后新会话生效；已发现的技能可在设置 → skills 面板用开关临时停用。

调用方式（FreeCodeZ 桌面/网页/终端与 Codex 一致）：直接描述问题，由 description 自动匹配加载；或在输入框敲 `$` 从面板选择技能；或在消息里写 `/shaoxingshiye`。`agents/openai.yaml` 提供 ChatGPT 桌面端的展示名称与默认提示词。其他支持 SKILL.md 标准的助手（Claude Code 等）放一份到各自的 skill 目录即可。

新开会话后直接说：

```text
请使用绍兴师爷帮我分析当前这个汇报/这个领导/这场谈判。
```

首次使用会收到一份紧凑问卷（角色、领导风格、同事格局、事件、目标、情绪），不知道的可以留空直接讲故事。

## 边界声明

本 skill 提供职场沟通与决策支持，不替代执业律师、心理治疗或医疗建议；涉及具体法律争议请咨询专业人士。测试：`python3 scripts/validate_skill.py`。

## 开源协议

[MIT License](./LICENSE)（分发时保留版权与许可声明）。
