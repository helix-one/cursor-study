# 精简版智能体核心代码
from llm_client import LLMClient
from memory import Memory
from tools import ToolManager

class Agent:
    def __init__(self):
        self.llm = LLMClient()
        self.memory = Memory()
        self.tools = ToolManager()
        self.iteration_count = 0

    def chat(self, user_input: str) -> str:
        """与用户对话的主要方法"""
        self.iteration_count = 0
        self.memory.add_message("user", user_input)
        response = self._process_message(user_input)
        self.memory.add_message("assistant", response)
        return response

    def _process_message(self, user_input: str) -> str:
        """处理消息的核心逻辑"""
        messages = self._build_messages(user_input)
        response = self.llm.chat(messages)
        tool_call = self.llm.extract_tool_call(response)
        
        if tool_call:
            return self._handle_tool_call(response, tool_call, user_input)
        else:
            return response

    def _handle_tool_call(self, response: str, tool_call: dict, original_input: str) -> str:
        """处理工具调用"""
        self.iteration_count += 1
        
        # 防止无限循环
        if self.iteration_count > 5:
            return "达到最大迭代次数限制"
        
        tool_name = tool_call.get("tool_name")
        tool_result = self.tools.execute_tool(tool_name, tool_call.get("parameters", {}))
        
        # 构建包含工具结果的消息
        context_messages = self._build_messages(original_input)
        tool_message = f"工具调用：{tool_call}\n工具结果：{tool_result}"
        context_messages.append({"role": "user", "content": tool_message})
        
        # 继续处理
        next_response = self.llm.chat(context_messages)
        next_tool_call = self.llm.extract_tool_call(next_response)
        
        if next_tool_call:
            return self._handle_tool_call(next_response, next_tool_call, original_input)
        else:
            return next_response

    def _build_messages(self, user_input: str) -> list:
        """构建发送给LLM的消息列表"""
        messages = []
        
        # 系统提示词
        system_message = """你是一个智能助手，具有以下能力：
1. 规划：能够将复杂任务分解为多个步骤
2. 记忆：能够记住之前的对话内容
3. 工具使用：能够调用工具来完成任务

当你需要使用工具时，请按以下格式输出：
```tool_call
{
    "tool_name": "工具名称",
    "parameters": {"参数名": "参数值"}
}
```

可用工具：
- get_time: 获取当前时间，无需参数
"""
        messages.append({"role": "system", "content": system_message})
        
        # 添加记忆中的上下文
        context_messages = self.memory.get_context_messages()
        messages.extend(context_messages)
        
        # 添加当前用户输入
        if not context_messages or context_messages[-1]["content"] != user_input:
            messages.append({"role": "user", "content": user_input})
        
        return messages 