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
    body = BotBody(scene=SCENE_ID, grid_size=0.5)
    eyes = BotEyes(model_name="qwen3-vl:4b")
    memory = MemoryBank(filename=SAVE_FILE)

    try:
            # initialize step counter
            print("--- 初始全景扫描 ---")
            for _ in range(4):
                body.move("RotateRight")
                process_step(body, eyes, memory, "RotateRight", step_count)
                step_count += 1

            # 主循环：智能探索
            while step_count < MAX_EXPLORE_STEPS:
                print(f"\n--- 探索进度 {step_count + 1}/{MAX_EXPLORE_STEPS} ---")
                
                # 1. 尝试向前走
                success, msg = body.move("MoveAhead")
                
                if success:
                    # 走通了
                    process_step(body, eyes, memory, "MoveAhead", step_count)
                    step_count += 1
                    
                    # 2. 走通后，偶尔左右看看（增加覆盖率）
                    if step_count % 3 == 0: # 每3步看一次
                        look_action = random.choice(["RotateRight", "RotateLeft"])
                        print(f"  > 顺便看看旁边 ({look_action})...")
                        body.move(look_action)
                        process_step(body, eyes, memory, look_action, step_count)
                        step_count += 1
                        
                        # 看完得转回来
                        back_action = "RotateLeft" if look_action == "RotateRight" else "RotateRight"
                        body.move(back_action)
                        # 转回来的动作通常不需要记录为新节点，或者也可以记录
                
                else:
                    # 3. 撞墙了
                    print(f"⚠️ 前方受阻 -> 触发避障转向")
                    turn_action = random.choice(["RotateRight", "RotateLeft"])
                    body.move(turn_action)
                    process_step(body, eyes, memory, turn_action, step_count)
                    step_count += 1
                    
                    # 撞墙后通常需要多转一下确认方向
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