import time
import sys

from build_map import run_scan
from find_item import run_find

def main():
    print("VLN-Qwen-老弟启动 ")
    
    try:
        # Stage 1: Build Memory
        print("\n>>> 正在启动 Phase 1: 构建环境记忆...")
        run_scan()
        print("Phase 1 完成。记忆库已生成。")
        
        
        # --- 第二阶段：找物 ---
        print(">>> 正在启动 Phase 2: 物品搜寻...")
        run_find()
        print("Phase 2 完成。")
        
    except KeyboardInterrupt:
        print("\nError：任务被用户强制中断。")
    except Exception as e:
        print(f"\nError：系统发生错误: {e}")
    finally:
        print("\n演示结束，谢谢大哥使用老弟！")

if __name__ == "__main__":
    main()