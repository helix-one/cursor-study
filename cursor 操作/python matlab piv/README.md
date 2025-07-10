# PIV分析自动化工具

这是一个使用Python控制MATLAB PIVlab进行PIV（粒子图像测速）分析的自动化工具。

## 功能特点

✅ **完全自动化** - 无需手动点击GUI界面  
✅ **批量处理** - 自动处理文件夹中的所有图像  
✅ **参数化配置** - 灵活的配置文件设置  
✅ **结果导出** - 自动导出分析结果和会话文件  
✅ **错误处理** - 完善的异常处理机制  

## 系统要求

### 必需软件
- **MATLAB** (R2016b 或更高版本)
- **PIVlab** (版本 2.62 或兼容版本)
- **Python** ⚠️ **特定版本要求**: 2.7, 3.8, 3.9, 或 3.10 (推荐3.10)

### Python依赖
- numpy
- matlab.engine (MATLAB Engine for Python)
- pathlib (Python 3.4+自带)

## ⚠️ 重要：Python版本兼容性

**MATLAB Engine for Python只支持特定版本的Python：**
- Python 2.7
- Python 3.8
- Python 3.9  
- Python 3.10 (推荐)

**如果您当前使用的是Python 3.11、3.12或更高版本，需要先安装Python 3.10。**

### 快速切换到Python 3.10

我们提供了自动化脚本帮您快速重建虚拟环境：

1. **安装Python 3.10**: https://www.python.org/downloads/release/python-31012/
2. **运行自动化脚本**:
   - Windows命令提示符: 双击 `重建虚拟环境_Python310.bat`
   - PowerShell: 运行 `.\重建虚拟环境_Python310.ps1`

详细步骤请参考：`虚拟环境Python版本修改指南.md`

## 安装步骤

### 1. 安装MATLAB Engine for Python

这是**最重要的步骤**！请严格按照以下步骤操作：

1. **找到MATLAB安装目录**
   ```
   默认路径通常是：
   C:\Program Files\MATLAB\R2023a\extern\engines\python
   ```

2. **打开命令提示符（管理员权限）**

3. **切换到MATLAB Engine目录**
   ```bash
   cd "C:\Program Files\MATLAB\R2023a\extern\engines\python"
   ```

4. **安装MATLAB Engine**
   ```bash
   python setup.py install
   ```

5. **验证安装**
   ```python
   import matlab.engine
   print("MATLAB Engine安装成功!")
   ```

### 2. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 3. 配置PIVlab路径

确保PIVlab已正确安装在指定路径：
```
G:\matlab\piv\PIVlab-2.62
```

## 使用方法

### 1. 配置参数

编辑 `config.py` 文件，设置以下关键参数：

```python
# 路径配置
PIVLAB_PATH = r"G:\matlab\piv\PIVlab-2.62"
INPUT_DIR = r"H:\20250315 mdck 10min 10x stripe\hzx\pos6"
OUTPUT_DIR = r"H:\20250315 mdck 10min 10x stripe\hzx\pos6\result"

# PIV分析参数
PASS1_WINDOW_SIZE = 128
PASS1_STEP_SIZE = 64
PASS2_WINDOW_SIZE = 64
PASS2_STEP_SIZE = 32
```

### 2. 运行分析

```bash
python piv_analyzer.py
```

### 3. 查看结果

分析完成后，结果将保存在指定的输出目录中：
- `frame_0000.txt` - 第一帧的PIV结果
- `frame_0001.txt` - 第二帧的PIV结果
- `...`
- `PIVlab_session.mat` - MATLAB会话文件

## 配置选项详解

### 路径设置

| 参数 | 说明 | 示例 |
|------|------|------|
| `PIVLAB_PATH` | PIVlab安装路径 | `r"G:\matlab\piv\PIVlab-2.62"` |
| `INPUT_DIR` | 输入图像目录 | `r"H:\images\pos6"` |
| `OUTPUT_DIR` | 输出结果目录 | `r"H:\images\pos6\result"` |

### PIV分析参数

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `PASS1_WINDOW_SIZE` | 第一轮窗口大小 | 128 |
| `PASS1_STEP_SIZE` | 第一轮步长 | 64 |
| `PASS2_WINDOW_SIZE` | 第二轮窗口大小 | 64 |
| `PASS2_STEP_SIZE` | 第二轮步长 | 32 |
| `NUM_PASSES` | 总轮数 | 2 |
| `SUBPIXEL_FINDER` | 子像素查找器 | 1 (3点高斯) |

### 预处理参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `ENABLE_CLAHE` | 对比度增强 | True |
| `CLAHE_WINDOW_SIZE` | CLAHE窗口大小 | 50 |
| `ENABLE_HIGHPASS` | 高通滤波 | False |
| `ENABLE_WIENER` | Wiener滤波 | False |

### 导出设置

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `ADD_COLUMN_HEADER` | 添加列标题 | False |
| `ADD_FILE_INFO` | 添加文件信息 | False |
| `EXPORT_FORMAT` | 导出格式 | 'txt' |
| `DELIMITER` | 数据分隔符 | '\t' |

## 输出文件格式

### 文本文件格式
每个结果文件包含四列数据：
```
X坐标    Y坐标    U速度    V速度
123.45   67.89    2.34     -1.56
...
```

### 会话文件
保存所有MATLAB工作空间变量，可以在PIVlab中直接加载。

## 常见问题解决

### 1. MATLAB Engine启动失败

**错误信息**：`matlab.engine.start_matlab()` 失败

**解决方案**：
1. 确保MATLAB已正确安装
2. 检查MATLAB Engine是否正确安装
3. 确保Python版本与MATLAB版本兼容
4. 尝试以管理员权限运行

### 2. PIVlab路径错误

**错误信息**：`PIVlab路径不存在`

**解决方案**：
1. 检查PIVlab是否正确安装
2. 确认`config.py`中的路径设置正确
3. 使用绝对路径，避免相对路径问题

### 3. 图像文件读取失败

**错误信息**：`图像文件数量不足`

**解决方案**：
1. 确认输入目录中有足够的图像文件
2. 检查图像文件格式是否支持（jpg, png, tif等）
3. 确认文件权限设置正确

### 4. 内存不足

**错误信息**：内存相关错误

**解决方案**：
1. 减少图像分辨率
2. 增加PIV窗口大小
3. 处理较少的图像文件
4. 关闭其他占用内存的程序

## 高级使用

### 1. 批量处理多个目录

创建一个脚本循环处理多个目录：

```python
import os
from config import PIVConfig
from piv_analyzer import PIVAnalyzer

directories = [
    r"H:\data\pos1",
    r"H:\data\pos2",
    r"H:\data\pos3"
]

for directory in directories:
    config = PIVConfig()
    config.INPUT_DIR = directory
    config.OUTPUT_DIR = os.path.join(directory, "result")
    
    analyzer = PIVAnalyzer(config)
    analyzer.run_analysis()
```

### 2. 自定义参数优化

根据不同的实验条件调整参数：

```python
# 高分辨率图像
config.PASS1_WINDOW_SIZE = 256
config.PASS1_STEP_SIZE = 128

# 低噪声图像
config.ENABLE_CLAHE = False
config.ENABLE_WIENER = True
```

### 3. 结果后处理

使用pandas和matplotlib进行结果分析：

```python
import pandas as pd
import matplotlib.pyplot as plt

# 读取结果文件
data = pd.read_csv('result/frame_0000.txt', delimiter='\t', 
                   names=['X', 'Y', 'U', 'V'])

# 计算速度大小
data['Speed'] = (data['U']**2 + data['V']**2)**0.5

# 绘制速度场
plt.figure(figsize=(10, 8))
plt.quiver(data['X'], data['Y'], data['U'], data['V'], 
           data['Speed'], cmap='viridis')
plt.colorbar(label='Speed')
plt.title('PIV速度场')
plt.show()
```

## 与手动GUI操作的对比

| 操作 | 手动GUI | 自动化工具 |
|------|---------|------------|
| 图像加载 | 手动点击Load image | 自动扫描目录 |
| 参数设置 | 手动填写GUI界面 | 配置文件设置 |
| 批量分析 | 需要重复点击 | 自动循环处理 |
| 结果导出 | 手动选择导出选项 | 自动导出所有结果 |
| 错误处理 | 界面卡死需要重启 | 自动异常处理 |
| 处理速度 | 慢，需要人工干预 | 快，无人工干预 |

## 许可证

本工具基于PIVlab开源项目，遵循相应的开源许可证。

## 联系方式

如有问题或建议，请联系开发者。

---

**注意事项**：
- 确保MATLAB许可证有效
- 首次运行前请验证所有路径设置
- 建议先用少量图像测试，确认参数设置正确
- 定期备份重要的分析结果 