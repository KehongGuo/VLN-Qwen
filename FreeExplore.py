import os
import time
import re
from core.bot_body import BotBody
from core.bot_eyes import BotEyes

# -- configurations --
MAX_STEPS = 10    # max steps for the agent to find the target

def parse_action(response_text):
    """
    From the model's response text, extract the intended action.
    Simple parsing logic based on keywords.
    """
    # The initial set of valid actions
    valid_actions = ["MoveAhead", "RotateRight", "RotateLeft", "Stop"]
    
    # 1. Try to find explicit Action tags in the response
    # example: "Action: MoveAhead"
    for action in valid_actions:
        if f"Action: {action}" in response_text:
            return action
            
# ----- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  -----
# 这里想优化一下，做更智能的解析
    # 2. Fallback: look for keywords in the text
    if "MoveAhead" in response_text: return "MoveAhead"
    if "RotateRight" in response_text: return "RotateRight"
    if "RotateLeft" in response_text: return "RotateLeft"
    if "Stop" in response_text: return "Stop"
    
    return "Stop" # default to Stop if unsure

def explore():
    print("=== 老弟，启动! ===")
    
    print("\n请告诉老弟，你想在这个房间里找什么？")
    print("例如：咖啡机、苹果、微波炉、水龙头...")
    target_object = input(">>> 请输入目标物体: ").strip()

    task_prompt = f"你的任务是在这个房间里找到【{target_object}】。请仔细观察周围。"

    # 1. create assets directory
    if not os.path.exists("assets"):
        os.mkdir("assets")

    # 2. 初始化模块
    eyes = BotEyes(model_name="qwen3-vl:4b")
    body = BotBody(scene="FloorPlan10") # This is a sample scene with a kitchen
    
    print(f"\n>>> 老弟的任务是: {task_prompt}")
    
    try:
        for step in range(MAX_STEPS):
            print(f"\n--- Step {step + 1}/{MAX_STEPS} ---")
            
            # [BotBody] get current view
            current_view = body.get_view()
            
            # save current view
            step_img_path = f"assets/step_{step}.png"
            current_view.save(step_img_path)
            print(f"[Main] 截图已保存: {step_img_path}")
            
            # [Thinking] system prompt
            prompt = (
                f"{task_prompt}\n"
                "请务必按照以下格式进行输出，不要跳过任何步骤：\n\n"
                "1. 观察\n"
                "列出你在图片中看到的主要物体和家具。\n\n"
                "2. 思考\n"
                f"分析目标【{target_object}】可能在哪里？\n\n"
                "3. 决策\n"
                "只能从以下动作中选一个: MoveAhead, RotateRight, RotateLeft, Stop\n"
                "Action: [在这里填入你的动作]"
            )
            
            # Call VLM to analyse the image (laodi's eyes)
            thought_process = eyes.analyse(step_img_path, prompt)
            print(f"\n [BotEyes]:\n{thought_process}\n")
            
            # [Main] analyze the response and decide action
            action = parse_action(thought_process)
            print(f"[Main]: {action}")
            
            if action == "Stop":
                print("老弟决定停止任务（可能已找到目标）。")
                break
            
            success, msg = body.move(action)
            if not success:
                print(f"动作执行失败: {msg}")
                # simple obstacle avoidance: try to turn right if move ahead fails
                print("触发避障机制: 老弟强制右转")
                body.move("RotateRight")
                
            # stop for a moment to simulate thinking time
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n 强制终止。")
    finally:
        body.close()
        print("老弟的任务已经结束，又是忙碌的一天！")

if __name__ == "__main__":
    explore()