from ai2thor.controller import Controller
from PIL import Image
import time

class BotBody:
    """
    The main class for robot body control in AI2-THOR environment.
    which handles movement and interaction within the scene.
    """
    def __init__(self, scene="FloorPlan10", grid_size=0.5):
        print(f"[BotBody] is initializing...")
        print(f"[BotBody] Loading scene: {scene}")
        
        # Initialize AI2-THOR Controller    
        self.controller = Controller(
            agentMode="default",
            visibilityDistance=1.5,
            scene=scene,
            gridSize=grid_size,
            renderDepthImage=False,     # RGB firtst, no need for depth
            renderInstanceSegmentation=False,
            renderObjectImage=False,
            width=600,                  
            height=600
        )
        print("[BotBody] Controller initialized.")

    def move(self, action: str):
        """
        implement robot movement action
        Move list: "MoveAhead", "RotateRight", "RotateLeft", "LookUp", "LookDown"
        Return: (success: bool, message: str)
        """
        print(f"[BotBody] 执行动作 -> {action}")
        
        if action == "Stop":
            return True, "Robot stopped."

        try:
            event = self.controller.step(action=action)
            
            success = event.metadata["lastActionSuccess"]
            error_msg = event.metadata["errorMessage"]
            
            if success:
                return True, "Action successful."
            else:
                return False, f"Action failed: {error_msg}"
                
        except Exception as e:
            return False, f"System Error: {str(e)}"

    def get_view(self):
        """
        Capture the current view from the robot's perspective.
        Return: PIL Image object of the current view.
        """
        event = self.controller.last_event
        if event and event.frame is not None:
            return Image.fromarray(event.frame)
        return None

    def close(self):
        self.controller.stop()
        print("[BotBody] 系统关闭。")

# module test
if __name__ == "__main__":
    # Try can bu can walk two step
    body = BotBody()
    
    # Try get initial view
    img = body.get_view()
    if img:
        img.save("test_body_view.png")
        print("Test: bot view image saved as test_body_view.png")
        
    # step one move ahead
    success, msg = body.move("MoveAhead")
    if success:
        print("test: Success")
    else:
        print(f"Test: no good ({msg})")

    body.close()