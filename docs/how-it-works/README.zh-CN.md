# EastAlmanac 计算架构规范：原理与开放文档

_一套完全公开、可逐字复现的核心命理与占星计算引擎规范。_

商业占星与命理应用大多将底层数学模型视作“商业机密”——用封闭的用户界面包裹着算法偏见、随意捏造的评分标准和未经核验的时区转换。

**EastAlmanac 坚持彻底的算法透明度。**

在 [eastalmanac.com](https://eastalmanac.com) 网站上生成的每一个干支字符、动爻变卦、星体度数以及五行强弱打分，均由纯净、完全确定且在浏览器本地安全运行的算法解算完成。没有不可控的云端黑盒、没有机器伪造的假随机数、更没有无法溯源的生搬硬套。遵照以下公开规范，任何人均可推导复现出完全一致的角秒级和分值结果。

---

## 规范目录清单（第一卷 · 基础引擎）

本期公开文档按易理演化次序，由直观的离散整型代数推进至高阶天体力学球面三角解算：

| 专篇指南 | 核心计算方法论 | 传统渊源与工程对齐基准 |
|---|---|---|
| **[1. 易经三数起卦算法规范](./three-number-casting.zh-CN.md)**<br>([English](./three-number-casting.md)) | 笔画折叠 + 时刻混合、3-bit 模运算、汉明重量奇偶状态机、六爻动静判定、朱熹六爻动变裁决断法。 | 《易经》大衍之数与三铜钱法、朱熹与焦延寿动爻取用规则。 |
| **[2. 四柱八字排盘规范](./four-pillars.zh-CN.md)**<br>([English](./four-pillars.md)) | 出生地挂钟时间权威、节气月柱边界、Sect 2（子初换日）早晚子时取舍、大运起运三天折一年推算。 | 二十四节气真太阳历、《三命通会》、*tyme4ts* 高精度天文历法。 |
| **[3. 五行旺衰打分模型](./strength-scoring.zh-CN.md)**<br>([English](./strength-scoring.md)) | 透干与支藏干基准权重、月令旺相休囚死五级乘数、50% 印比生扶临界点、正统扶抑喜用神推导。 | 《渊海子平》“以月令为纲”正统子平命理学说。 |
| **[4. 结构属性与作用规范](./structural-attrs.zh-CN.md)**<br>([English](./structural-attrs.md)) | 易经当位失位、得中中正、正应敌应、乘承比邻、互卦内核；地支三合局、六合、六冲、三刑（自刑）、六害拓扑网络。 | 易经爻位动力学体系与天干地支刑冲合害相互作用法则。 |
| **[5. 西方回归黄道本命盘规范](./western-chart.zh-CN.md)**<br>([English](./western-chart.md)) | 回归黄道、希腊化古典整宫制（Whole-Sign）、四大主要托勒密相位、分层容许度（日月 8°、行星 6°）。 | *astronomy-engine* 天体力学计算，瑞士星历表（Swiss Ephemeris）0.0″ ASC/MC 严密对齐。 |

## 第二卷 · 占法扩展与生活决策

| 专篇指南 | 核心计算方法论 | 传统渊源与工程对齐基准 |
|---|---|---|
| **[6. 六爻纳甲排盘引擎](./liuyao-najia.zh-CN.md)**<br>([English](./liuyao-najia.md)) | 六笔笔画 mod-8 四象映射、京房八宫生成序、纳甲干支全表、六亲六神、世应、伏神、变卦。 | 京房八宫纳甲、袁天罡六神起法；64 卦全覆盖不变量机器校验。 |
| **[7. 梅花易数体用分析](./meihua-body-use.zh-CN.md)**<br>([English](./meihua-body-use.md)) | 与铜钱卦共享同一卦象；钉死的体用划分、体用总诀五档判定、互卦变卦阶梯阅读。 | 《梅花易数》体用总诀；多爻齐动的确定性扩展。 |
| **[8. 塔罗抽牌引擎](./tarot-draw.zh-CN.md)**<br>([English](./tarot-draw.md)) | 种子 = 揭牌时刻 + 挑牌顺序；种子化 Fisher-Yates 摊牌、独立正逆位流、重跑引擎的 `/r/` 永久链。 | 韦特牌（RWS 1909，公有领域）；两万种子统计健康度校验。 |
| **[9. 称骨算命引擎](./chengu-bone-weight.zh-CN.md)**<br>([English](./chengu-bone-weight.md)) | 四张骨重表（60+12+30+12）、21–71 钱全量判词、三条钉死约定（农历年界、闰月归基、晚子时进日）。 | 袁天罡称骨歌；与归档底本逐字节钉死。 |
| **[10. 八字合参引擎](./synastry.zh-CN.md)**<br>([English](./synastry.md)) | 六维公开权重（30/25/15/15/10/5）、四档评级、角色对称预设、「无总分」回传契约。 | 建立于 l3attrs 支关系与十神之上的公开规则层。 |
| **[11. 择日引擎](./date-selection.zh-CN.md)**<br>([English](./date-selection.md)) | 黄历反查：宜忌词条 + 建除十二神 + 黄黑道十二星的加法权重、本命六冲标记。 | tyme4ts 规则表；2026 全年扫描校准。 |
| **[12. 溯源起名引擎](./naming-stroke.zh-CN.md)**<br>([English](./naming-stroke.md)) | 检索而非生成：八字喜用匹配为唯一排序键、五格/三才作披露参考层、谐音只标记不剔除。 | 经典语料库逐行出典；熊崎氏五格数理表（公有领域）。 |

---

## 核心系统保障

1. **零伪随机**：易经占筮引擎绝不使用 `Math.random()` 随机构造卦象，起卦机锋全部出自求问者的真实心念。
2. **挂钟时间权威**：东方节气与星盘坐标均对应出生瞬间地表物理天象，拒绝粗暴的 UTC 绝对时区平移。
3. **纯浏览器端执行**：所有计算逻辑完全在客户端无依赖运行，用户个人生辰隐私永不上报服务器。
4. **金样案例可验证**：每篇文档均附带测试套件锁定的真实基准算例，支持公众对照核查。

---

## 在线实测工具

您可在已上线的生产环境中亲自验证上述任意算法与命盘解算：
- **八字在线排盘工具**：[https://eastalmanac.com/zh/tools/chart/](https://eastalmanac.com/zh/tools/chart/)
- **易经起卦工具（铜钱卦 / 梅花）**：[https://eastalmanac.com/zh/tools/cast/](https://eastalmanac.com/zh/tools/cast/)
- **六爻纳甲排盘工具**：[https://eastalmanac.com/zh/tools/liuyao/](https://eastalmanac.com/zh/tools/liuyao/)
- **塔罗工具**：[https://eastalmanac.com/zh/tools/tarot/](https://eastalmanac.com/zh/tools/tarot/)
- **称骨工具**：[https://eastalmanac.com/zh/tools/chengu/](https://eastalmanac.com/zh/tools/chengu/)
- **合盘工具**：[https://eastalmanac.com/zh/tools/match/](https://eastalmanac.com/zh/tools/match/)
- **择日工具**：[https://eastalmanac.com/zh/tools/dates/](https://eastalmanac.com/zh/tools/dates/)
- **溯源起名工具**：[https://eastalmanac.com/zh/tools/naming/](https://eastalmanac.com/zh/tools/naming/)
- **西方占星排盘工具**：[https://eastalmanac.com/zh/astrology-bridge/](https://eastalmanac.com/zh/astrology-bridge/)
