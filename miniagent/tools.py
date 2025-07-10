# 精简版工具管理
from datetime import datetime
from typing import Dict, Any

class ToolManager:
    def __init__(self):
        # 工具注册表：工具名 -> 工具函数
        self.tools = {
            "get_time": self.get_time
        }

    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """
        执行工具
        这是智能体与外部世界交互的核心机制
        """
        if tool_name not in self.tools:
            return f"错误：未找到工具 {tool_name}"
        
        # 调用对应的工具函数
        return self.tools[tool_name](**parameters)

    def get_time(self) -> str:
        """
        获取当前时间
        这是智能体唯一的工具，用于演示工具调用机制
        """
        now = datetime.now()
        weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][now.weekday()]
        return f"当前时间：{now.strftime('%Y年%m月%d日 %H:%M:%S')} {weekday}" 