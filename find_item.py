import time
import os
from core.bot_body import BotBody
from core.bot_eyes import BotEyes
from core.bot_memory import MemoryBank

SCENE_ID = "FloorPlan10"   # must match the scene used in build_map.py
MEMORY_FILE = "memory.json"

def is_opposite(act1, act2):
    """
    check if two actions are opposites
    """
    pairs = {
        ("RotateRight", "RotateLeft"), 
        ("RotateLeft", "RotateRight"),
        ("MoveAhead", "MoveBack")
    }
    return (act1, act2) in pairs

def optimize_path(raw_nodes):
    """
    path optimization to remove redundant actions
    """
    optimized_actions = []
    
    actions = [node['action_to_here'] for node in raw_nodes if node['action_to_here'] != "Start"]
    
    # optimize by removing opposite actions (pair cancellation)
    for action in actions:
        if optimized_actions and is_opposite(optimized_actions[-1], action):
            optimized_actions.pop()
        else:
            optimized_actions.append(action)
                
    return optimized_actions

def run_find():
    print(f'=== 老弟，启动! (场景: {SCENE_ID}) ===')
    
    # 1. load memory bank
    if not os.path.exists(MEMORY_FILE):
        print(f"Error: 找不到记忆文件 {MEMORY_FILE}。")
        return

    memory = MemoryBank(filename=MEMORY_FILE)
    memory.load()
    
    # 2. initialize bot body and eyes
    print("Initializing BotBody and BotEyes...")
    body = BotBody(scene=SCENE_ID, grid_size=0.5)
    eyes = BotEyes(model_name="qwen3-vl:4b")
    
    try:
        # 3. get user input
        print("\n请告诉老弟，你想在这个房间里找什么？")
        print("例如：咖啡机、苹果、微波炉、水龙头...")

        while True:
            target = input(">>> 请输入目标物体: ").strip()
            
            if target.lower() in ['q', 'quit', 'exit', '退出']:
                print("👋 再见！")
                break
            
            if not target:
                print("你没说话，任务取消。")
                continue

            # 4. read memory from JSON and search for the target
            print(f"Searching memory for '{target}'...")
            target_node_id, reasoning = memory.search(target, eyes)
            
            print(f"\n{reasoning}")
            
            if target_node_id == -1:
                print("抱歉，我的记忆里没有关于这个物品的线索。")
                continue

            print(f"\n目标物品【{target}】可能在附近。")
            print("开始规划路径并移动...")
            
            # 5. Action Replay
            # get path to target
            raw_path = memory.history[:target_node_id+1]
            path_to_target = optimize_path(raw_path)

            for i, action in enumerate(path_to_target): 
                success, msg = body.move(action)   
            
                if not success:
                    print(f"Error: 路径执行意外失败: {msg}")
                    break
                    
                time.sleep(0.5) 

            # 6. Final confirmation
            print(f"\n老弟找到了！")
            
            # 拍张照确认
            final_view = body.get_view()
            if final_view:
                final_view.save("assets/found_target.png")
                print("最终视角已保存为 assets/found_target.png")
            
            print("\n任务完成，老弟正在归位...")
            time.sleep(1)
            body.controller.reset(SCENE_ID)
            
    except Exception as e:
        print(f"Error in run_find: {e}")
    finally:
        print("Closing BotBody...")
        body.close()

if __name__ == "__main__":
    run_find()