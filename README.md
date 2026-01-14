# Luigi Prompt - 语音外呼代理提示词管理系统

## 项目简介

Luigi Prompt 是一个专为电话外呼代理（Telephony Outbound Call Agent）设计的提示词管理框架。它通过可复用的节点（Node）和流程（Flow）架构，解决了传统硬编码方式下提示词维护困难的问题。
See [example.md](example.md) for an example.
## 背景与痛点

在电话外呼场景中，代理通常需要按照状态机的方式完成一系列任务。传统做法是将整个对话流程硬编码在提示词中，但这带来了以下问题：

- **维护困难**：产品逻辑变更时，需要修改大段提示词
- **复用性差**：相同的对话环节在不同流程中无法复用
- **可读性低**：复杂的状态转换逻辑难以理解和审查
- **迭代缓慢**：每次需求变更都需要重新编写和测试整个提示词

## 核心设计理念

Luigi Prompt 采用**节点组合**的思想：

1. **节点（ConversationNode）**：代表对话流程中的一个环节，包含描述、指令、示例和转换条件
2. **流程（ConversationFlow）**：由多个节点组成，通过转换关系（Transition）连接
3. **复用性**：节点可在不同流程中重复使用
4. **声明式**：通过简单的代码声明节点关系，而非硬编码复杂逻辑

## 架构说明

### 文件结构

```
luigi_prompt/
├── base.py          # 核心抽象类：ConversationNode, Transition, ConversationFlow
├── nodes.py         # 可复用节点库
├── flow.py          # 流程组装逻辑
└── README.md        # 项目文档
```

### 核心组件

#### 1. ConversationNode（对话节点）

```python
@dataclass
class ConversationNode:
    name: str                    # 节点名称
    description: str             # 节点描述
    instructions: list[str]      # 执行指令
    examples: list[str]          # 示例话术
```

**主要方法**：
- `transit_to(node, condition)` - 定义到下一个节点的转换条件
- `format()` - 生成格式化的提示词文本

#### 2. Transition（转换关系）

```python
@dataclass
class Transition:
    condition: str               # 转换条件
    target_node: ConversationNode  # 目标节点
```

#### 3. ConversationFlow（对话流程）

```python
class ConversationFlow:
    def __init__(self, nodes: list[ConversationNode], 
                 global_instructions: str)
```

**主要方法**：
- `format(**kwargs)` - 生成完整的提示词，支持动态上下文变量

## 使用示例

### 1. 定义可复用节点（nodes.py）

```python
from base import ConversationNode

# 问候节点
greeting = ConversationNode(
    name='greeting',
    description="问候用户，询问是否需要金融支持",
    instructions=["简洁、温暖，包含用户姓名（如可用）"],
    examples=["您好 {{用户姓名}}，我是您的金融顾问，请问您需要金融支持吗？"]
)

# 车辆所有权询问节点
car_ownership = ConversationNode(
    name='car_ownership',
    description="询问车辆所有权",
    instructions=["询问用户是否拥有车辆"],
    examples=["请问您有车吗？"]
)
```

### 2. 组装对话流程（flow.py）

```python
from nodes import greeting, car_ownership, drive_liscence_availability
from base import ConversationFlow

def create_flow_financial_assistant() -> ConversationFlow:
    # 定义节点转换关系
    greeting.transit_to(
        node=car_ownership,
        condition="用户回应问候"
    )
    
    car_ownership.transit_to(
        node=drive_liscence_availability,
        condition="用户表示拥有车辆"
    )
    
    car_ownership.transit_to(
        node=end_conversation_unqualified,
        condition="用户表示没有车辆"
    )
    
    # 创建流程
    flow = ConversationFlow(
        nodes=[greeting, car_ownership, drive_liscence_availability, ...],
        global_instructions="你是一个金融助手，引导客户回答一系列问题。"
    )
    
    return flow
```

### 3. 生成提示词

```python
# 创建流程
flow = create_flow_financial_assistant()

# 注入上下文变量并生成提示词
instruction = flow.format(
    customer_name="张三",
    customer_age=30,
    call_time="2026年1月14日 14:30"
)

print(instruction)
```

### 输出示例

```
你是一个金融助手，引导客户回答一系列问题。

<Conversation Flow Definition>
{
  "id": "1_greeting",
  "description": "问候用户，询问是否需要金融支持",
  "instructions": ["简洁、温暖，包含用户姓名（如可用）"],
  "examples": ["您好 {{用户姓名}}，我是您的金融顾问，请问您需要金融支持吗？"],
  "transitions": [
    {"condition": "用户回应问候", "target_node": "car_ownership"}
  ]
}

{
  "id": "2_car_ownership",
  "description": "询问车辆所有权",
  "instructions": ["询问用户是否拥有车辆"],
  "examples": ["请问您有车吗？"],
  "transitions": [
    {"condition": "用户表示拥有车辆", "target_node": "drive_liscence_availability"},
    {"condition": "用户表示没有车辆", "target_node": "end_conversation_unqualified"}
  ]
}
...
</Conversation Flow Definition>

<Conversation context>
customer_name = 张三
customer_age = 30
call_time = 2026年1月14日 14:30
</Conversation context>
```

## 核心优势

### ✅ 高度可复用
- 节点可在不同业务场景中重复使用
- 例如：`greeting`、`end_conversation` 等通用节点

### ✅ 易于维护
- 产品逻辑变更时，只需调整节点组合关系
- 无需重写整个提示词

### ✅ 清晰可读
- 声明式的转换关系，一目了然
- 便于产品经理和开发人员协作

### ✅ 灵活扩展
- 支持动态上下文变量注入
- 可轻松添加新节点和转换条件

### ✅ 适应业务变化
- 外呼业务逻辑经常变化，可快速重组流程
- 新需求只需创建新节点或调整现有节点组合

## 使用场景

Luigi Prompt 特别适合以下场景：

- 🎯 **金融贷款外呼**：资质审核、产品推荐
- 🎯 **保险销售外呼**：需求调研、方案介绍
- 🎯 **客户回访外呼**：满意度调查、续费提醒
- 🎯 **市场调研外呼**：问卷调查、数据收集
- 🎯 **催收提醒外呼**：还款确认、协商方案

## 快速开始

```bash
# 克隆项目
git clone <repository_url>

# 运行示例
python flow.py
```

## 扩展建议

1. **节点验证**：确保所有转换都指向有效节点
2. **流程可视化**：生成状态机图表
3. **版本控制**：记录流程变更历史
4. **JSON 配置**：支持从配置文件加载流程
5. **测试框架**：为节点转换编写单元测试
6. **文档生成**：自动生成流程文档

## 许可证

MIT License

## 贡献指南

欢迎提交 Issue 和 Pull Request！

---

**Luigi Prompt** - 让外呼提示词管理更简单、更灵活！
