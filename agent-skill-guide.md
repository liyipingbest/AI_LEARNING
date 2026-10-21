# Agent Skill 学习文档

> 目标：读完后能判断什么时候该写 Skill、Skill 目录如何组织、`SKILL.md` 应该包含什么，以及如何创建和验证一个可用的 Skill。

本文以 Codex 的 Agent Skill 规范为主。其他 Agent 产品的字段可能略有差异，但“按需加载、只写非显然信息、把细节放进资源文件”的设计思想是共通的。

## 1. Skill 是什么

Skill 是一个可复用的能力包，用来告诉 Agent：

- 这类任务的目标是什么；
- 什么时候应该使用它；
- 推荐怎样做；
- 有哪些必须遵守的约束；
- 需要时去哪里读取更详细的资料、脚本或模板。

Skill 不是模型微调，也不是 MCP 工具本身。它更像一份“任务说明书 + 资源入口”：

```text
Prompt       = 这一次要做什么
AGENTS.md    = 在这个仓库里工作时必须遵守什么
MCP          = Agent 可以调用哪些外部能力
Skill        = 遇到某类任务时，应该怎样稳定地完成它
```

一个好的 Skill 应该让 Agent 少做重复探索，同时保留它在具体情况下选择合理方案的空间。

## 2. Skill 的三层加载结构

Skill 不是一次性把全部内容塞进上下文，而是分三层逐步展开：

```text
第 1 层：name + description
        ├─ 始终可见，用来判断是否应该加载这个 Skill
        ↓
第 2 层：SKILL.md 正文
        ├─ 命中后加载，放目标、流程、约束和资源入口
        ↓
第 3 层：references / scripts / assets
        └─ 只在当前任务确实需要时读取或执行
```

这种设计叫 **渐进式披露**（progressive disclosure）。

它带来三个直接要求：

1. `description` 必须准确、可区分，不能写成万能描述。
2. `SKILL.md` 只放每次执行都可能需要的信息。
3. 长篇资料、模式分支、确定性代码和模板分别放进 `references/`、`scripts/` 和 `assets/`。

## 3. Skill 的目录结构

一个 Skill 是一个独立文件夹，其中 `SKILL.md` 必须有，其余目录按实际需要创建：

```text
skill-name/
├── SKILL.md                 # 必需：技能入口和核心指令
├── agents/
│   └── openai.yaml          # 可选：UI 展示名、默认提示、调用策略
├── scripts/                 # 可选：确定性脚本或自动化工具
├── references/              # 可选：按需读取的长文档、规范、Schema
└── assets/                  # 可选：生成结果时使用的模板、图片、字体
```

不要为了“看起来完整”而创建空目录。没有明确用途的 `README.md`、变更日志、重复速查表也不要放进去。

## 4. SKILL.md 的结构

`SKILL.md` 通常由两部分组成：

```markdown
---
name: skill-name
description: 这个 Skill 能做什么，以及什么时候应该使用。
---

# Skill 标题

正文：目标、适用范围、流程、约束、资源入口和验证方式。
```

### 4.1 YAML Frontmatter

必填字段：

| 字段 | 要求 | 作用 |
|---|---|---|
| `name` | 小写字母、数字和连字符，建议少于 64 个字符 | 技能标识和显式调用名 |
| `description` | 简洁说明“做什么 + 何时使用” | 自动发现和路由的主要依据 |

可选字段：

| 字段 | 用途 |
|---|---|
| `metadata` | 附加元数据，例如 `short-description` |
| `license` | 许可证信息 |
| `allowed-tools` | 环境支持时声明工具范围 |

`description` 是最重要的路由信息。它应该像这样有明确边界：

```yaml
description: Create or edit Word documents when formatting, tracked changes, or comments require document-specific handling.
```

不要写成：

```yaml
description: Help with documents, writing, analysis, coding, research, and anything else the user needs.
```

后者范围过大，会让 Skill 在无关任务中被误加载。

### 4.2 Markdown 正文

正文没有强制章节顺序，但通常应回答下面这些问题：

1. **目标**：最终要交付什么结果？
2. **适用场景**：什么请求应该使用它？
3. **不适用场景**：哪些相似任务不应使用它？
4. **输入与前提**：开始前需要确认哪些信息？
5. **工作流程**：推荐的步骤、分支和决策标准是什么？
6. **硬约束**：哪些行为绝对不能做，哪些格式必须遵守？
7. **资源入口**：何时读取哪个 reference、运行哪个 script？
8. **输出规范**：最终文件、格式、命名和验收标准。
9. **验证方式**：怎样证明任务确实完成？

简单 Skill 可以只保留其中几节；复杂 Skill 再按需要展开。

## 5. Skill 应该包含什么内容

判断一条信息是否应该写进 Skill，可以问四个问题：

- 它是否会改变 Agent 的决策？
- 它是否是 Agent 不容易自己推断出来的？
- 它是否确实属于当前任务范围？
- 它是否值得长期维护？

四个答案都偏向“是”，才值得写进去。

### 必写内容

- **能力边界**：Skill 解决什么问题，不解决什么问题。
- **目标结果**：完成时应该得到什么交付物。
- **关键决策规则**：遇到常见分支时如何选择。
- **真实约束**：格式、权限、安全、兼容性或业务规则。
- **资源路由**：哪个文件负责哪类细节，什么时候读取。
- **验收方法**：如何检查结果，而不是只看“看起来像完成了”。

### 推荐内容

- 一小段最小可用示例；
- 输出文件的结构或 Schema；
- 容易出错的边界条件；
- 对非显然术语的解释；
- 失败重试或停止条件；
- 需要长期维护的本地约定。

### 不应该写进 SKILL.md 的内容

- “要仔细”“要专业”“要保证质量”这类空泛建议；
- Agent 已经知道的一般性知识；
- 可以放在 `references/` 的长篇手册；
- 可以写成 `scripts/` 的重复确定性逻辑；
- 与任务无关的个人偏好；
- 还没有验证过的推测性边界条件；
- 其他 Skill 已经维护的重复内容。

## 6. 四类资源的职责

| 位置 | 放什么 | 什么时候使用 |
|---|---|---|
| `SKILL.md` | 每次都需要知道的目标、流程、约束和路由 | Skill 被选中时加载 |
| `references/` | API 文档、Schema、政策、详细模式说明、长示例 | 当前任务需要该细节时读取 |
| `scripts/` | 重复执行、容易出错、需要确定性的代码 | 需要执行或修改时运行 |
| `assets/` | 模板、图片、字体、项目脚手架 | 生成结果时复制或引用 |

### 什么时候拆到 references

出现下面情况时，考虑拆分：

- 只有某一种模式才需要；
- 内容很长，但大部分任务不会用到；
- 内容需要独立维护或频繁更新；
- 同一主题有多个并列分支，例如不同云平台、不同文档类型。

例如：

```text
cloud-deploy/
├── SKILL.md
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

`SKILL.md` 负责选择平台；选定 AWS 后只读取 `references/aws.md`，不要同时加载三份云平台文档。

### 什么时候拆到 scripts

满足任一条件就值得写脚本：

- 同一段逻辑会被反复重写；
- 结果必须可重复；
- 手工执行容易漏步骤；
- 需要处理结构化数据、外部 API 或复杂文件格式。

脚本写完后要实际运行验证，不要只在文档里声明“可用”。

## 7. 最小可用模板

```markdown
---
name: weekly-status
description: Create a concise weekly status report from project notes, git history, and issue updates; use when the user asks for a weekly or sprint summary.
metadata:
  short-description: Draft weekly status reports
---

# Weekly Status

## Goal

Produce a short status report that separates completed work, current risks, and next actions.

## Workflow

1. Collect the reporting period and intended audience.
2. Read repository history and project notes for evidence.
3. Group changes by outcome, not by file name.
4. Keep claims traceable to concrete commits, issues, or notes.
5. Call out blockers, owners, and next steps when the source material supports them.

## Constraints

- Do not invent progress or completion dates.
- Separate confirmed facts from inferred follow-ups.
- Keep the default report under 300 Chinese characters or 150 English words unless the user asks for detail.

## Output

Use these sections: Completed, In Progress, Risks / Blockers, Next.

## Validation

Check that every reported item has a source, and that no next action appears without an owner or a clear unresolved state.
```

这个模板短，但已经具备 Skill 最关键的几个部分：路由、目标、流程、约束、输出和验证。

## 8. 完整示例：论文学习 Skill

目录可以这样组织：

```text
paper-learning/
├── SKILL.md
├── references/
│   └── note-template.md
└── assets/
    └── equation-checklist.md
```

`SKILL.md` 示例：

```markdown
---
name: paper-learning
description: Turn an AI paper into a structured Chinese learning note covering problem, prior work, method, equations, experiments, limitations, and connections to related papers; use when the user asks to study, explain, compare, or teach a paper.
metadata:
  short-description: Structured AI paper notes
---

# Paper Learning

## Goal

Produce a learning note that helps a reader understand why the paper exists, how the method works, what evidence supports it, and where it fits in the research timeline.

## Workflow

1. Identify the title, authors, year, venue, and arXiv version.
2. State the problem in plain language before introducing notation.
3. Explain the previous approach and identify the concrete limitation it leaves.
4. Walk through the method in causal order, defining every symbol and tensor shape on first use.
5. Explain experiments, baselines, metrics, and the strongest counterargument.
6. Separate the paper's claims from later interpretation or follow-up work.
7. End with limitations, open questions, and connections to adjacent papers.

## Constraints

- Never invent experimental results, numbers, or citations.
- Preserve exact model names, paper titles, author names, and years.
- Mark any inference that is not directly supported by the source.
- Explain equations in words before or after displaying them.

## Resources

- Read `references/note-template.md` when producing a long-form note.
- Use `assets/equation-checklist.md` before publishing an equation-heavy section.

## Output

Use: One-sentence thesis, Problem, Prior work, Core idea, Method, Experiments, Limitations, Connections, Self-check.

## Validation

Check that the note explains every symbol, distinguishes claims from evidence, and contains no unsupported numeric result.
```

注意：这个示例没有把完整模板复制进 `SKILL.md`，而是把长模板放进 `references/`，只在需要长文时读取。

## 9. agents/openai.yaml

`agents/openai.yaml` 是可选的界面与调用策略配置，不是 Skill 正文。常见字段包括：

```yaml
interface:
  display_name: "Paper Learning"
  short_description: "Structured AI paper notes"
  default_prompt: "Use $paper-learning to create a structured learning note for this paper."

policy:
  allow_implicit_invocation: true
```

说明：

- `allow_implicit_invocation` 默认为 `true`，允许根据任务自动发现；
- 设为 `false` 后，Skill 默认不进入模型上下文，但仍可通过 `$skill-name` 显式调用；
- `default_prompt` 应明确提到 `$skill-name`；
- 不要为了“更安全”就盲目关闭自动发现，除非用户明确要求显式调用。

## 10. 创建一个 Skill 的步骤

### 第 1 步：确认它值得成为 Skill

适合做成 Skill 的任务通常具备：

- 会反复出现；
- 有稳定流程或项目约定；
- 需要特定资料、模板或脚本；
- 不写下来时，Agent 容易漏步骤或做错选择。

一次性写作请求、普通问答和简单代码修改通常不需要 Skill。

### 第 2 步：命名

使用小写字母、数字和连字符：

```text
paper-learning
release-notes
pdf-review
api-migration
```

文件名和目录名保持一致，避免 `Paper_Learning`、`paperLearning` 等混用。

### 第 3 步：初始化目录

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/init_skill.py \
  paper-learning \
  --path "${CODEX_HOME:-$HOME/.codex}/skills"
```

如果确定需要资源目录，再按需添加：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/init_skill.py \
  paper-learning \
  --path "${CODEX_HOME:-$HOME/.codex}/skills" \
  --resources references,scripts
```

不要一开始就创建所有可选目录。

### 第 4 步：先写最小版本

先写清楚：

- 何时使用；
- 最终交付什么；
- 最关键的三到五个步骤；
- 绝对不能违反的约束；
- 怎样验证完成。

不要急着加入所有示例和边缘情况。

### 第 5 步：用真实任务测试

给 Agent 一个真实请求，观察它是否会：

- 在正确场景触发；
- 在错误场景保持沉默；
- 读取正确的 reference；
- 执行正确的 script；
- 产出符合验收标准的结果。

如果 Agent 没有做对，优先修正信息缺失或边界不清的地方，而不是不断增加泛化规则。

### 第 6 步：验证格式

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  "${CODEX_HOME:-$HOME/.codex}/skills/paper-learning"
```

验证器主要检查：

- `SKILL.md` 是否存在；
- YAML frontmatter 是否合法；
- `name` 和 `description` 是否存在；
- 名称是否符合连字符规范；
- 是否遗留未完成的 TODO。

格式验证通过不等于 Skill 一定好用，还需要检查路由描述、指令边界和资源引用是否合理。

## 11. Skill 自检清单

- [ ] `name` 简短、唯一、符合连字符规范。
- [ ] `description` 说明了“做什么”和“何时使用”。
- [ ] `description` 没有宽泛到会吸走无关任务。
- [ ] `SKILL.md` 包含目标、流程、约束和验证。
- [ ] 只保留会改变 Agent 决策的信息。
- [ ] 长内容已拆到 `references/`。
- [ ] 可重复逻辑已拆到 `scripts/`。
- [ ] 模板、字体、图片等已放入 `assets/`。
- [ ] 每个资源都从 `SKILL.md` 明确链接，并说明何时读取。
- [ ] 没有重复的 README、变更日志或空目录。
- [ ] 已用真实请求测试过。
- [ ] 已通过 `quick_validate.py`。

## 12. 常见误区

### 误区 1：把所有知识都塞进 SKILL.md

结果是入口文件过长，真正重要的约束反而不突出。应把长文档放进 `references/`。

### 误区 2：description 写得太宽

“处理文档、代码、数据和研究”不是描述，是目录。路由描述应尽量具体，并在必要时说明不适用边界。

### 误区 3：把一次性偏好写成永久规则

Skill 应该沉淀真实、重复出现的工作方式，而不是把某次对话中的临时要求升级为通用制度。

### 误区 4：只有说明，没有验收

没有验证标准的 Skill 很容易产出“看起来完成”的结果。至少写清楚一个可观察的完成条件。

### 误区 5：为了完整而创建空资源目录

可选目录只有在确实有对应内容时才创建。空目录会增加维护成本，也会误导 Agent。

## 13. Skill、AGENTS.md、Prompt 与 MCP 的区别

| 形态 | 解决的问题 | 加载方式 |
|---|---|---|
| Prompt | 这一次要做什么 | 当前请求 |
| AGENTS.md | 这个目录树中的工作规则 | 进入对应目录时生效 |
| Skill | 某类任务如何稳定完成 | 根据名称和描述按需加载 |
| MCP | 可以调用哪些外部工具和数据源 | 由运行时配置和调用 |

它们可以组合使用：AGENTS.md 规定仓库约束，Skill 规定任务流程，MCP 提供外部工具，Prompt 描述本次目标。

## 14. 学习练习

### 练习 1：写一个最小 Skill

选择一个你每周都会做的任务，只写 `SKILL.md`，控制在 40 行以内。要求包含：目标、适用场景、三步流程、一个约束、一个验证条件。

### 练习 2：拆分长内容

给上面的 Skill 增加一个 `references/` 文件，把重复出现的长模板或规则移出去，并确认 `SKILL.md` 中仍能清楚找到它。

### 练习 3：增加确定性脚本

把一个容易手工出错的步骤写成 `scripts/` 中的脚本，实际运行一次，并记录输入、输出和失败条件。

### 练习 4：做一次反向测试

拿一个与 Skill 相似但不属于它范围的任务，检查 description 是否会让 Agent 误触发。如果会，收紧边界。

## 15. 一句话总结

**Skill 的价值不在于写得多，而在于把“什么时候用、做到什么程度、哪些信息不能猜、需要时去哪里找”写得足够准确。**
