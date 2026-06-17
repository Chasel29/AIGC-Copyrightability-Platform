from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():

    result = ""
    copyright_score = 0
    copyright_level = ""
    analysis_dimensions = {}
    matched_cases = []
    governance_suggestions = []

    # 平台演示数据（用于研究展示与可视化）
    platform_stats = {
        "cases": 58,
        "surveys": 632,
        "interviews": 26,
        "frameworks": 4,
        "update_time": datetime.now().strftime("%Y-%m-%d")
    }

    # 典型案例展示
    case_library = [
        {
            "title": "Midjourney版权争议案例",
            "type": "AI图像生成",
            "risk": "中风险",
            "issue": "作品独创性认定",
            "view": "需结合人工修改程度综合判断"
        },
        {
            "title": "ChatGPT辅助写作案例",
            "type": "文本生成",
            "risk": "低风险",
            "issue": "人类创作主导性",
            "view": "AI主要承担辅助生成功能"
        },
        {
            "title": "AI仿风格生成案例",
            "type": "风格模仿生成",
            "risk": "高风险",
            "issue": "潜在侵权与商业传播风险",
            "view": "需加强平台审核与版权风险提示"
        },
        {
            "title": "AI音乐生成案例",
            "type": "AIGC音频生成",
            "risk": "中风险",
            "issue": "训练数据合规性",
            "view": "需进一步明确平台责任边界"
        }
    ]

    # 风险场景展示
    risk_scenarios = [
        {
            "level": "低风险",
            "scene": "AI辅助润色与资料整理",
            "description": "人工创作占主导，AI主要承担辅助优化功能"
        },
        {
            "level": "中风险",
            "scene": "AI生成海报与自媒体内容",
            "description": "存在一定原创表达，但训练数据来源可能存在争议"
        },
        {
            "level": "高风险",
            "scene": "AI批量商业化内容生成",
            "description": "自动生成程度较高，存在较明显版权风险"
        }
    ]

    # 可视化演示数据
    chart_data = {
        "groups": ["普通用户", "内容创作者", "法学相关群体", "AIGC高频使用者"],
        "copyright_support": [48, 67, 72, 61],
        "governance_labels": ["平台审核", "AI标识", "法律规制", "行业标准"],
        "governance_values": [32, 24, 28, 16],
        "dimension_labels": [
            "Human Participation",
            "Originality",
            "AI Dependency",
            "Expression Complexity"
        ],
        "dimension_values": [82, 74, 61, 69]
    }

    if request.method == 'POST':

        text = request.form['content']

        # AIGC认知研究辅助分析模块

        creation_mode = "Human–AI Collaborative Creation"
        prompt_creativity = "中等"
        judicial_tendency = "存在争议"

        # TRG V2.0 多因子版权认定模型

        human_match = 0
        originality_match = 0
        ai_match = 0
        complexity_match = 0

        text_lower = text.lower()

        def count_features(feature_dict):
            score = 0
            detected = []

            for label, config in feature_dict.items():
                hit = False

                for kw in config["keywords"]:
                    if kw.lower() in text_lower:
                        hit = True
                        break

                if hit:
                    score += config["weight"]
                    detected.append(label)

            return score, detected

        def semantic_match(keyword_group, content):
            score = 0
            matched = []

            for word in keyword_group:
                if word.lower() in content.lower():
                    score += 1
                    matched.append(word)

            return score, matched

        human_features = {
            "人工深度修改": {"weight": 18, "keywords": ["人工修改", "反复修改", "后期", "重构", "润色"]},
            "创作策划": {"weight": 15, "keywords": ["构思", "策划", "设计", "导演", "脚本"]},
            "创作控制": {"weight": 15, "keywords": ["调整", "多轮", "迭代", "优化", "编排"]},
            "专业工具参与": {"weight": 12, "keywords": ["photoshop", "ps", "剪辑", "editing"]}
        }

        originality_features = {
            "原创世界观": {"weight": 18, "keywords": ["世界观", "原创表达", "角色设定"]},
            "独立创意": {"weight": 15, "keywords": ["独特", "创新", "创意", "个性化"]},
            "艺术表达": {"weight": 12, "keywords": ["视觉风格", "美学", "叙事", "镜头语言"]},
            "复杂内容设计": {"weight": 10, "keywords": ["故事结构", "concept art", "worldbuilding"]}
        }

        ai_features = {
            "直接生成": {"weight": 20, "keywords": ["一键生成", "直接生成", "无需修改"]},
            "高度依赖AI": {"weight": 18, "keywords": ["完全由ai", "fully generated", "automatic"]},
            "生成式工具": {"weight": 10, "keywords": ["chatgpt", "midjourney", "claude", "gemini", "stable diffusion"]}
        }

        complexity_features = {
            "系统结构": {"weight": 18, "keywords": ["系统化", "品牌体系", "交互"]},
            "叙事复杂度": {"weight": 15, "keywords": ["人物关系", "时间线", "多层"]},
            "视觉复杂度": {"weight": 12, "keywords": ["视觉设计", "scene design", "composition"]},
            "空间与架构": {"weight": 10, "keywords": ["architecture", "空间设计"]}
        }

        human_score, human_detected = count_features(human_features)
        originality_score, originality_detected = count_features(originality_features)
        ai_score, ai_detected = count_features(ai_features)
        complexity_score, complexity_detected = count_features(complexity_features)

        text_length = len(text)

        if text_length > 800:
            complexity_score += 10
            originality_score += 5
        elif text_length > 300:
            complexity_score += 5

        if ("人工修改" in text or "多轮" in text) and ("chatgpt" in text_lower or "midjourney" in text_lower):
            human_score += 12
            originality_score += 8

        human_score = min(human_score, 100)
        originality_score = min(originality_score, 100)
        ai_score = min(ai_score, 100)
        complexity_score = min(complexity_score, 100)

        detected_dimensions = (
            human_detected +
            originality_detected +
            ai_detected +
            complexity_detected
        )

        # Prompt创造性分析
        high_prompt_keywords = [
            "赛博朋克", "水墨", "未来", "电影感",
            "蒸汽朋克", "废土", "东方幻想",
            "赛博神话", "意识流", "超现实",
            "cyberpunk", "cinematic", "original architecture",
            "multi-round", "prompt engineering",
            "post-editing", "photoshop",
            "worldbuilding", "visual storytelling"
        ]

        high_prompt_match, _ = semantic_match(high_prompt_keywords, text)

        if high_prompt_match >= 2:
            prompt_creativity = "较高"
        elif high_prompt_match >= 1:
            prompt_creativity = "中等偏高"
        else:
            prompt_creativity = "基础"

        if "多轮" in text or "人工修改" in text or "重构" in text:
            creation_mode = "Deep Human–AI Collaborative Creation"

        # 研究性司法倾向模拟（仅用于案例研究展示）
        if human_score >= 50 and originality_score >= 40 and complexity_score >= 30:
            judicial_tendency = "倾向认可作品属性"

        elif ai_score >= 60 and human_score <= 20:
            judicial_tendency = "倾向不认可完全版权"

        else:
            judicial_tendency = "存在法律争议"

        # TRG V2.0 综合评价模型

        human_weight = 0.35
        originality_weight = 0.30
        complexity_weight = 0.20
        ai_penalty_weight = 0.15

        copyright_score = (
            human_score * human_weight +
            originality_score * originality_weight +
            complexity_score * complexity_weight -
            ai_score * ai_penalty_weight
        )

        collaboration_bonus = 0

        if human_score >= 40 and originality_score >= 40:
            collaboration_bonus += 8

        if complexity_score >= 50:
            collaboration_bonus += 5

        if text_length >= 500:
            collaboration_bonus += 4

        copyright_score += collaboration_bonus + 25

        copyright_score = int(max(20, min(copyright_score, 98)))

        # 研究参考等级判断
        if copyright_score >= 80:
            copyright_level = "高独创性协同创作"
            icon = "🟢"
            legal_opinion = "该内容体现出较强的人类创造性投入与表达控制能力，具有较明显的人机协同创作特征。"

        elif copyright_score >= 60:
            copyright_level = "中等独创性表达"
            icon = "🟠"
            legal_opinion = "该内容存在一定原创表达与人工参与，但AI生成成分相对较高，相关权利认定仍存在争议。"

        else:
            copyright_level = "高度AI生成倾向"
            icon = "🔴"
            legal_opinion = "该内容对AIGC生成依赖程度较高，人类独创性表达相对有限。"

        # 维度等级分析
        def level_text(score):
            if score >= 60:
                return "较高"
            elif score >= 30:
                return "中等"
            else:
                return "较低"

        human_level = level_text(human_score)
        originality_level = level_text(originality_score)
        ai_level = level_text(ai_score)
        complexity_level = level_text(complexity_score)

        analysis_dimensions = {
            "human": human_score,
            "originality": originality_score,
            "ai_dependency": ai_score,
            "complexity": complexity_score
        }

        if detected_dimensions:
            detected_text = ", ".join(detected_dimensions)
        else:
            detected_text = "未检测到明显创作特征"

        # 相似案例推荐
        if "Midjourney" in text or "AI绘画" in text:
            matched_cases.append("AI绘画著作权争议案例")

        if "文案" in text or "ChatGPT" in text:
            matched_cases.append("AI辅助文案创作案例")

        if "风格" in text or "模仿" in text:
            matched_cases.append("仿风格AI生成内容案例")

        if not matched_cases:
            matched_cases = [
                "AIGC内容版权认知案例",
                "平台治理与风险识别案例"
            ]

        # 治理建议
        governance_suggestions = [
            "建议明确标注AI参与程度",
            "建议保留创作过程记录与修改痕迹",
            "商业传播前建议增加版权风险审核"
        ]

        result = f"""
{icon} AIGC Copyrightability Research Analysis

━━━━━━━━━━━━━━━
Research Risk Level
━━━━━━━━━━━━━━━

{copyright_level}
综合分析指数：{copyright_score}/100

━━━━━━━━━━━━━━━
TRG Four-Dimensional Framework
━━━━━━━━━━━━━━━

Human Participation Index：{human_level}
Original Expression Index：{originality_level}
AI Dependency Index：{ai_level}
Expression Complexity：{complexity_level}

Human Participation Score：{analysis_dimensions['human']}/100
Originality Score：{analysis_dimensions['originality']}/100
AI Dependency Score：{analysis_dimensions['ai_dependency']}/100
Complexity Score：{analysis_dimensions['complexity']}/100

━━━━━━━━━━━━━━━
Creative Process Analysis
━━━━━━━━━━━━━━━
Research Confidence Level：Experimental Research Reference

创作模式：{creation_mode}
Prompt创造性：{prompt_creativity}
司法认知倾向：{judicial_tendency}

━━━━━━━━━━━━━━━
Detected Creative Features
━━━━━━━━━━━━━━━

{detected_text}

━━━━━━━━━━━━━━━
Related Case References
━━━━━━━━━━━━━━━

- {matched_cases[0]}
- {matched_cases[-1]}

━━━━━━━━━━━━━━━
Governance Suggestions
━━━━━━━━━━━━━━━

- {governance_suggestions[0]}
- {governance_suggestions[1]}
- {governance_suggestions[2]}

━━━━━━━━━━━━━━━
Research Observation
━━━━━━━━━━━━━━━

{legal_opinion}

━━━━━━━━━━━━━━━
Global Governance Trends
━━━━━━━━━━━━━━━

China: Emphasizes human intellectual contribution and originality
United States: Tends not to protect fully AI-generated content
European Union: Focuses on creator control and collaborative process
Japan: Exploring emerging copyright rules for the AIGC era

━━━━━━━━━━━━━━━
Platform Statement
━━━━━━━━━━━━━━━

This platform is an experimental research and visualization module
for AIGC copyrightability analysis and governance studies.
All analysis results are for academic research reference only
and do not constitute formal legal opinions.
        """

    return render_template(
        'index.html',
        result=result,
        score=copyright_score,
        risk_level=copyright_level,
        dimensions=analysis_dimensions,
        matched_cases=matched_cases,
        governance_suggestions=governance_suggestions,
        stats=platform_stats,
        cases=case_library,
        risks=risk_scenarios,
        charts=chart_data
    )

if __name__ == '__main__':
    app.run(debug=True)