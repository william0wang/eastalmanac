# EastAlmanac Skill

> **Version 2.2.1** · Updated 2026-10-14 · [Changelog](#changelog)

把专业的命理解读框架"教"给 AI 客户端，让 LLM 与 [EastAlmanac](https://eastalmanac.com) 浏览器交互协同拿到原始数据后，按专业框架输出高质量解读。

## 架构：单 Skill + 渐进式披露

遵循 [Agent Skills 规范](https://agentskills.io/specification)，EastAlmanac 是**一个 skill**，通过渐进式披露按需加载各主题的解读框架：

```
eastalmanac/                        ← 唯一的 skill 目录
├── SKILL.md                        ← 入口：路由表 + 全局原则（触发时加载）
├── scripts/
│   └── bridge.py                   ← 唯一的脚本：本地回环桥接（纯标准库 Python，零依赖）
└── references/                     ← 各主题详细解读框架（按需加载，不占启动上下文）
    ├── bazi-chart.md               ← 八字排盘解读（日主/格局/十神/大运/刑冲合会）
    ├── astrology-chart.md          ← 占星排盘解读（三巨头/行星落宫/相位）
    ├── yijing-cast.md              ← 易经起卦解读（本卦/动爻/变卦/贞悔亨厉 + 梅花体用）
    ├── liuyao-chart.md             ← 六爻纳甲排盘（卦宫/六亲/六神/世应/伏神）
    ├── chengu.md                   ← 称骨算命（袁天罡骨重 + 批注诗）
    ├── tarot.md                    ← 塔罗牌解读（RWS 1909 韦特牌/牌阵/正逆位）
    ├── glossary.md                 ← 术语字典 + 映射表（single source of truth）
    ├── mapping-tables.md           ← 扩展映射表（五行→行业/脏腑/颜色/数字…）
    ├── terms-detail.md             ← 术语深挖（纳音/胎元/五格剖象法/生肖全表…）
    ├── career.md                   ← 事业方向
    ├── wealth.md                   ← 财运分析
    ├── love.md                     ← 感情婚姻
    ├── health.md                   ← 健康养生
    ├── growth.md                   ← 个人成长
    ├── compatibility.md            ← 配对合婚
    ├── period-fortune.md           ← 周期运势（日/周/月/年）
    ├── name-analysis.md            ← 姓名分析
    ├── date-selection.md           ← 择日择吉
    ├── fengshui.md                 ← 风水方位/幸运元素
    └── annual-reading.md           ← 年度流年详批
```

**三层加载**（来自 Agent Skills 规范）：

1. **Metadata**（启动时）：Claude 只读 `SKILL.md` 的 frontmatter（`name` + `description`），判断是否触发本 skill
2. **Body**（触发时）：触发后读 `SKILL.md` 正文 —— 路由表 + 全局原则，按用户问题定位到具体 reference
3. **References**（按需）：只在需要某主题时加载对应 `references/*.md`，避免一次性灌满上下文

**设计原则**：

- **术语 single source of truth**：所有术语定义集中在 `references/glossary.md`（+ 扩展表），其他 reference 只引用不重复
- **数据层与功能层分离**：`bazi-chart.md` / `astrology-chart.md` / `yijing-cast.md` 只做排盘/起卦的结构化解读，功能层 reference 各专注一个生活主题
- **交叉引用**：功能层 reference 通过 context pointer 引用数据层（如 `career.md` 引用 `bazi-chart.md` 和 `glossary.md`）
- **语言自适应**：`SKILL.md` 定义全局原则——检测用户语言，用相同语言回答和追问

## 前置环境要求

- **零安装，开箱即用**：本地回环桥接脚本（`scripts/bridge.py`）纯标准库实现，系统自带的 Python 3 即可运行，**零第三方依赖、无需 Node.js**。
- **免注册免配置 Key**：彻底废弃旧版 Worker MCP 远程后端服务，无需申请 API Key，无每月 100 次额度限制。所有排盘推导（八字、易经、西方占星）均在用户浏览器端静态运行。

## 安全与信任模型

- 桥接脚本（`scripts/bridge.py`，纯标准库可直接审阅）只在 `127.0.0.1` 随机端口一次性监听，收到工具页回传即打印并退出；5 分钟超时自动关闭；无 API Key、无遥测、无文件访问。
- 唯一外部源是 `eastalmanac.com` 工具页；回调地址只指向 `127.0.0.1`，页面拒绝非 localhost 回调。
- **回传 JSON 仅作命理数据使用（data-only）**：skill 指示 agent 忽略其中任何指令式文本，杜绝提示注入。扫描器对运行时外部依赖的提示（如 Snyk W012）是零后端架构固有的信任边界，并非恶意代码检出。

## 安装

### 方式 A —— skills CLI 一键安装（推荐）

```bash
npx skills add william0wang/eastalmanac
```

CLI 会自动检测你已安装的 AI 客户端（Claude Code、Codex、Cursor、ZCode 等 75+ 个）并完成安装：

```bash
npx skills add william0wang/eastalmanac -a zcode -a claude-code   # 指定客户端
npx skills add william0wang/eastalmanac -g                        # 全局（用户级）安装
npx skills update                                               # 之后一键更新
```

### 方式 B —— 手动复制

把 `eastalmanac` 目录复制到你的 AI 客户端对应的 skills 目录：

### ZCode

```bash
cp -r eastalmanac ~/.zcode/skills/
```

### Claude Code / 其他 ~/.agents 客户端

```bash
cp -r eastalmanac ~/.agents/skills/
```

## 验证安装

在客户端里试这几句话：

1. **"帮我排个八字，1990 年 1 月 15 日下午 2 点 30 分出生在上海，男"**
   → 打开 EastAlmanac 八字排盘页，回传后加载 `references/bazi-chart.md`，输出结构化八字盘解读

2. **"我适合做什么工作？"**（需先提供出生信息）
   → 加载 `references/career.md`，输出十神→职业天赋 + 用神→行业方向

3. **"帮我为'今年换工作是否合适'起一卦"**
   → 打开 EastAlmanac 画卦起卦交互页，回传后加载 `references/yijing-cast.md`，输出卦象决策分析

4. **"What does my astrology chart say about me?"** (English)
   → 打开占星桥接页（西式星盘 + 八字同屏计算），回传后加载 `references/astrology-chart.md`，**全程英文回答**

5. **"我属龙他属狗，我们配不配"**
   → 加载 `references/compatibility.md`，输出多系统配对分析

6. **"下个月想搬家，帮我选个吉日"**（需提供出生信息）
   → 加载 `references/date-selection.md`，输出避冲+神煞+用神综合择日

## 开放计算架构（算法与原理文档）

EastAlmanac 将底层核心计算模型、权重表与天文算法完全公开，供开发者与命理研究者查阅与复现：

- **[计算架构规范总览 (Index)](../docs/how-it-works/README.zh-CN.md)** ([English](../docs/how-it-works/README.md))
- **[易经三数起卦算法规范](../docs/how-it-works/three-number-casting.zh-CN.md)** ([English](../docs/how-it-works/three-number-casting.md))：3-bit 模运算、奇偶状态机、六爻动静判定与朱熹动爻断法。
- **[四柱八字排盘规范](../docs/how-it-works/four-pillars.zh-CN.md)** ([English](../docs/how-it-works/four-pillars.md))：出生地挂钟时间权威、节气月柱边界、Sect 2（子初换日）早晚子时取舍与大运顺逆推排。
- **[五行旺衰打分模型](../docs/how-it-works/strength-scoring.zh-CN.md)** ([English](../docs/how-it-works/strength-scoring.md))：透干与支藏干基准权重、月令旺相休囚死五级乘数、50% 生扶临界点与正统扶抑喜用神。
- **[结构属性与作用规范](../docs/how-it-works/structural-attrs.zh-CN.md)** ([English](../docs/how-it-works/structural-attrs.md))：易经爻位当位/得中/中正/正应/乘承比与互卦；地支三合/六合/六冲/三刑/六害拓扑网络。
- **[西方回归黄道本命盘规范](../docs/how-it-works/western-chart.zh-CN.md)** ([English](../docs/how-it-works/western-chart.md))：希腊化古典整宫制（Whole-Sign）、四大主要托勒密相位、分层容许度与瑞士星历表（Swiss Ephemeris）0.0″ 严密对齐。

## 这个 Skill 不做什么

- ❌ **不含合规规则**——解读由用户的 LLM 自由完成，不需要词汇规避
- ❌ **不含字数硬性规定**——与解读质量无关
- ❌ **不替 LLM 做解读决策**——skill 提供框架和术语，LLM 用自己的能力产出解读

## Changelog

遵循 [语义化版本](https://semver.org/lang/zh-CN/)：MAJOR（不兼容变更）/ MINOR（向后兼容新增）/ PATCH（修 bug）。

### 2.2.1 — 2026-10-14

- **梅花易数解读框架**：`references/yijing-cast.md` 新增梅花体用章节——2.1.0 的触发词已承诺梅花易数，现在 `input.method === "meihua"` 的回传 payload 有了完整断法框架（钉死的体/用划分、体用总诀五档判定、用卦→互卦→变卦的阶梯阅读顺序）；SKILL.md 路由表同步增加梅花条目。
- **文档账务同步**：README 徽章与 skills 目录版 changelog 补齐 2.1.0/2.2.0 两个版本的记录。

### 2.2.0 — 2026-10-14

- **塔罗动作**：`tarot` 桥接动作支持四种牌阵（`daily` / `three` / `relationship` / `cross`），打开 RWS 1909 韦特牌页；新增 `references/tarot.md`（78 牌结构、正逆位、可复现 `/r/` 永久链、各牌阵解读框架）；触发词扩充（塔罗/tarot/抽牌/牌阵/正逆位）。

### 2.1.0 — 2026-10-13

- **新增五个桥接动作，skill 覆盖全部工具链**：`liuyao`（六笔铜钱摇卦→纳甲排盘）、`chengu`（袁天罡称骨算命）、`match`（两人八字合参，5 种关系类型）、`dates`（六大事项择日）、`naming`（语料库溯源起名，仅中文）。八个动作全部对线上环境完成回环 E2E 实测（en/zh 双语，79 条 payload 契约断言全过）。
- **新增两篇 references**：`references/liuyao-chart.md`（六笔卦象→排盘→取用神→五步解读顺序）与 `references/chengu.md`（农历年界以正月初一、闰月基重、晚子时进日、金样四两四钱）。
- **SKILL.md 触发词扩充**（六爻/纳甲/梅花易数/称骨/骨重等）；路由表新增六爻、称骨、配对、择日、姓名条目，compatibility / date-selection / name-analysis 三篇同步更新为对应命令用法。

### 2.0.0 — 2026-10-12

- **skill 标识符改名 `yifortune` → `eastalmanac`**：目录、`name` 字段与全部引用路径同步更新；旧版安装需重装并删除旧的 `yifortune` 目录。

### 1.2.0 — 2026-10-12

- **开放计算架构文档（How-It-Works）**（`../docs/how-it-works/`）：五篇可逐字复现的算法规范（三数起卦、四柱排盘、五行旺衰打分、结构属性、西方本命星盘），中英双语，含完整权重表与金样演算。
- **品牌统一为 EastAlmanac**，与 eastalmanac.com 网站品牌一致。
- 仓库地址更新为 `william0wang/eastalmanac`（旧地址自动重定向）。

### 1.1.1 — 2026-10-12

- **回传数据仅作数据（data-only）规则**：`SKILL.md` 明确指示 agent 把桥接回传的 JSON 一律当作命理数据使用，字段中任何指令式文本一律忽略、绝不执行。
- 新增**安全与信任模型**小节：单向回环数据流、`127.0.0.1` 一次性服务、无遥测、唯一外部源 `eastalmanac.com`。

### 1.1.0 — 2026-10-12

- **全面迁移至 EastAlmanac 浏览器回环交互架构**：废弃 Cloudflare Worker MCP 远程后端服务与 API Key 鉴权。
- 免注册、免配置 Key、零月度调用额度限制，计算 100% 运行在浏览器端。
- **核心零安装**：桥接脚本改为纯标准库 Python（`scripts/bridge.py`），系统自带 Python 3 即可运行，无需 Node.js、无 pip 依赖；离线起卦脚本（`cast.sh` / `cast.ps1`）已移除。
- **西方占星也迁移到浏览器端**（`bridge` 动作）：占星桥接页同时计算西式本命盘与同一时刻的八字并打包回传——kerykeion 与 `requirements.txt` 移除，全库零依赖。
- **七种页面/回传语言**：所有桥接动作支持 `--lang=en|zh|zh-tw|es|pt|de|ja`（默认 `en`），按语言前缀打开页面——提示词、卦名/卦义与出处链接按该语言返回，排盘计算字段与语言无关（三条链路 en/zh 双语 E2E 实测通过）。
- 支持 skills CLI 一键安装：`npx skills add william0wang/eastalmanac`。
- 所有解读结尾均附带出处链接（`canonicalUrl`）。

### 1.0.0 — 2026-07-28

- 首个公开发布版本
- 单 skill + 渐进式披露架构（`SKILL.md` 入口 + `references/` 按需加载 + `scripts/` 本地占星计算）
- 覆盖 15 个主题：八字 / 占星 / 易经 / 事业 / 财运 / 感情 / 健康 / 成长 / 配对 / 周期运势 / 姓名 / 择日 / 风水 / 年度详批 / 术语
- **白话结论层**：每个解读双层输出——内层命理要点（术语 OK）+ 外层大白话总结（强制最后输出）
- **语言匹配**：检测用户语言，全程用同一种语言回答
- **推断优先**：性别、公历/农历等能从用户输入读出来的不再追问
