import ollama
import os
from PIL import Image

class BotEyes:
    """
    main class for Visual Language Model (VLM) perception using Ollama service.
    """
    def __init__(self, model_name='qwen3-vl:8b'):
        self.model_name = model_name
        # test connection to Ollama
        try:
            ollama.list()
            print(f"[VLM] initialized with model: {self.model_name}")
        except Exception as e:
            print(f"[VLM] Failed to connect to Ollama service: {e}")

    def analyse(self, image_path: str, prompt: str) -> str:
        """
        Analyzes the scene in the given image using the specified prompt.
        """
        if not os.path.exists(image_path):
            return "Error: Image file not found."

        print(f"[BotEyes] 正在观察并思考...")
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                        'images': [image_path]
                    }
                ]
            )
            result = response['message']['content']
            return result
        except Exception as e:
            return f"Error during VLM inference: {str(e)}"

# module test
if __name__ == "__main__":
    # This is a simple test for the VLMPerceiver class.
    # Make sure you have an image named 'robot_view.png' in the parent directory.
    test_img = "../robot_view.png"  # relative path to the test image
    
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test_body_view.png"))
    
    if os.path.exists(abs_path):
        perceiver = BotEyes()
        description = perceiver.analyse(abs_path, "老弟，简短描述一下你看到的主要物体。")
        print(f"\n[测试结果]:\n{description}")
    else:
        print(f"请先在项目根目录放一张 test_body_view.png 用于测试模块功能。")