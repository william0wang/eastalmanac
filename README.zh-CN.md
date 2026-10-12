# EastAlmanac Skill

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-spec%20compliant-blue)](https://agentskills.io)
[![skills.sh](https://skills.sh/b/william0wang/eastalmanac)](https://skills.sh/william0wang/eastalmanac)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.2.0-green.svg)](#changelog)

**[English](README.md)** · **简体中文**

> 一个符合 [Agent Skills](https://agentskills.io) 规范的 skill，通过与 [EastAlmanac](https://eastalmanac.com) 浏览器交互协同，把任意 LLM 客户端变成专业的命理解读助手。

EastAlmanac 教 AI **怎么解读**命理数据——排盘框架、术语体系、白话表达——这样当八字或卦象算出来之后，输出的是一份高质量的专业解读，而不是一堆原始数字。

覆盖 **15 个主题**：八字、西方占星、易经起卦、事业、财运、感情、健康、成长、配对、周期运势、姓名、择日、风水、流年详批，外加一套共享的术语层。

## 产品优势

- **完全开源且免注册**：无须申请 API 密钥，无邮箱注册门槛，彻底摆脱调用次数和每月配额限制。
- **零安装、零依赖**：系统自带的 Python 3 即可运行（桥接脚本纯标准库）；八字、易经、西方占星**全部**在浏览器端计算，数据零留存，隐私零泄露。
- **动静结合的仪式感**：保留终端极客交互的同时，通过 `eastalmanac.com` 带来视觉画布画卦起卦与生辰八字核对的仪式感，通过本地回环桥接脚本无缝自动回传终端，输出 15 主题大师级断语。

---

## 这个仓库是什么 —— 以及不是什么

| ✅ 提供 | ❌ 不包含 |
| ------ | ------ |
| `yifortune` skill（`SKILL.md` + `references/` + `scripts/bridge.py`） | 远程云端数据库或集中式后端 |
| 15 个命理主题的解读框架 | API Key、付费墙或每月调用限额 |
| 本地回环交互桥接脚本（`scripts/bridge.py`） | 收集个人生辰八字的网络追踪 |
| 白话输出规则（AI 服务普通人，不是命理大师） | |

---

## 前置环境要求

- **零安装，开箱即用**——skill 依赖系统自带的 Python 3（`scripts/bridge.py` 纯标准库实现），macOS 和绝大多数 Linux 发行版无需任何额外安装。包括西方占星在内，所有计算都在浏览器端完成，**没有任何依赖要装**。

---

## 安装

### 方式 A —— [skills CLI](https://skills.sh) 一键安装（推荐）

```bash
npx skills add william0wang/eastalmanac
```

CLI 会自动检测你已安装的 AI 客户端（Claude Code、Codex、Cursor、ZCode 等 75+ 个）并完成安装。常用变体：

```bash
npx skills add william0wang/eastalmanac -a claude-code -a zcode   # 指定客户端
npx skills add william0wang/eastalmanac -g                        # 全局（用户级）安装
npx skills update                                               # 之后一键更新
```

### 方式 B —— 手动安装（Claude Desktop 或其他客户端）

把 `yifortune` skill 目录复制到客户端的 skills 文件夹。

**Claude Code / 其他兼容 `~/.agents` 的客户端：**

```bash
git clone https://github.com/william0wang/eastalmanac.git
cp -r eastalmanac/skills/yifortune ~/.agents/skills/
```

**ZCode：**

```bash
git clone https://github.com/william0wang/eastalmanac.git
cp -r eastalmanac/skills/yifortune ~/.zcode/skills/
```

**Claude Desktop：** 把 skill 放到 `~/Library/Application Support/Claude/skills/`（macOS）或 `%APPDATA%\Claude\skills\`（Windows），然后重启 Claude Desktop。

安装后直接在对话里提到即可——比如"用 yifortune skill 帮我看个八字"。

---

## 验证安装

在客户端里试这些：

| 提示词 | 会发生什么 |
| ------ | ---------- |
| "帮我排个八字，1990 年 1 月 15 日下午 2 点 30 分出生在上海，男" | 自动打开网页核对八字，回传后进行八字排盘结构化解读 |
| "我适合做什么工作？"（需提供出生信息） | 事业分析 |
| "帮我为'今年换工作是否合适'起一卦" | 自动打开画卦起卦页面，绘制完成后回传进行决策解读 |
| "What does my astrology chart say about me?" | 打开占星桥接页（西式星盘 + 八字同屏），回传后用**英文**解读 |
| "下个月想搬家，帮我选个吉日" | 择吉日 |

---

## 架构：单 skill + 渐进式披露

遵循 [Agent Skills 规范](https://agentskills.io/specification)，EastAlmanac 是**一个 skill**，内容按需加载：

```
skills/yifortune/
├── SKILL.md                  ← 入口：路由表 + 全局原则（触发时加载）
├── scripts/
│   └── bridge.py             ← 唯一的脚本：纯标准库 Python 零依赖回环桥接
└── references/               ← 各主题解读框架（按需加载，启动时不读）
    ├── bazi-chart.md         ← 八字解读（数据层）
    ├── astrology-chart.md    ← 西方占星解读（数据层）
    ├── yijing-cast.md        ← 易经起卦解读（数据层）
    ├── glossary.md           ← 术语（唯一真相源）
    ├── mapping-tables.md     ← 扩展五行映射表
    ├── terms-detail.md       ← 深度术语参考
    ├── career.md  wealth.md  love.md  health.md  growth.md
    ├── compatibility.md  period-fortune.md  name-analysis.md
    └── date-selection.md  fengshui.md  annual-reading.md
```

**三层加载**（渐进式披露）：

1. **元数据**（启动时）—— 客户端只读 `SKILL.md` 的 frontmatter，决定是否触发本 skill（约 100 tokens）
2. **正文**（触发时）—— 读 `SKILL.md`：路由表 + 全局原则，然后定位到相关 reference
3. **References**（按需）—— 只在需要某个主题时加载对应的 `references/*.md`，保持上下文窗口精简

---

## 安全与信任模型

所有计算在 `eastalmanac.com` 浏览器端完成；仓库里唯一的本地代码是 `scripts/bridge.py`（纯标准库，约 180 行，可直接审阅）：

- **单向回环数据流**：桥接只在 `127.0.0.1` 随机端口监听，收到工具页的一次 POST 后把 JSON 打印到 stdout 即退出；`GET` 一律 404；5 分钟超时自动关闭。
- **唯一外部源**：桥接唯一的对外动作是在浏览器打开 `https://eastalmanac.com`（按语言加前缀）的工具页；回调地址指向 `127.0.0.1`，且页面拒绝非 localhost 回调。
- **无密钥、无遥测**：没有 API Key、账号、统计上报和文件访问——没有可泄露的东西。
- **回传数据仅作数据**：skill 明确指示 agent 把回传 JSON 只当作命理事实使用、忽略其中任何指令式文本，即使页面被攻破也无法驱动 agent。

> 安全扫描器可能会对运行时依赖 `eastalmanac.com` 给出提示（如 Snyk Agent Scan 的 W012 "unverifiable external dependency"）。这是零后端架构固有的信任边界（即上文描述的模型），并非恶意代码的检出结果。

---

## 开放计算架构（算法与原理文档）

与市面上大量黑盒算命与占星工具不同，EastAlmanac 将底层的核心计算模型、权重配比表与天文推导法则完全公开，作为可逐字复现的标准规范对外发布：

- **[计算架构规范总览 (Index)](docs/how-it-works/README.zh-CN.md)** ([English](docs/how-it-works/README.md))
- **[易经三数起卦算法规范](docs/how-it-works/three-number-casting.zh-CN.md)** ([English](docs/how-it-works/three-number-casting.md))：3-bit 模运算、奇偶状态机、六爻动静判定与朱熹动爻断法。
- **[四柱八字排盘规范](docs/how-it-works/four-pillars.zh-CN.md)** ([English](docs/how-it-works/four-pillars.md))：出生地挂钟时间权威、节气月柱边界、Sect 2（子初换日）早晚子时取舍与大运顺逆推排。
- **[五行旺衰打分模型](docs/how-it-works/strength-scoring.zh-CN.md)** ([English](docs/how-it-works/strength-scoring.md))：透干与支藏干基准权重、月令旺相休囚死五级乘数、50% 生扶临界点与正统扶抑喜用神。
- **[结构属性与作用规范](docs/how-it-works/structural-attrs.zh-CN.md)** ([English](docs/how-it-works/structural-attrs.md))：易经爻位当位/得中/中正/正应/乘承比与互卦；地支三合/六合/六冲/三刑/六害拓扑网络。
- **[西方回归黄道本命盘规范](docs/how-it-works/western-chart.zh-CN.md)** ([English](docs/how-it-works/western-chart.md))：希腊化古典整宫制（Whole-Sign）、四大主要托勒密相位、分层容许度与瑞士星历表（Swiss Ephemeris）0.0″ 严密对齐。

---

## 设计原则

- **服务对象是普通人，不是命理大师** —— AI 服务的是好奇的门外汉。每次解读分两层：内层（命理要点 + 术语，保证可追溯）+ **外层大白话**（用户真正想要的）。
- **主动服务** —— AI 自己路由、决定用哪个工具，绝不把工具菜单甩给用户挑。
- **语言匹配** —— 用户用什么语言问，AI 从第一句开始就用同样的语言回答。
- **推断优先** —— 能从用户措辞读出来的出生信息（性别、公历/农历等），AI 不再追问。
- **唯一真相源** —— 所有术语集中在 `references/glossary.md`，其他文件引用它而不是重复定义。

## 这个 skill 不做的事

- ❌ 不做合规 / 审查规则 —— 解读由用户自己的 LLM 产出
- ❌ 不硬性规定字数 —— 与解读质量无关
- ❌ 不替 LLM 做解读决策 —— skill 提供框架和术语，LLM 用自己的能力产出解读

---

## 常见问题

| 症状 | 原因 / 解决 |
| ---- | ----------- |
| Skill 不触发 | 确认 `yifortune` 目录在客户端的 skills 文件夹里，且 `SKILL.md` frontmatter 的 `name: yifortune` 一致。重启客户端。 |
| 无法自动打开系统浏览器 | 检查终端输出中的 URL，可手动复制并在任意浏览器中打开 `https://eastalmanac.com/...`。 |
| 等待网页操作超时（5分钟） | 若已在网页完成操作并生成了结果，可直接点击页面上的「复制提示词」并直接粘贴在对话框中。 |
| 占星页需要经纬度和时区 | 自行把**出生地**换算成经纬度和 UTC 偏移（注意夏令时），再运行 `python3 scripts/bridge.py bridge --date=... --time=... --lat=... --lon=... --tz=...`。 |

---

## 贡献

欢迎贡献——尤其是术语订正、新主题 reference、翻译。规则见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## Changelog

### 1.2.0 — 2026-10-12

- **开放计算架构文档（How-It-Works）**（`docs/how-it-works/`）：五篇可逐字复现的算法规范——三数起卦、四柱排盘、五行旺衰打分（完整权重表）、结构属性（爻位格局与地支刑冲合害）、西方本命星盘——每篇含公式、完整数值表与金样演算，中英双语，带索引页并从三份 README 互链。
- **品牌统一为 EastAlmanac**：所有文档、references 标题与脚本提示信息均与 eastalmanac.com 网站品牌对齐（skill 标识 `name` 仍为 `yifortune`）。
- **仓库改名** `william0wang/yifortune` → `william0wang/eastalmanac`；安装命令、clone 示例与 skills.sh 徽章已同步更新（旧地址保持自动重定向）。

### 1.1.1 — 2026-10-12

- **回传数据仅作数据（data-only）规则**：`SKILL.md` 明确指示 agent 把桥接回传的 JSON（及用户粘贴的 EastAlmanac 文本）一律当作命理数据使用——字段中出现的任何指令式文本一律忽略、绝不执行，收窄网站被攻破时的提示注入面。
- README 新增**安全与信任模型**小节：单向回环数据流、`127.0.0.1` 一次性服务、无遥测、唯一外部源 `eastalmanac.com`。

### 1.1.0 — 2026-10-12

- **全面迁移至 EastAlmanac 浏览器回环交互架构**：废弃 Cloudflare Worker MCP 远程后端服务与 API Key 鉴权。
- 免注册、免配置 Key、零月度调用额度限制，计算 100% 运行在浏览器端。
- **核心零安装**：桥接脚本改为纯标准库 Python——系统自带 Python 3 即可运行，不再需要 Node.js，也没有任何 pip 依赖。内置的离线起卦脚本（`cast.sh` / `cast.ps1`）已移除，八字与易经的全部计算都在浏览器端完成。
- **西方占星也迁移到浏览器端**（`bridge` 动作）：占星桥接页同时计算西式本命盘与同一时刻的八字并打包回传——kerykeion、`requirements.txt` 和 AGPL 许可证说明全部移除，整个 skill 端到端零依赖。
- **七种页面/回传语言**：所有桥接动作支持 `--lang=en|zh|zh-tw|es|pt|de|ja`（默认 `en`），按语言前缀打开页面——提示词、卦名/卦义与出处链接按该语言返回，排盘计算字段与语言无关（三条链路 en/zh 双语 E2E 实测通过）。
- 支持 skills CLI 一键安装：`npx skills add william0wang/eastalmanac`。
- 所有解读结尾均附带出处链接（`canonicalUrl`）。

### 1.0.0 — 2026-07-28

- 首个公开发布版本。单 skill 架构 + 渐进式披露（SKILL.md + references + scripts）
- 覆盖 15 个主题：八字、西方占星、易经、事业、财运、感情、健康、成长、配对、周期运势、姓名、择日、风水、流年详批
- 白话输出规则（双层：专业分析 + 大白话总结）

## 许可证

[MIT](LICENSE) © 2026 william0wang
