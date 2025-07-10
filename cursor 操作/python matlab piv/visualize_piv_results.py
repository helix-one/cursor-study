#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PIV结果可视化工具
将PIV分析结果的txt文件转换为向量场图片
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path
import glob

class PIVVisualizer:
    def __init__(self, result_dir):
        """
        初始化PIV可视化工具
        
        Args:
            result_dir: PIV结果文件所在目录
        """
        self.result_dir = Path(result_dir)
        
        # 设置matplotlib参数
        plt.rcParams['font.size'] = 12
        plt.rcParams['axes.labelsize'] = 14
        plt.rcParams['axes.titlesize'] = 16
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        
    def read_piv_data(self, txt_file):
        """
        读取PIV结果txt文件
        
        Args:
            txt_file: txt文件路径
            
        Returns:
            x, y, u, v: numpy数组，分别为x坐标、y坐标、u分量、v分量
        """
        try:
            # 读取数据，假设数据格式为：x y u v（制表符或空格分隔）
            data = np.loadtxt(txt_file)
            
            if data.shape[1] != 4:
                print(f"警告: {txt_file} 数据格式不正确，应该包含4列 (x, y, u, v)")
                return None, None, None, None
                
            x = data[:, 0]
            y = data[:, 1] 
            u = data[:, 2]
            v = data[:, 3]
            
            # 移除无效数据（NaN或无穷大）
            valid_mask = np.isfinite(x) & np.isfinite(y) & np.isfinite(u) & np.isfinite(v)
            
            return x[valid_mask], y[valid_mask], u[valid_mask], v[valid_mask]
            
        except Exception as e:
            print(f"读取文件 {txt_file} 失败: {e}")
            return None, None, None, None
    
    def create_vector_plot(self, x, y, u, v, title="PIV Vector Field", 
                          arrow_width=0.003, colormap='viridis', show_magnitude=True):
        """
        创建向量场图
        
        Args:
            x, y, u, v: 坐标和向量分量
            title: 图标题
            arrow_width: 箭头宽度
            colormap: 颜色映射
            show_magnitude: 是否显示速度大小颜色映射
            
        Returns:
            fig, ax: matplotlib图形对象
        """
        # 创建图形
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # 计算速度大小
        magnitude = np.sqrt(u**2 + v**2)
        
        # 固定缩放规则：速度大小100对应60像素箭头长度
        # 因此比例系数 = 100/60 = 1.667
        # scale参数表示：data units per arrow length unit
        scale_factor = 0.2 # 1.667
        
        print(f"使用固定缩放: 速度100 = 60像素箭头")
        if len(magnitude) > 0:
            print(f"当前最大速度: {np.max(magnitude):.2f} = {np.max(magnitude)/scale_factor:.1f}像素箭头")
        
        if show_magnitude and len(magnitude) > 0:
            # 使用颜色表示速度大小
            quiver = ax.quiver(x, y, u, v, magnitude, 
                             scale=scale_factor, 
                             scale_units='xy',
                             angles='xy',
                             width=arrow_width,
                             cmap=colormap,
                             alpha=0.8)
            
            # 添加颜色条
            cbar = plt.colorbar(quiver, ax=ax, shrink=0.8)
            cbar.set_label('Speed Magnitude (pixels/frame)', rotation=270, labelpad=20)
        else:
            # 使用单一颜色
            quiver = ax.quiver(x, y, u, v, 
                             scale=scale_factor, 
                             scale_units='xy',
                             angles='xy',
                             width=arrow_width,
                             color='blue',
                             alpha=0.7)
        
        # 设置坐标轴
        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        ax.set_title(title)
        
        # 设置坐标轴相等比例
        ax.set_aspect('equal')
        
        # 反转y轴（图像坐标系，y轴向下）
        ax.invert_yaxis()
        
        # 添加网格
        ax.grid(True, alpha=0.3)
        
        # 设置坐标轴范围
        if len(x) > 0:
            margin_x = (np.max(x) - np.min(x)) * 0.1
            margin_y = (np.max(y) - np.min(y)) * 0.1
            ax.set_xlim(np.min(x) - margin_x, np.max(x) + margin_x)
            ax.set_ylim(np.max(y) + margin_y, np.min(y) - margin_y)
        
        # 添加统计信息和缩放说明
        if len(magnitude) > 0:
            stats_text = f'Vectors: {len(x)}\n'
            stats_text += f'Avg Speed: {np.mean(magnitude):.1f}\n'
            stats_text += f'Max Speed: {np.max(magnitude):.1f}\n'
            stats_text += f'Min Speed: {np.min(magnitude):.1f}\n'
            stats_text += f'Scale: Speed 100 = 60px arrow'
            
            # 添加文本框
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
            ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
                   verticalalignment='top', bbox=props, fontsize=10)
        
        plt.tight_layout()
        return fig, ax
    
    def process_single_file(self, txt_file, output_dir=None, 
                           dpi=300, format='png'):
        """
        处理单个txt文件并生成图片
        
        Args:
            txt_file: 输入txt文件路径
            output_dir: 输出目录（默认为txt文件所在目录）
            dpi: 图片分辨率
            format: 图片格式
        """
        txt_path = Path(txt_file)
        
        if output_dir is None:
            output_dir = txt_path.parent
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # 读取数据
        print(f"正在处理: {txt_path.name}")
        x, y, u, v = self.read_piv_data(txt_file)
        
        if x is None:
            print(f"跳过文件: {txt_path.name}")
            return False
        
        print(f"  读取到 {len(x)} 个向量点")
        print(f"  位置范围: X=[{np.min(x):.1f}, {np.max(x):.1f}], Y=[{np.min(y):.1f}, {np.max(y):.1f}]")
        print(f"  速度范围: U=[{np.min(u):.1f}, {np.max(u):.1f}], V=[{np.min(v):.1f}, {np.max(v):.1f}]")
        
        # 创建图形
        title = f"PIV Vector Field - {txt_path.stem}"
        fig, ax = self.create_vector_plot(x, y, u, v, title=title)
        
        # 保存图片
        output_file = output_dir / f"{txt_path.stem}_vectors.{format}"
        fig.savefig(output_file, dpi=dpi, bbox_inches='tight')
        plt.close(fig)  # 关闭图形以释放内存
        
        print(f"已保存: {output_file}")
        return True
    
    def process_all_files(self, pattern="frame_*.txt", dpi=300, format='png'):
        """
        处理目录中的所有txt文件
        
        Args:
            pattern: 文件名模式
            dpi: 图片分辨率
            format: 图片格式
        """
        # 查找所有匹配的txt文件
        txt_files = list(self.result_dir.glob(pattern))
        
        if not txt_files:
            print(f"在目录 {self.result_dir} 中没有找到匹配 '{pattern}' 的文件")
            return
        
        print(f"找到 {len(txt_files)} 个txt文件")
        print("=" * 50)
        
        success_count = 0
        for txt_file in sorted(txt_files):
            try:
                if self.process_single_file(txt_file, dpi=dpi, format=format):
                    success_count += 1
                print()  # 添加空行分隔
            except Exception as e:
                print(f"处理文件 {txt_file.name} 时出错: {e}")
        
        print("=" * 50)
        print(f"处理完成! 成功生成 {success_count} 张图片")
    
    def create_animation(self, pattern="frame_*.txt", output_name="piv_animation.gif", 
                        duration=500):
        """
        创建PIV结果的动画
        
        Args:
            pattern: 文件名模式
            output_name: 输出动画文件名
            duration: 每帧持续时间（毫秒）
        """
        try:
            from PIL import Image
            import tempfile
            
            # 创建临时目录
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # 查找所有txt文件
                txt_files = sorted(list(self.result_dir.glob(pattern)))
                
                if not txt_files:
                    print(f"没有找到匹配 '{pattern}' 的文件")
                    return
                
                print(f"正在创建动画，包含 {len(txt_files)} 帧...")
                
                # 生成临时图片
                temp_images = []
                for i, txt_file in enumerate(txt_files):
                    x, y, u, v = self.read_piv_data(txt_file)
                    if x is not None:
                        title = f"PIV Vector Field - Frame {i:04d}"
                        fig, ax = self.create_vector_plot(x, y, u, v, title=title)
                        
                        temp_img = temp_path / f"frame_{i:04d}.png"
                        fig.savefig(temp_img, dpi=150, bbox_inches='tight')
                        plt.close(fig)
                        temp_images.append(temp_img)
                
                # 创建动画
                if temp_images:
                    images = [Image.open(img) for img in temp_images]
                    output_path = self.result_dir / output_name
                    images[0].save(output_path, save_all=True, append_images=images[1:], 
                                 duration=duration, loop=0)
                    print(f"动画已保存: {output_path}")
                
        except ImportError:
            print("需要安装PIL库才能创建动画: pip install Pillow")
        except Exception as e:
            print(f"创建动画时出错: {e}")

def main():
    """主函数"""
    # 设置PIV结果目录
    result_dir = r"H:\20250315 mdck 10min 10x stripe\hzx\pos6\result"
    
    # 创建可视化工具
    visualizer = PIVVisualizer(result_dir)
    
    print("PIV结果可视化工具")
    print("=" * 50)
    print(f"处理目录: {result_dir}")
    print("缩放规则: 速度100 = 60像素箭头长度")
    
    # 处理所有frame_*.txt文件
    visualizer.process_all_files(
        pattern="piv_result_*.txt",
        dpi=300,            # 图片分辨率
        format='png'        # 图片格式
    )
    
    # 可选：创建动画
    print("\n正在创建动画...")
    visualizer.create_animation(
        pattern="piv_result_*.txt",
        output_name="piv_animation.gif",
        duration=500  # 每帧500毫秒
    )
    
    print("\n可视化完成!")

if __name__ == "__main__":
    main() 