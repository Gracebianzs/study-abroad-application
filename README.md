# 留学申请全流程助手 (Study Abroad Application Skill)

> 面向海外硕士申请的标准化工作流技能，覆盖院校搜索、匹配度打分、简历优化、跟踪台账生成全流程。

## 功能特性

### 5阶段标准化工作流

| 阶段 | 功能 | 产出 |
|------|------|------|
| 1. 背景与需求解析 | 提取申请人背景（院校/GPA/语言/经历）和申请需求（专业/地区/预算/排名） | 申请人画像 + 需求清单 |
| 2. 院校搜索与信息采集 | 分地区并行搜索，采集学费/语言要求/截止日期/课程/录取率等10+维度 | 院校信息数据库 |
| 3. 匹配度打分与排序 | 6维度10分制加权评分，分冲刺/主申/保底三档定位 | 匹配度评分表 + 投递优先级 |
| 4. 简历针对性优化 | 标准结构重构、STAR法则量化经历、专业关键词植入、各校微调 | 优化简历 + 修改方案 |
| 5. 可视化跟踪台账 | 交互式HTML台账（总览对比/院校跟踪/截止时间线/材料清单） | 可交互跟踪台账 |

### 内置资源

- **院校速查表**：香港5所 + 英国12所TESOL项目核心数据（学费/雅思/截止/特点）
- **打分框架**：6维度详细评分标准，每维度5档评分细则
- **简历关键词库**：TESOL领域5大类专业关键词（教学法/评估/教育技术/研究方法/跨文化）
- **台账生成脚本**：接受JSON输入，一键生成4模块交互式HTML

## 适用场景

- 海外硕士申请规划（任何国家/地区、任何专业）
- 院校信息搜集与对比
- 申请竞争力评估与投递策略制定
- 申请简历/CV优化
- 申请进度跟踪与管理

## 安装方法

### 前提条件

- 已安装豆包客户端（Windows / Mac）
- （可选）Python 3.7+，仅用于生成跟踪台账HTML

### 安装步骤

1. **下载或克隆本仓库**
   ```bash
   git clone https://github.com/your-username/study-abroad-application.git
   ```

2. **找到豆包用户技能目录**

   在豆包对话框中发送：
   > 我的用户技能目录在哪里？

   系统会返回准确路径，典型路径如下：

   - **Windows**:
     ```
     C:\Users\{用户名}\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.user_skills\
     ```
   - **Mac**:
     ```
     ~/.doubao/agent_mode/workspace/.user_skills/
     ```

3. **安装技能**

   将 `study-abroad-application` 文件夹整个复制到上述 `.user_skills` 目录中。

   最终路径应为：
   ```
   ...\.user_skills\study-abroad-application\SKILL.md
   ```

4. **重启生效**

   完全关闭豆包客户端后重新打开，或新开会话。

5. **验证安装**

   在新会话中发送：
   > 帮我做留学申请规划

   技能会自动触发并开始工作流。

## 使用方法

安装后，在豆包对话中直接用自然语言描述需求即可，技能会自动识别并触发对应阶段。

### 典型触发语句

```
帮我申请海外TESOL硕士，搜索香港和英国的院校并按匹配度排序
根据我的背景推荐5-8所海外大学，分冲刺/主申/保底
帮我优化留学申请简历，针对教育类专业
生成一份留学申请进度跟踪表
我要申请计算机科学硕士，预算30万，推荐QS前100的院校
```

### 工作流执行

技能会按以下顺序自动推进（也可根据用户需求跳过某些阶段）：

1. 解析你的背景和申请需求
2. 联网搜索目标院校信息
3. 多维度匹配度打分并排序
4. 给出投递优先级建议
5. 针对性优化申请简历
6. 生成可视化跟踪台账

## 文件结构

```
study-abroad-application/
├── SKILL.md                              # 技能主入口（工作流程总览 + 各阶段指引）
├── README.md                             # 本文件（GitHub仓库说明）
├── .gitignore                            # Git忽略规则
├── scripts/
│   └── generate_tracker.py              # 可视化跟踪台账生成脚本
└── references/
    ├── school-research-guide.md         # 院校搜索与信息采集指南
    ├── matching-scoring-framework.md    # 匹配度打分框架
    └── cv-optimization-guide.md         # 简历优化指南
```

### 文件说明

| 文件 | 用途 |
|------|------|
| `SKILL.md` | 技能核心文件，包含YAML元数据和完整工作流程指引，豆包客户端通过此文件识别和加载技能 |
| `scripts/generate_tracker.py` | Python脚本，接受JSON格式的院校数据，生成交互式HTML跟踪台账 |
| `references/school-research-guide.md` | 院校搜索策略、信息采集维度、重点院校速查表、汇率标准、常见陷阱 |
| `references/matching-scoring-framework.md` | 6维度评分标准、权重分配、投递定位分类、输出格式规范 |
| `references/cv-optimization-guide.md` | 简历结构、各板块优化要点、STAR法则、专业关键词库、格式规范、检查清单 |

## 跟踪台账脚本使用

### 命令行用法

```bash
python scripts/generate_tracker.py --input schools.json --output tracker.html
```

### 输入数据格式（JSON）

```json
{
  "applicant": {
    "name": "申请人姓名",
    "program": "申请专业",
    "bg": "背景简述",
    "target_year": "2026"
  },
  "rate_note": "汇率说明",
  "schools": [
    {
      "id": "school1",
      "name": "学校中文名",
      "en": "学校英文名",
      "region": "地区",
      "tier": "主申",
      "tierColor": "#5B7FC4",
      "qs": 36,
      "tuition": 14.9,
      "tuitionStatus": "ok",
      "ielts": "7.0(W≥7.0)",
      "match": 8.6,
      "deadline": "2026-02-28",
      "deadlineText": "2026.02.28",
      "program": "MA TESOL",
      "status": "未开始",
      "note": "注意事项",
      "courses": ["课程1", "课程2"]
    }
  ],
  "common_materials": [
    {"name": "成绩单", "done": false}
  ],
  "school_materials": {
    "school1": ["特殊要求1"]
  }
}
```

### 台账功能

生成的HTML台账包含4个交互模块：
1. **总览对比**：所有院校关键指标一表对比
2. **院校跟踪**：每所院校独立卡片，可点击更新申请状态
3. **截止时间线**：按时间排列的申请节点
4. **材料清单**：通用材料可勾选跟踪 + 各校特殊要求

## 扩展与定制

### 适配其他专业

本技能的工作流程是通用的，申请其他专业时只需：
1. 替换搜索关键词（如"TESOL"→"Computer Science"）
2. 更新 `references/school-research-guide.md` 中的院校速查表
3. 更新 `references/cv-optimization-guide.md` 中的专业关键词库

### 适配其他国家/地区

在 `references/school-research-guide.md` 中添加对应地区的：
- 搜索query模板
- 重点院校速查表
- 汇率标准
- 申请注意事项

## 注意事项

1. **数据真实性**：所有院校信息来自联网搜索，建议以大学官网最新信息为准
2. **时效性**：学费、截止日期、录取要求每年可能变化，使用时注意核实
3. **个体差异**：匹配度打分基于整体背景，实际录取还受文书、推荐信、面试等影响
4. **Python依赖**：仅跟踪台账生成功能需要Python，其他功能不需要
5. **纯本地运行**：技能不调用任何外部API，所有逻辑在本地执行

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个技能。
