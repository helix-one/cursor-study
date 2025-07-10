知识点

1. Cursor简介  
- Cursor 是基于 VSCode 的 AI 编辑器。  
- Github Copilot AI 插件权限受限（如只能插入文本，不能删除文本）。

2. Tab操作  
- 打开 Tab：设置 -> Tab 打开。

3. 对话功能  
- 快捷键：Ctrl + L（类似 ChatGPT 对话）。

4. 修改功能  
- 快捷键：Ctrl + K（类似 ChatGPT 对话）。

5. Composer功能  
- 可重建、修改文件。  
- 生成网页测试正常，删除操作较慢（按下 accept 后才完成删除）。  
- 目前 Composer 与 Chat 已合并。  
- 如不需生成文件，需在 Chat 中明确指出。  
- Claude-4-Sonnet 偏好生成和执行文件。

6. Docs文档管理  
- docs 可为链接文档，结尾加 / 可读取当前及链接文档。  
- 可先录入后使用，也可直接 @ 后 addlink。

7. Codebase管理  
- 位于 Indexing & Docs 中。  
- 可用 .cursorignore 忽略文件，提高效率。

8. Cursor Rule  
- 可设置全局规则，如要求回答中文。

9. 避免 Composer 随意修改代码的方法  
- 回答需清晰全面：  
  1) 让 AI 复述需求  
  2) 范围足够精确  
  3) 多个需求分条列出  
  4) 必要时给出思路和案例

10. Nodepad使用  
- 详细描述需求（如复杂 bug 修复），在 nodepad 中记录，然后用 @nodepad。

11. 模型选择建议  
- GPT-4o：日常使用  
- Claude-4：写代码  
- O3：推理、建模、论文讨论  
- Gemini：数学推导

12. Chat历史记录管理  
- 历史记录与文件夹关联。  
- 可用 specstory 插件将 chat 保存在本地。

13. 插件安装建议  
- 尽量在虚拟环境中安装新插件，避免污染 base 环境

使用
1. 和chat对话，明确需求，指定范围，指定mcp比模糊更好

一、构建mcp server（以weather为例）

1. 前期准备
- 安装uv：在powershell中运行  
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
- 卸载anaconda并重装，可解决conda下载慢、python版本过旧等问题
- uv venv --python 3.13 可指定python版本创建虚拟环境（如失败，需检查uv自带python版本，建议使用3.10及以上）
- 使用uv python list查看已安装python，uv python uninstall 3.9.23卸载不需要的版本

2. 创建weather项目
- uv init weather
- cd weather
- uv venv
- .venv\Scripts\activate
- uv add mcp[cli] httpx
- new-item weather.py

3. 编写weather.py（核心结构如下）
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    # 请求NWS API，异常处理
    ...

def format_alert(feature: dict) -> str:
    # 格式化预警信息
    ...

@mcp.tool()
async def get_alerts(state: str) -> str:
    # 获取指定州的天气预警
    ...

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    # 获取指定经纬度的天气预报
    ...

if __name__ == "__main__":
    mcp.run(transport='stdio')

4. 配置mcp.json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\ABSOLUTE\\PATH\\TO\\PARENT\\FOLDER\\weather",
        "run",
        "weather.py"
      ]
    }
  }
}

二、构建eyelevelRAG mcp
- 参考：https://github.com/patchy631/ai-engineering-hub/tree/main/eyelevel-mcp-rag
- 复制代码，按weather流程构建

三、构建groundx mcp工具
- 在虚拟环境中pip install groundx
- 修改代码：client = GroundX(api_key="xxxxxxxxxxxx")，填写自己的apikey
- @mcp注释需详细，注释为功能描述，代码为使用案例
- 确认bucket id正确，否则无法访问
- 测试分析和上传功能


使用python控制matlab
1.创建虚拟环境，下载matlab engine api需要3.10，安装3.10然后下载并且将虚拟环境的python设置为3.10
2. 让cursor编写代码，先让cursor阅读PIVlab_GUI.m，然后整理如何执行导入图片，设置piv参数，导出结果，别多轮测试保存结果没有问题

待办
没有尝试接入外部mcp
1. 搜索论文库的mcp
2. 
