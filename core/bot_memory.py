import json
import os
import re

class MemoryBank:
    """
    bot's memory module.
    in charge of storing exploration paths and performing semantic search using VLM.
    """
    def __init__(self, filename="memory_log.json"):
        self.filename = filename
        self.history = [] # store every node's info as a list of dicts

    def add_event(self, step, description, action, image_path):
        """
        add a new event to memory
        """
        event = {
            "node_id": step,           # node ID
            "description": description, # VLM description of the scene
            "action_to_here": action,   # action taken to reach here
            "image_path": image_path    # screenshot path
        }
        self.history.append(event)
        # save immediately
        self.save()

    def save(self):
        """
        save memory to file
        """
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[BotMemory] Error: {e}")

    def load(self):
        """
        load memory from file
        """
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                print(f"[BotMemory] Success load {len(self.history)} memories.")
            except Exception as e:
                print(f"[BotMemory] Error: {e}")
        else:
            print("[BotMemory] No existing memory file found, starting fresh.")

    def get_memory_str(self):
        """
        get a string summary of the memory for prompt usage
        """
        summary = ""
        for event in self.history:
            summary += f"-[Node {event['node_id']}]: {event['description']}\n"
        return summary

    def search(self, query, bot_eyes):
        """
        Uses the VLM to find the target object in the memory logs.
        """
        if not self.history:
            return -1, "Memory is empty."

        context = self.get_memory_str()
        last_img = self.history[-1]["image_path"] # Use last image as placeholder context
        
        prompt = (
            f"你是一个记忆检索助手。用户想要寻找：【{query}】。\n"
            f"这是你之前的探索记录：\n"
            f"{context}\n"
            "请分析以上记录，告诉我【{query}】最可能出现在哪个节点？\n"
            "请严格按照以下格式回答：\n"
            "分析: [你的分析理由]\n"
            "Result: [节点数字ID]\n"
            "(如果完全没找到相关线索，Result 返回 -1)"
        )
        
        response = bot_eyes.analyse(last_img, prompt)
        
        # Robust Regex Parsing for "Result: X"
        match = re.search(r"Result:\s*(-?\d+)", response, re.IGNORECASE)
        if match:
            return int(match.group(1)), response
        
        return -1, "老弟没找到目标物品。"

# test code 
if __name__ == "__main__":
    mem = MemoryBank()
    mem.add_event(0, "我看到一个冰箱和微波炉", "Start", "assets/step_0.png")
    mem.add_event(1, "我看到水槽和水龙头", "MoveAhead", "assets/step_1.png")
    mem.add_event(2, "我看到一张餐桌和椅子", "RotateRight", "assets/step_2.png")
    
    print(f"当前记忆:\n{mem.get_memory_str()}")
