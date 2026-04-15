---
title: "Dify 工作流编排实战：安全领域自动化"
category: "其他"
board: "tech"
tags: ["Dify", "工作流", "自动化", "安全"]
summary: "Dify 工作流在安全自动化场景中的实战应用，涵盖节点配置、变量管理、Code 节点与调试技巧"
is_published: true
created_at: "2025-02-15T10:00:00Z"
updated_at: "2025-02-15T10:00:00Z"
---

# Dify 工作流编排实战：安全领域自动化

Dify 是一个开源的 LLM 应用开发平台，它的工作流（Workflow）功能提供了可视化的 AI 应用编排能力。我在安全领域用 Dify 工作流实现了多个自动化场景，本文分享实战中的节点配置技巧和踩坑经验。

## 一、安全自动化场景

在安全运营中，以下场景非常适合用 Dify 工作流自动化：

1. **漏洞情报分析**：自动抓取漏洞公告 → LLM 提取关键信息 → 匹配受影响资产 → 生成处置建议
2. **安全事件研判**：告警日志输入 → 上下文关联 → LLM 判断真假阳 → 输出研判报告
3. **安全报告生成**：汇总扫描数据 → 风险评级 → LLM 生成分析报告 → 格式化输出
4. **IOC 情报提取**：从威胁情报源提取 IP/域名/Hash → 标准化 → 入库

## 二、工作流节点设计

### 2.1 漏洞情报分析工作流

整个工作流由以下节点组成：

```
[开始] → [HTTP请求:获取漏洞] → [Code:数据清洗] → [LLM:信息提取] 
→ [Code:匹配资产] → [条件分支:是否高危] → [LLM:生成建议] → [结束]
                                              ↓
                                        [HTTP请求:发送通知]
```

### 2.2 HTTP 请求节点配置

```yaml
# 节点：获取最新漏洞信息
节点类型: HTTP 请求
方法: GET
URL: https://services.nvd.nist.gov/rest/json/cves/2.0
参数:
  pubStartDate: "{{start_date}}"
  pubEndDate: "{{end_date}}"
  resultsPerPage: 50
请求头:
  apiKey: "{{api_key}}"
超时: 30秒
重试: 2次

# 输出变量
输出: response_body
```

### 2.3 Code 节点：数据清洗

Code 节点是 Dify 工作流中最灵活的节点，支持 Python 和 JavaScript。

```python
# Code 节点：漏洞数据清洗与标准化
def main(input_data: dict) -> dict:
    """
    输入：HTTP 请求返回的原始 NVD 数据
    输出：标准化的漏洞列表
    """
    raw = input_data.get("response_body", {})
    vulnerabilities = raw.get("vulnerabilities", [])
    
    results = []
    for item in vulnerabilities:
        cve = item.get("cve", {})
        
        # 提取 CVSS 评分
        metrics = cve.get("metrics", {})
        cvss_data = None
        for version in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
            if version in metrics:
                cvss_data = metrics[version][0].get("cvssData", {})
                break
        
        cvss_score = cvss_data.get("baseScore", 0) if cvss_data else 0
        
        # 提取描述（中英文）
        descriptions = cve.get("descriptions", [])
        desc_en = next((d["value"] for d in descriptions if d["lang"] == "en"), "")
        
        # 提取受影响产品
        affected = []
        for config in cve.get("configurations", []):
            for node in config.get("nodes", []):
                for match in node.get("cpeMatch", []):
                    if match.get("vulnerable"):
                        cpe = match.get("criteria", "")
                        # 从 CPE 中提取产品名
                        parts = cpe.split(":")
                        if len(parts) >= 5:
                            affected.append(f"{parts[3]}:{parts[4]}")
        
        # 只保留中高危漏洞
        if cvss_score >= 7.0:
            results.append({
                "cve_id": cve.get("id", ""),
                "cvss_score": cvss_score,
                "severity": "critical" if cvss_score >= 9.0 else "high",
                "description": desc_en[:500],
                "affected_products": list(set(affected))[:20],
                "published": cve.get("published", ""),
            })
    
    return {
        "vulnerabilities": results,
        "total_found": len(vulnerabilities),
        "high_risk_count": len(results),
    }
```

**Code 节点最佳实践**：

1. **输入输出类型明确**：始终返回 dict，key 名称要语义化
2. **错误处理**：Code 节点内部异常会导致整个工作流失败，必须 try-except
3. **不要引入外部依赖**：Code 节点只能用标准库，不能 pip install
4. **数据大小控制**：变量在节点间传递有大小限制，大数据要截断

### 2.4 LLM 节点：信息提取

```yaml
# LLM 节点配置
模型: gpt-4o / deepseek-chat
温度: 0.1  # 信息提取场景用低温度
最大输出: 2000 tokens

System Prompt: |
  你是一个专业的安全分析师。你的任务是分析漏洞信息并提取关键安全要素。
  
  输出格式要求（严格 JSON）：
  {
    "risk_assessment": "风险评估描述",
    "attack_vector": "攻击向量",
    "exploit_difficulty": "利用难度（低/中/高）",
    "impact": "影响范围",
    "remediation": "修复建议",
    "priority": "处置优先级（P0/P1/P2/P3）"
  }

User Prompt: |
  请分析以下漏洞信息：
  
  CVE编号: {{cve_id}}
  CVSS评分: {{cvss_score}}
  描述: {{description}}
  受影响产品: {{affected_products}}
  
  请提取关键安全要素并给出处置建议。
```

### 2.5 条件分支节点

```yaml
# 条件分支：判断是否需要紧急通知
条件1: 
  如果 {{severity}} == "critical" 且 {{cvss_score}} >= 9.0
  → 走紧急通知分支（发送钉钉/飞书告警）

条件2:
  如果 {{severity}} == "high" 且 匹配到内部资产
  → 走标准处置分支

默认:
  → 走记录入库分支
```

## 三、变量管理

### 3.1 变量传递机制

Dify 工作流中的变量通过节点间的连接传递。关键要点：

```
开始节点输入变量 → 可在所有下游节点中通过 {{变量名}} 引用
Code 节点输出 → 通过 {{node_name.output_key}} 引用
LLM 节点输出 → 通过 {{node_name.text}} 引用
```

### 3.2 变量调试技巧

```python
# 在 Code 节点中打印调试信息
def main(input_data: dict) -> dict:
    # 把调试信息放在输出中
    debug_info = {
        "received_keys": list(input_data.keys()),
        "vuln_count": len(input_data.get("vulnerabilities", [])),
        "first_item": str(input_data.get("vulnerabilities", [{}])[0])[:200],
    }
    
    # ... 正常处理逻辑 ...
    
    return {
        "result": processed_data,
        "_debug": debug_info,  # 前缀 _ 标记为调试字段
    }
```

### 3.3 复杂变量处理

```python
# 处理 LLM 输出的 JSON（LLM 输出可能包含 markdown 标记）
def main(input_data: dict) -> dict:
    llm_output = input_data.get("llm_response", "")
    
    # 清理 markdown 代码块标记
    text = llm_output.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    
    try:
        parsed = json.loads(text.strip())
    except json.JSONDecodeError:
        # 降级处理：用正则提取关键字段
        import re
        priority_match = re.search(r'"priority"\s*:\s*"(P[0-3])"', text)
        parsed = {
            "priority": priority_match.group(1) if priority_match else "P2",
            "raw_text": text[:500],
            "parse_error": True,
        }
    
    return {"analysis": parsed}
```

## 四、实际工作流案例

### 4.1 安全事件自动研判工作流

```
[开始：告警输入]
    ↓
[Code：告警预处理]
    - 提取源IP、目标IP、告警类型
    - 查询IP信誉库
    - 关联近期告警
    ↓
[LLM：初步研判]
    - 输入：告警详情 + IP信誉 + 历史告警
    - 输出：是否疑似误报、置信度、依据
    ↓
[条件分支]
    ├── 置信度 > 80% 且判定为真实攻击
    │   ↓
    │   [Code：生成处置工单]
    │   ↓
    │   [HTTP：创建Jira工单]
    │   ↓
    │   [HTTP：发送告警通知]
    │
    ├── 置信度 < 30% 且判定为误报
    │   ↓
    │   [Code：记录误报样本]
    │   ↓
    │   [HTTP：更新告警状态为已忽略]
    │
    └── 其他
        ↓
        [LLM：深度分析]
        ↓
        [HTTP：提交人工研判队列]
```

### 4.2 Code 节点：告警预处理

```python
def main(input_data: dict) -> dict:
    alert = input_data.get("alert", {})
    
    # 提取关键字段
    src_ip = alert.get("src_ip", "")
    dst_ip = alert.get("dst_ip", "")
    alert_type = alert.get("type", "")
    raw_log = alert.get("raw_log", "")
    
    # IP 分类
    import ipaddress
    try:
        src_addr = ipaddress.ip_address(src_ip)
        is_internal_src = src_addr.is_private
    except ValueError:
        is_internal_src = False
    
    # 构建上下文
    context = {
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "is_internal_source": is_internal_src,
        "alert_type": alert_type,
        "alert_summary": raw_log[:1000],
        
        # 风险因子
        "risk_factors": [],
    }
    
    # 规则引擎：快速判断
    if alert_type in ["sql_injection", "rce", "webshell_upload"]:
        context["risk_factors"].append("高危攻击类型")
    
    if not is_internal_src:
        context["risk_factors"].append("外部源IP")
    
    # 时间特征
    alert_time = alert.get("timestamp", "")
    if alert_time:
        hour = int(alert_time[11:13]) if len(alert_time) > 13 else 12
        if hour < 6 or hour > 22:
            context["risk_factors"].append("异常时间段")
    
    context["pre_score"] = len(context["risk_factors"]) * 25  # 简单评分
    
    return context
```

## 五、工作流调试技巧

### 5.1 分段调试

不要一次性运行整个工作流。在开发阶段，我的做法是：

1. 先单独调试 Code 节点（用 Python 本地运行测试）
2. 再单独测试 LLM 节点的 prompt（在 Dify 的 prompt 调试工具中）
3. 最后组装整个工作流

### 5.2 Mock 数据

```python
# 在开始节点设置 mock 数据，避免每次都调用真实 API
mock_alert = {
    "alert": {
        "src_ip": "203.0.113.50",
        "dst_ip": "192.168.1.100",
        "type": "sql_injection",
        "raw_log": "GET /api/users?id=1' OR '1'='1 HTTP/1.1",
        "timestamp": "2024-01-20T03:15:00Z"
    }
}
```

### 5.3 错误处理模式

```python
# Code 节点的防御性编程
def main(input_data: dict) -> dict:
    try:
        # 主逻辑
        result = process(input_data)
        return {"status": "success", "data": result}
    except KeyError as e:
        return {
            "status": "error",
            "error_type": "missing_field",
            "error_msg": f"缺少字段: {e}",
            "fallback_data": get_default_data(),
        }
    except Exception as e:
        return {
            "status": "error",
            "error_type": "unknown",
            "error_msg": str(e)[:200],
            "fallback_data": get_default_data(),
        }
```

## 六、性能与成本优化

### 6.1 减少 LLM 调用

LLM 调用是工作流中最慢、最贵的节点。优化策略：

1. **规则前置**：用 Code 节点做规则判断，只有不确定的才调用 LLM
2. **批量处理**：多个漏洞合并到一个 prompt 中分析，而不是每个漏洞调一次 LLM
3. **缓存结果**：相似输入的 LLM 输出可以缓存复用

### 6.2 模型选择

| 节点任务 | 推荐模型 | 原因 |
|---------|---------|------|
| 信息提取 | deepseek-chat | 性价比高，结构化输出稳定 |
| 深度分析 | gpt-4o | 推理能力强，适合复杂判断 |
| 报告生成 | gpt-4o-mini | 文本生成质量够用，成本低 |
| 简单分类 | deepseek-chat | 速度快，成本低 |

## 总结

Dify 工作流在安全自动化中的要点：

1. **Code 节点是核心**：复杂的数据处理和转换都在 Code 节点中完成
2. **LLM 节点要节制**：只在需要"理解"和"推理"的环节使用
3. **变量命名规范**：节点间传递的变量要语义化，避免混乱
4. **防御性编程**：每个 Code 节点都要有错误处理和降级逻辑
5. **分段调试**：先单节点调通，再组装工作流
6. **Prompt 持续迭代**：LLM 节点的 prompt 需要根据实际 case 不断优化
