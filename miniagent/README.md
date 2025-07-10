# 🤖 精简版智能体代码解读

这是一个去掉调试信息和复杂功能的精简版智能体，展示了构建智能体的核心原理。

## 📁 文件结构

```
miniagent/
├── agent.py      # 智能体核心逻辑
├── llm_client.py # LLM客户端（模拟实现）
├── memory.py     # 记忆管理
├── tools.py      # 工具管理
├── main.py       # 测试程序
└── README.md     # 本文件
```

## 🧠 核心原理

### 1. 智能体架构

```
用户输入 → Agent → LLM → 工具调用 → 结果返回
           ↑                    ↓
        Memory ←─────────────────┘
```

### 2. 工具调用机制

智能体通过以下步骤实现工具调用：

1. **LLM输出特定格式**：
   ```
   ```tool_call
   {
       "tool_name": "get_time",
       "parameters": {}
   }
   ```
   ```

2. **正则表达式解析**：
   ```python
   pattern = r'```tool_call\n(.*?)\n```'
   match = re.search(pattern, response, re.DOTALL)
   ```

3. **执行工具并返回结果**：
   ```python
   tool_result = self.tools.execute_tool(tool_name, parameters)
   ```

## 📄 代码解读

### agent.py - 智能体核心

```python
class Agent:
    def __init__(self):
        self.llm = LLMClient()      # LLM客户端
        self.memory = Memory()       # 记忆管理
        self.tools = ToolManager()   # 工具管理
```

**核心方法：**
- `chat()`: 主要对话入口，处理用户输入
- `_process_message()`: 处理消息，判断是否需要工具调用
- `_handle_tool_call()`: 处理工具调用，支持多轮迭代
- `_build_messages()`: 构建发送给LLM的消息列表

**关键设计：**
- 迭代控制：防止无限循环
- 记忆管理：自动保存对话历史
- 工具调用：解析LLM输出并执行工具

### llm_client.py - LLM客户端

```python
class LLMClient:
    def chat(self, messages):
        # 模拟LLM响应
        # 实际项目中这里会调用真实的LLM API
        
    def extract_tool_call(self, response):
        # 从LLM响应中提取工具调用
        # 这是工具调用的核心机制
```

**核心功能：**
- 模拟LLM对话
- 解析工具调用指令
- 清理响应文本

### memory.py - 记忆管理

```python
class Memory:
    def __init__(self):
        self.conversations = []  # 对话历史
        
    def add_message(self, role, content):
        # 添加消息到记忆
        
    def get_context_messages(self):
        # 获取上下文消息
        return self.conversations[-10:]  # 最近10条
```

**核心功能：**
- 存储对话历史
- 自动限制记忆长度
- 提供上下文给LLM

### tools.py - 工具管理

```python
class ToolManager:
    def __init__(self):
        self.tools = {
            "get_time": self.get_time  # 工具注册
        }
        
    def execute_tool(self, tool_name, parameters):
        # 执行工具
        return self.tools[tool_name](**parameters)
```

**核心功能：**
- 工具注册和管理
- 工具执行
- 错误处理

## 🔄 工作流程

1. **用户输入** → `agent.chat()`
2. **构建消息** → `_build_messages()` (包含系统提示词 + 记忆上下文)
3. **LLM处理** → `llm.chat()`
4. **检查工具调用** → `extract_tool_call()`
5. **如果需要工具**：
   - 执行工具 → `tools.execute_tool()`
   - 将结果反馈给LLM
   - 继续处理直到得到最终答案
6. **保存到记忆** → `memory.add_message()`
7. **返回响应**

## 🎯 核心概念

### 1. 提示词工程
通过精心设计的系统提示词，让LLM知道何时以及如何调用工具。

### 2. 结构化输出
LLM输出特定格式的工具调用指令，代码解析后执行。

### 3. 迭代处理
支持多轮工具调用，直到完成任务。

### 4. 上下文管理
通过记忆系统保持对话的连贯性。

## 🚀 运行测试

```bash
cd miniagent
python main.py
```

测试示例：
- 输入："现在几点了？"
- 输出：智能体会调用get_time工具并返回当前时间

## 💡 扩展建议

1. **添加更多工具**：在tools.py中注册新工具
2. **改进LLM客户端**：连接真实的LLM API
3. **增强记忆管理**：添加记忆压缩和持久化
4. **优化提示词**：提高工具调用的准确性

这个精简版本展示了智能体的核心原理：**通过结构化提示词让LLM输出结构化指令，然后通过代码解析和执行这些指令，实现LLM与外部世界的交互。** 