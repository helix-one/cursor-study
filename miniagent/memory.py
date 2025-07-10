# 精简版记忆管理
from typing import List, Dict

class Memory:
    def __init__(self):
        self.conversations: List[Dict] = []

    def add_message(self, role: str, content: str):
        """
        添加消息到记忆中
        """
        self.conversations.append({
            "role": role,
            "content": content
        })
        
        # 如果对话太长，保留最近的20条
        if len(self.conversations) > 20:
            self.conversations = self.conversations[-20:]

    def get_context_messages(self) -> List[Dict]:
        """
        获取用于LLM的上下文消息
        智能体通过这个方法获取历史对话上下文
        """
        # 返回最近的10条对话作为上下文
        return self.conversations[-10:]

    def clear(self):
        """清空记忆"""
        self.conversations = [] 