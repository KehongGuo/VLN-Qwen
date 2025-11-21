import os
import time
from core.bot_body import BotBody
from core.bot_eyes import BotEyes
from core.bot_memory import MemoryBank

SCENE_ID = "FloorPlan10"  # ai2-thor scene ID
SAVE_FILE = "memory.json" # final output - the environment database (simillar to a topological map)


EXPLORATION_ROUTINE = [
    "Start",       
    "RotateRight", 
    "RotateRight", 
    "RotateRight",  
    "RotateRight",
    "MoveAhead",   
    "RotateRight", 
    "MoveAhead",   
    "RotateLeft",  
    "RotateLeft",  
]

def run_scan():
    print(f"[{SCENE_ID}]:场景初始化中....")
    
    if not os.path.exists("assets"):
        os.mkdir("assets")
        
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print("  > deleted existing memory file.")

    # initial bot components
    body = BotBody(scene=SCENE_ID, grid_size=0.5)
    eyes = BotEyes(model_name="qwen3-vl:4b")
    memory = MemoryBank(filename=SAVE_FILE)

    try:
        for step_idx, action in enumerate(EXPLORATION_ROUTINE):
            print(f"--- 扫描进度 {step_idx+1}/{len(EXPLORATION_ROUTINE)} ---")
            
            # (A) if not starting, move
            if action != "Start":
                success, msg = body.move(action)
                if not success:
                    continue
            
            # (B) capture view
            current_view = body.get_view()
            img_name = f"scan_{step_idx}.png"
            img_path = os.path.join("assets", img_name)
            current_view.save(img_path)
            
            # (C) Qwen captures semantics
            prompt = (
                "请简短、精确地列出你在这张图片中看到的所有家具、家电和物品。"
                "不要说废话，直接列出物体名称（例如：冰箱、微波炉、苹果、水槽）。"
                "这对于构建环境数据库非常重要。"
            )
            
            # call bot_eyes to analyse
            description = eyes.analyse(img_path, prompt)
            
            # (D) store into memory
            memory.add_event(
                step=step_idx,
                description=description,
                action=action,
                image_path=img_path
            )
            
            time.sleep(1) 

    except KeyboardInterrupt:
        print("\n 扫描中断。")
    finally:
        body.close()
        memory.save()
        # scan complete

if __name__ == "__main__":
    run_scan()