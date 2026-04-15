---
title: "Prompt Engineering 实战：从数据回收到模型优化"
category: "机器学习"
board: "tech"
tags: ["Prompt Engineering", "LLM", "数据标注", "模型优化"]
summary: "Prompt Engineering 实战方法论，涵盖 prompt 设计、0 分 case 回溯分析、精确率优化到 95% 与 system prompt 迭代经验"
is_published: true
created_at: "2025-04-01T10:00:00Z"
updated_at: "2025-04-01T10:00:00Z"
---

# Prompt Engineering 实战：从数据回收到模型优化

Prompt Engineering 不是简单的"调词"，而是一套系统工程。在 Reward Model 训练数据管道项目中，我负责通过 prompt 优化将标注数据的精确率从 72% 提升到 95%。本文分享完整的方法论和实操经验。

## 一、项目背景

我们的目标是用 LLM 替代部分人工标注，为 Reward Model 生成高质量的偏好数据。具体任务是对两个模型回复进行质量比较，输出"哪个更好"的判断。

核心指标：
- **精确率（Precision）**：LLM 标注结果与人工标注一致的比例
- **一致性（Consistency）**：同一样本多次标注结果相同的比例
- **覆盖率（Coverage）**：LLM 能给出明确判断（而非"差不多"）的比例

初始状态：精确率 72%、一致性 80%、覆盖率 65%

## 二、Prompt 设计方法论

### 2.1 第一版：朴素 prompt（精确率 72%）

```
请比较以下两个回复的质量，判断哪个更好。

问题：{question}

回复A：{response_a}

回复B：{response_b}

请输出你的判断：A更好 / B更好 / 差不多
```

问题：
- 评判标准模糊，模型按自己的"感觉"判断
- 输出格式不稳定，有时输出"都不太好"、"各有优劣"
- 对长回复倾向性高（长度偏差）

### 2.2 第二版：结构化评判（精确率 80%）

```python
SYSTEM_PROMPT = """你是一个专业的内容质量评估员。你需要根据明确的评分维度来比较两个回复的质量。

## 评分维度（按权重排序）
1. **准确性**（权重40%）：事实是否正确，是否有错误信息
2. **完整性**（权重25%）：是否完整回答了问题的所有方面
3. **清晰度**（权重20%）：表达是否清晰、逻辑是否连贯
4. **有用性**（权重15%）：对提问者是否真正有帮助

## 评判规则
- 如果一个回复在准确性上有明显错误，直接判定为更差
- 不要因为回复更长就判定更好（长度偏差）
- 如果两个回复质量确实非常接近（各维度差异<5%），才判定为平局
- 必须给出明确判断，"平局"的比例应控制在10%以内

## 输出格式（严格 JSON）
{
    "accuracy": {"a_score": 0-10, "b_score": 0-10, "reason": "..."},
    "completeness": {"a_score": 0-10, "b_score": 0-10, "reason": "..."},
    "clarity": {"a_score": 0-10, "b_score": 0-10, "reason": "..."},
    "usefulness": {"a_score": 0-10, "b_score": 0-10, "reason": "..."},
    "overall_winner": "A" | "B" | "TIE",
    "confidence": 0.0-1.0,
    "key_reason": "一句话总结判断依据"
}"""
```

### 2.3 第三版：消除位置偏差（精确率 87%）

分析发现一个严重问题：模型对第一个出现的回复有显著偏好（位置偏差，约 8% 的影响）。

```python
import random

async def compare_with_debiasing(question: str, response_a: str, response_b: str):
    """双向对比消除位置偏差"""
    
    # 第一次：正序（A在前，B在后）
    result_ab = await llm_compare(question, response_a, response_b)
    
    # 第二次：反序（B在前，A在后）
    result_ba = await llm_compare(question, response_b, response_a)
    # 注意：result_ba 的结果需要翻转
    
    # 判定逻辑
    winner_ab = result_ab["overall_winner"]
    winner_ba = "B" if result_ba["overall_winner"] == "A" else (
        "A" if result_ba["overall_winner"] == "B" else "TIE"
    )
    
    if winner_ab == winner_ba:
        # 两次结果一致，高置信度
        return {
            "winner": winner_ab,
            "confidence": max(result_ab["confidence"], result_ba["confidence"]),
            "consistent": True,
        }
    else:
        # 两次结果不一致，取加权分数
        score_a = (
            result_ab["weighted_score_a"] + result_ba["weighted_score_a"]
        ) / 2
        score_b = (
            result_ab["weighted_score_b"] + result_ba["weighted_score_b"]
        ) / 2
        
        diff = abs(score_a - score_b)
        if diff < 0.5:
            winner = "TIE"
        else:
            winner = "A" if score_a > score_b else "B"
        
        return {
            "winner": winner,
            "confidence": min(result_ab["confidence"], result_ba["confidence"]),
            "consistent": False,
            "score_diff": diff,
        }
```

### 2.4 第四版：few-shot + 边界案例（精确率 92%）

```python
FEW_SHOT_EXAMPLES = """
## 示例 1：准确性差异明显
问题：Python 中 list 和 tuple 的区别是什么？
回复A：list 是可变的，tuple 是不可变的。list 用方括号，tuple 用圆括号。
回复B：list 是可变的，tuple 是不可变的。list 用方括号，tuple 用圆括号。tuple 因为不可变所以可以作为字典的 key，而且 tuple 的创建和访问速度比 list 快。
判断：B更好
原因：两者准确性都没问题，但 B 更完整，补充了 hashable 特性和性能差异这两个重要区别。

## 示例 2：长度不等于质量
问题：如何用 Python 读取文件？
回复A：使用 open() 函数：with open('file.txt', 'r') as f: content = f.read()。推荐使用 with 语句自动管理文件关闭。
回复B：Python 读取文件有很多方法，首先你需要了解文件系统的概念，文件系统是操作系统用来......（长篇幅但核心内容稀疏）
判断：A更好
原因：A 虽然更短，但直接回答了问题，代码示例正确且提到了最佳实践。B 虽然更长但信噪比低。

## 示例 3：边界案例
问题：解释量子计算的基本原理
回复A：量子计算利用量子叠加和量子纠缠......（基本正确但有一处表述不够严谨）
回复B：量子计算是基于量子力学原理......（完全正确但过于简略）
判断：TIE
原因：A 在完整性上更好但有小瑕疵，B 准确但过于简略。综合评估差异在边界范围内。
"""
```

### 2.5 最终版：system prompt 精细调优（精确率 95%）

```python
FINAL_SYSTEM_PROMPT = """你是一个严格的内容质量评估专家，专门负责比较两个AI回复的质量。

## 核心原则
1. 准确性是第一优先级：任何事实错误都是严重扣分项
2. 回复长度≠回复质量：不要因为一个回复更长就偏向它
3. 关注问题的核心诉求：回复是否真正解决了提问者的问题
4. 注意幻觉：编造的信息比没有回答更糟糕

## 具体评判标准

### 准确性评分（0-10）
- 10分：完全准确，无任何错误
- 7-9分：基本准确，有微小不严谨
- 4-6分：有部分错误但核心正确
- 0-3分：有重大事实错误或严重幻觉

### 完整性评分（0-10）
- 10分：全面覆盖问题所有方面
- 7-9分：覆盖主要方面，缺少次要细节
- 4-6分：只回答了部分问题
- 0-3分：严重偏题或回答不相关

### 清晰度评分（0-10）
- 10分：逻辑清晰，结构合理，易于理解
- 7-9分：基本清晰，偶有跳跃
- 4-6分：表达混乱但能理解
- 0-3分：难以理解

### 有用性评分（0-10）
- 10分：直接可操作，对提问者非常有帮助
- 7-9分：有帮助但可能需要额外信息
- 4-6分：有一定参考价值
- 0-3分：基本没有帮助

## 加权公式
总分 = 准确性 * 0.40 + 完整性 * 0.25 + 清晰度 * 0.20 + 有用性 * 0.15

## 判定规则
- 总分差 >= 0.8：明确判定分高的获胜
- 总分差 < 0.8 但 >= 0.3：倾向分高的，但需要在 key_reason 中说明
- 总分差 < 0.3：判定为 TIE
- 特殊规则：如果一方有明确的事实错误（准确性 <= 5），无论总分如何，判定对方获胜

## 易犯错误提醒
- 不要偏向更长的回复
- 不要偏向使用更多专业术语的回复
- 不要偏向更"政治正确"但回避问题的回复
- 代码类问题要实际验证代码逻辑是否正确"""
```

## 三、0 分 Case 回溯分析

这是提升精确率的核心方法。每次迭代后，我会系统分析所有判断错误的案例。

### 3.1 错误分类体系

```python
class ErrorCategory(Enum):
    LENGTH_BIAS = "长度偏差"          # 偏向更长的回复
    POSITION_BIAS = "位置偏差"        # 偏向第一个回复
    HALLUCINATION_MISS = "漏检幻觉"   # 没发现回复中的编造内容
    OVER_STRICT = "过度严格"          # 把正确但不完美的判为很差
    UNDER_STRICT = "过度宽松"         # 对错误太宽容
    FORMAT_CONFUSE = "格式混淆"       # 被排版好的回复迷惑
    DOMAIN_ERROR = "领域知识不足"      # 在专业领域判断失误
    TIE_EXCESS = "过度平局"           # 明显有好坏却判为平局

def analyze_errors(test_results: list[dict]) -> dict:
    """分析错误分布"""
    errors = [r for r in test_results if r["predicted"] != r["ground_truth"]]
    
    categories = {}
    for error in errors:
        cat = classify_error(error)
        categories[cat] = categories.get(cat, 0) + 1
    
    total_errors = len(errors)
    report = {}
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        report[cat] = {
            "count": count,
            "percentage": f"{count/total_errors*100:.1f}%",
            "sample_cases": get_sample_cases(errors, cat, n=3),
        }
    
    return report
```

### 3.2 各版本错误分布

| 错误类型 | V1 (72%) | V2 (80%) | V3 (87%) | V4 (92%) | V5 (95%) |
|---------|----------|----------|----------|----------|----------|
| 长度偏差 | 25% | 15% | 8% | 3% | 1% |
| 位置偏差 | 20% | 18% | 2% | 1% | 1% |
| 漏检幻觉 | 15% | 12% | 10% | 5% | 2% |
| 过度平局 | 18% | 10% | 8% | 4% | 3% |
| 领域知识不足 | 8% | 10% | 12% | 8% | 5% |
| 其他 | 14% | 35% | 60% | 79% | 88% |

### 3.3 针对性优化

**案例：漏检幻觉**

分析发现，LLM 在医学和法律领域容易漏检幻觉内容。

```python
# 在 prompt 中添加领域特殊规则
DOMAIN_RULES = """
## 高风险领域特殊规则
对于以下领域的问题，准确性权重提升到60%：
- 医学/健康：任何不准确的医疗建议都是严重错误
- 法律：法律条文引用必须准确
- 金融：数据和计算必须精确
- 安全：安全建议必须基于当前最佳实践

在这些领域，如果你无法验证某个事实的准确性，应倾向于判定该回复质量较低。
"""
```

**案例：过度平局**

```python
# 在 prompt 中增加反平局指引
ANTI_TIE = """
## 关于 TIE 的严格限制
- TIE 不是"我不确定"的同义词
- 只有当两个回复在每个维度的差异都小于1分时才可以判 TIE
- 如果你倾向于判 TIE，请再仔细看一遍两个回复的准确性
- 强制要求：TIE 比例应低于15%
"""
```

## 四、评估体系

### 4.1 测试集设计

```python
class EvalDataset:
    """评估数据集管理"""
    
    def __init__(self):
        self.categories = {
            "easy": [],      # 明显差异，baseline 都能判对
            "medium": [],    # 需要仔细分析
            "hard": [],      # 边界案例，人工标注也有分歧
            "trap": [],      # 长度陷阱、幻觉陷阱等
        }
    
    def evaluate(self, model_results: list) -> dict:
        """分类别评估"""
        results = {}
        for category, samples in self.categories.items():
            correct = sum(
                1 for s in samples 
                if model_results[s["id"]] == s["ground_truth"]
            )
            results[category] = {
                "accuracy": correct / len(samples),
                "total": len(samples),
                "correct": correct,
            }
        
        # 整体精确率
        total_correct = sum(r["correct"] for r in results.values())
        total_samples = sum(r["total"] for r in results.values())
        results["overall"] = {
            "accuracy": total_correct / total_samples,
            "total": total_samples,
        }
        
        return results
```

### 4.2 A/B 测试

每次 prompt 修改都要做 A/B 测试：

```python
async def ab_test(prompt_a: str, prompt_b: str, test_set: list) -> dict:
    """A/B 测试两个 prompt 版本"""
    results_a = await batch_evaluate(prompt_a, test_set)
    results_b = await batch_evaluate(prompt_b, test_set)
    
    # 统计检验
    from scipy import stats
    _, p_value = stats.mcnemar(
        build_contingency_table(results_a, results_b)
    )
    
    return {
        "prompt_a_accuracy": calculate_accuracy(results_a),
        "prompt_b_accuracy": calculate_accuracy(results_b),
        "p_value": p_value,
        "significant": p_value < 0.05,
        "recommendation": "B" if results_b > results_a and p_value < 0.05 else "A",
    }
```

## 五、数据管道集成

```python
class RewardDataPipeline:
    """Reward Model 训练数据管道"""
    
    async def process_batch(self, pairs: list[dict]) -> list[dict]:
        """处理一批比较对"""
        results = []
        
        for pair in pairs:
            # 1. LLM 标注（双向消除偏差）
            judgment = await self.compare_with_debiasing(
                pair["question"],
                pair["response_a"],
                pair["response_b"]
            )
            
            # 2. 质量控制
            if judgment["confidence"] < 0.6:
                # 低置信度，送人工复审
                await self.send_to_human_review(pair, judgment)
                continue
            
            if not judgment["consistent"]:
                # 双向不一致，送人工复审
                await self.send_to_human_review(pair, judgment)
                continue
            
            # 3. 生成训练数据
            results.append({
                "prompt": pair["question"],
                "chosen": pair[f"response_{judgment['winner'].lower()}"],
                "rejected": pair[f"response_{'b' if judgment['winner'] == 'A' else 'a'}"],
                "confidence": judgment["confidence"],
                "metadata": {
                    "source": "llm_auto",
                    "model": "gpt-4o",
                    "prompt_version": "v5",
                }
            })
        
        return results
```

## 六、经验总结

### Prompt 迭代的核心方法

1. **每次只改一个变量**：不要同时改评分标准和输出格式
2. **量化对比**：每次修改都跑完整测试集，用数字说话
3. **错误驱动优化**：分析 0 分 case 找到错误模式，针对性修改
4. **防过拟合**：不要针对个别 case 写特殊规则，要找到通用模式
5. **版本管理**：每个 prompt 版本都要记录修改原因和效果

### 精确率提升路线图

```
72% → 80%：结构化评分维度 + 明确输出格式
80% → 87%：双向对比消除位置偏差
87% → 92%：Few-shot 示例 + 边界案例处理
92% → 95%：0 分 case 针对性优化 + 领域特殊规则
```

关键认知：**从 90% 到 95% 的提升，比从 70% 到 90% 难得多**。最后 5% 需要对错误案例进行逐条分析，找到系统性的模式，然后在不影响已有正确判断的前提下做微调。这是一个精细的工程过程，不是灵感闪现。
