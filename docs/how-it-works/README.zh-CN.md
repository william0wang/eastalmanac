# EastAlmanac 计算架构规范：原理与开放文档

_一套完全公开、可逐字复现的核心命理与占星计算引擎规范。_

商业占星与命理应用大多将底层数学模型视作“商业机密”——用封闭的用户界面包裹着算法偏见、随意捏造的评分标准和未经核验的时区转换。

**EastAlmanac 坚持彻底的算法透明度。**

在 [eastalmanac.com](https://eastalmanac.com) 网站上生成的每一个干支字符、动爻变卦、星体度数以及五行强弱打分，均由纯净、完全确定且在浏览器本地安全运行的算法解算完成。没有不可控的云端黑盒、没有机器伪造的假随机数、更没有无法溯源的生搬硬套。遵照以下公开规范，任何人均可推导复现出完全一致的角秒级和分值结果。

---

## 规范目录清单（第一卷）

本期公开文档按易理演化次序，由直观的离散整型代数推进至高阶天体力学球面三角解算：

| 专篇指南 | 核心计算方法论 | 传统渊源与工程对齐基准 |
|---|---|---|
| **[1. 易经三数起卦算法规范](./three-number-casting.zh-CN.md)**<br>([English](./three-number-casting.md)) | 3-bit 模运算、汉明重量奇偶状态机、六爻动静判定、朱熹六爻动变裁决断法。 | 《易经》大衍之数与三铜钱法、朱熹与焦延寿动爻取用规则。 |
| **[2. 四柱八字排盘规范](./four-pillars.zh-CN.md)**<br>([English](./four-pillars.md)) | 出生地挂钟时间权威、节气月柱边界、Sect 2（子初换日）早晚子时取舍、大运起运三天折一年推算。 | 二十四节气真太阳历、《三命通会》、*tyme4ts* 高精度天文历法。 |
| **[3. 五行旺衰打分模型](./strength-scoring.zh-CN.md)**<br>([English](./strength-scoring.md)) | 透干与支藏干基准权重、月令旺相休囚死五级乘数、50% 印比生扶临界点、正统扶抑喜用神推导。 | 《渊海子平》“以月令为纲”正统子平命理学说。 |
| **[4. 结构属性与作用规范](./structural-attrs.zh-CN.md)**<br>([English](./structural-attrs.md)) | 易经当位失位、得中中正、正应敌应、乘承比邻、互卦内核；地支三合局、六合、六冲、三刑（自刑）、六害拓扑网络。 | 易经爻位动力学体系与天干地支刑冲合害相互作用法则。 |
| **[5. 西方回归黄道本命盘规范](./western-chart.zh-CN.md)**<br>([English](./western-chart.md)) | 回归黄道、希腊化古典整宫制（Whole-Sign）、四大主要托勒密相位、分层容许度（日月 8°、行星 6°）。 | *astronomy-engine* 天体力学计算，瑞士星历表（Swiss Ephemeris）0.0″ ASC/MC 严密对齐。 |

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
- **易经三数起卦工具**：[https://eastalmanac.com/zh/tools/cast/](https://eastalmanac.com/zh/tools/cast/)
- **西方占星排盘工具**：[https://eastalmanac.com/zh/astrology-bridge/](https://eastalmanac.com/zh/astrology-bridge/)
