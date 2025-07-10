# 简单的测试程序
from agent import Agent

def main():
    print("=== 精简版智能体测试 ===")
    agent = Agent()
    
    while True:
        user_input = input("\n用户: ").strip()
        if user_input.lower() in ['quit', 'exit']:
            break
        
        response = agent.chat(user_input)
        print(f"助手: {response}")

if __name__ == "__main__":
    main() 