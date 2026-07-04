import tkinter as tk
import ctypes

def set_clickthrough(hwnd):
    """
    调用 Windows API 让窗口实现鼠标穿透
    """
    WS_EX_TRANSPARENT = 0x00000020
    WS_EX_LAYERED = 0x00080000
    GWL_EXSTYLE = -20
    
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED | WS_EX_TRANSPARENT)

class CrosshairApp:
    def __init__(self, root):
        self.root = root
        # --- 1. 设置控制面板 (主窗口) ---
        self.root.title("FPS 准星大师")
        self.root.geometry("300x180")
        self.root.attributes('-topmost', True) # 控制面板也稍微置顶一下，方便操作
        
        # 默认准星属性
        self.window_size = 40
        self.crosshair_color = "red"
        
        # --- 2. 创建准星图层 (子窗口) ---
        self.overlay = tk.Toplevel(self.root)
        self.setup_overlay()
        
        # --- 3. 绘制控制面板 UI ---
        self.setup_control_panel()

    def setup_overlay(self):
        """配置透明的准星图层"""
        screen_width = self.overlay.winfo_screenwidth()
        screen_height = self.overlay.winfo_screenheight()
        
        x = int((screen_width / 2) - (self.window_size / 2))
        y = int((screen_height / 2) - (self.window_size / 2))
        
        self.overlay.geometry(f'{self.window_size}x{self.window_size}+{x}+{y}')
        self.overlay.overrideredirect(True)      # 无边框
        self.overlay.wm_attributes("-topmost", True)  # 始终置顶
        self.overlay.wm_attributes("-transparentcolor", "black") # 黑色背景设为透明
        
        self.overlay.update_idletasks()
        
        # 设置鼠标穿透
        hwnd = ctypes.windll.user32.GetParent(self.overlay.winfo_id())
        set_clickthrough(hwnd)
        
        # 创建画布并绘制准星
        self.canvas = tk.Canvas(self.overlay, width=self.window_size, height=self.window_size, bg='black', highlightthickness=0)
        self.canvas.pack()
        self.draw_crosshair()

    def draw_crosshair(self):
        """在画布上绘制十字"""
        self.canvas.delete("all") # 清空画布
        center = self.window_size / 2
        length = 10
        width = 2
        
        # 画十字
        self.canvas.create_line(center, center - length, center, center + length, fill=self.crosshair_color, width=width)
        self.canvas.create_line(center - length, center, center + length, center, fill=self.crosshair_color, width=width)

    def setup_control_panel(self):
        """配置控制面板界面的按钮和标签"""
        # 标题
        tk.Label(self.root, text="请选择准星颜色:", font=("Microsoft YaHei", 12)).pack(pady=10)
        
        # 颜色按钮区域
        color_frame = tk.Frame(self.root)
        color_frame.pack(pady=5)
        
        # 定义几种常见的亮色
        colors = ["red", "green", "cyan", "yellow", "white", "magenta"]
        for c in colors:
            # 使用 lambda 函数传递特定的颜色给改变颜色的方法
            btn = tk.Button(color_frame, bg=c, width=3, relief="groove", command=lambda col=c: self.change_color(col))
            btn.pack(side=tk.LEFT, padx=3)
            
        # 退出按钮
        exit_btn = tk.Button(self.root, text="退出程序", bg="#ff4d4d", fg="white", font=("Microsoft YaHei", 10, "bold"), command=self.exit_app)
        exit_btn.pack(pady=20)

    def change_color(self, new_color):
        """更改颜色并重新绘制"""
        self.crosshair_color = new_color
        self.draw_crosshair()

    def exit_app(self):
        """安全关闭所有窗口"""
        self.root.quit()
        self.root.destroy()

if __name__ == '__main__':
    # 实例化主循环
    root = tk.Tk()
    app = CrosshairApp(root)
    root.mainloop()
