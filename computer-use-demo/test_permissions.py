import pyautogui

def test_permissions():
    try:
        # Get current mouse position as a basic test
        x, y = pyautogui.position()
        print(f"Mouse position: ({x}, {y})")
        
        # Try a basic keyboard command
        pyautogui.press('a')
        print("Keyboard test successful")
        
    except pyautogui.FailSafeException:
        print("FailSafe triggered - mouse moved to corner")
    except Exception as e:
        print(f"Error: {e}")
        print("You may need to grant accessibility permissions")
        print("Go to System Settings > Privacy & Security > Accessibility")

if __name__ == "__main__":
    test_permissions()