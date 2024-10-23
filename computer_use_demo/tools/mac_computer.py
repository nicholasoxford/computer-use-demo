from datetime import time
from .base import BaseAnthropicTool, ComputerToolOptions, ToolError, ToolResult
import pyautogui
import base64
from io import BytesIO
from pathlib import Path
import os
from typing import Dict, Any, List

class MacComputerTool(BaseAnthropicTool):
    name = "computer"
    api_type = "computer_20241022"
    
    def __init__(self):
        super().__init__()
        # Get screen size
        self.width, self.height = pyautogui.size()
        #print screen size
        print(f"Screen size: {self.width}x{self.height}")
        self._screenshot_delay = 2.0
        self._scaling_enabled = True
        
    @property
    def options(self) -> ComputerToolOptions:
        return {
            "display_width_px": self.width,
            "display_height_px": self.height,
            "display_number": None
        }

    async def __call__(self, *, action: str, text: str | None = None, 
                       coordinate: tuple[int, int] | None = None, 
                       modifiers: List[str] | None = None, **kwargs):
        print(f"Action: {action}, Text: {text}, Coordinate: {coordinate}, Modifiers: {modifiers}")
        if action in ("mouse_move", "left_click_drag"):
            if coordinate is None:
                raise ToolError(f"coordinate is required for {action}")
            x, y = coordinate
            
            if action == "mouse_move":
                pyautogui.moveTo(x, y, duration=0.5)
                return ToolResult(output=f"Mouse moved to {x}, {y}")
            elif action == "left_click_drag":
                pyautogui.mouseDown()
                pyautogui.moveTo(x, y, duration=0.5)
                pyautogui.mouseUp()
                return ToolResult(output=f"Mouse dragged to {x}, {y}")

        if action in ("key", "type"):
            if text is None:
                raise ToolError(f"text is required for {action}")
            
            if action == "key":
                # if text includes command, shift, or option, add the appropriate modifier, and split the text by -
                if "command" in text:
                    text = text.split("+")[1]
                    pyautogui.hotkey("command", text)
                elif "shift" in text:
                    text = text.split("+")[1]
                    pyautogui.hotkey("shift", text)
                elif "option" in text:
                    text = text.split("+")[1]
                    pyautogui.hotkey("option", text)
                elif "super" in text.lower():  # Make case-insensitive
                    textCommand = text.split("+")[1].lower().strip()
                    pyautogui.keyDown("command")
                    pyautogui.keyDown(textCommand)
                    pyautogui.keyUp("command")
                    pyautogui.keyUp(textCommand)
                else:
                    pyautogui.press(text)
                return ToolResult(output=f"Pressed key: {text}")
            elif action == "type":
                pyautogui.write(text, interval=0.01)
                return ToolResult(output=f"Typed text: {text}")

        if action in ("left_click", "right_click", "double_click", "middle_click", 
                     "screenshot", "cursor_position"):
            if action == "screenshot":
                return await self.screenshot()
            elif action == "cursor_position":
                x, y = pyautogui.position()
                return ToolResult(output=f"X={x},Y={y}")
            else:
                click_map = {
                    "left_click": pyautogui.click,
                    "right_click": pyautogui.rightClick,
                    "middle_click": pyautogui.middleClick,
                    "double_click": lambda: pyautogui.click(clicks=2)
                }
                click_map[action]()
                return ToolResult(output=f"Performed {action}")

        raise ToolError(f"Invalid action: {action}")

    async def screenshot(self):
        """Take a screenshot and return it as base64."""
        output_dir = Path(os.getenv("OUTPUT_DIR", "/tmp/outputs"))
        output_dir.mkdir(parents=True, exist_ok=True)
        
        screenshot = pyautogui.screenshot()
        img_buffer = BytesIO()
        screenshot.save(img_buffer, format='PNG')
        base64_image = base64.b64encode(img_buffer.getvalue()).decode()
        
        return ToolResult(base64_image=base64_image)
    
    

