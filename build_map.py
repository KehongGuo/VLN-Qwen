import os
import time
import random
from core.bot_body import BotBody
from core.bot_eyes import BotEyes
from core.bot_memory import MemoryBank

SCENE_ID = "FloorPlan10"  # ai2-thor scene ID
SAVE_FILE = "memory.json" # final output - the environment database (simillar to a topological map)

MAX_EXPLORE_STEPS = 12

def process_step(body, eyes, memory, action, step_idx):
    """
    process a single exploration step
    """
    # 1. capture view
    current_view = body.get_view()
    img_name = f"scan_{step_idx}.png"
    img_path = os.path.join("assets", img_name)
    current_view.save(img_path)
    
    # 2.Qwen captures semantics
    prompt = (
        "请简短、精确地列出你在这张图片中看到的所有家具、家电和物品。"
        "不要说废话，直接列出物体名称（例如：冰箱、微波炉、苹果、水槽）。"
        "这对于构建环境数据库非常重要。"
    )
    # call bot_eyes to analyse
    description = eyes.analyse(img_path, prompt)
    
    # 3. store into memory
    memory.add_event(
        step=step_idx,
        description=description,
        action=action,
        image_path=img_path
    )

def run_scan():
    print(f"[{SCENE_ID}]:场景初始化中....")
    
    if not os.path.exists("assets"):
        os.mkdir("assets")
        
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print("  > deleted existing memory file.")

    # initial bot components
    body = BotBody(scene=SCENE_ID, grid_size=1.0)
    eyes = BotEyes(model_name="qwen3-vl:4b")
    memory = MemoryBank(filename=SAVE_FILE)

    try:
            # initialize step counter
            for _ in range(4):
                body.move("RotateRight")
                process_step(body, eyes, memory, "RotateRight", step_count)
                step_count += 1

            # loop body: explore until max steps
            while step_count < MAX_EXPLORE_STEPS:
                
                # 1. try move forward
                success, msg = body.move("MoveAhead")
                
                if success:
                    process_step(body, eyes, memory, "MoveAhead", step_count)
                    step_count += 1
                    
                    # 2. if is successful, randomly look around
                    if step_count % 3 == 0: # every 3 steps
                        look_action = random.choice(["RotateRight", "RotateLeft"])
                        body.move(look_action)
                        process_step(body, eyes, memory, look_action, step_count)
                        step_count += 1
                        
                        # back to original direction
                        back_action = "RotateLeft" if look_action == "RotateRight" else "RotateRight"
                        body.move(back_action)
                
                else:
                    # 3. if hit the wall
                    turn_action = random.choice(["RotateRight", "RotateLeft"])
                    body.move(turn_action)
                    process_step(body, eyes, memory, turn_action, step_count)
                    step_count += 1
                    
                    # simple anti-stuck: turn again
                    body.move(turn_action)
                    process_step(body, eyes, memory, turn_action, step_count)
                    step_count += 1

                time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n 扫描中断。")
    finally:
        body.close()
        memory.save()
        # scan complete

if __name__ == "__main__":
    run_scan()