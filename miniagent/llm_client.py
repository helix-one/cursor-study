# 精简版LLM客户端
import re
import json

class LLMClient:
    def __init__(self):
        self.model = "模拟LLM"

    def chat(self, messages, temperature=0.7, max_tokens=1500):
        """
        与LLM进行对话
        这里是模拟实现，实际项目中需要调用真实的LLM API
        """
        # 模拟LLM响应
        user_message = messages[-1]["content"] if messages else ""
        
        # 简单的响应逻辑
        if "时间" in user_message or "几点" in user_message:
            return """我需要查询当前时间。
```tool_call
{
    "tool_name": "get_time",
    "parameters": {}
}
```"""
        else:
            return f"我收到了你的消息：{user_message}"

    def extract_tool_call(self, response):
        """
        从LLM响应中提取工具调用
        这是智能体工具调用的核心机制
        """
        # 查找工具调用代码块
        pattern = r'```tool_call\n(.*?)\n```'
        match = re.search(pattern, response, re.DOTALL)
        
        if match:
            tool_call_str = match.group(1).strip()
            tool_call = json.loads(tool_call_str)
            return tool_call
        return None

    def remove_tool_call_from_response(self, response):
        """从响应中移除工具调用部分"""
        pattern = r'```tool_call\n.*?\n```'
        cleaned_response = re.sub(pattern, '', response, flags=re.DOTALL)
        return cleaned_response.strip() 