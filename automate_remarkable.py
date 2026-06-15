import os
import time
from datetime import datetime
from pathlib import Path

import pyautogui
import pygetwindow as gw
import pyperclip

time.sleep(3)

pyautogui.hotkey('win')
time.sleep(0.5)

pyautogui.write("remarkable")
time.sleep(0.5)

pyautogui.press('enter')
time.sleep(15)

try:
    remarkable_window = gw.getWindowsWithTitle("Remarkable")[0]
    center_x = remarkable_window.left + (remarkable_window.width // 2)
    center_y = remarkable_window.top + (remarkable_window.height // 2)
    pyautogui.click(center_x, center_y)
    print(f"Clicked center of Remarkable window: ({center_x}, {center_y})")
except IndexError:
    print("Remarkable window not found. Clicking screen center instead.")
    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width // 2, screen_height // 2)

pyautogui.hotkey('ctrl', 'f')
time.sleep(0.5)

pyautogui.write("exploit")
time.sleep(0.5)

pyautogui.press('down')
time.sleep(0.3)

pyautogui.press('enter')
time.sleep(0.3)

pyautogui.hotkey('ctrl', 'enter')
time.sleep(0.3)

pyautogui.hotkey('ctrl', 'enter')
time.sleep(0.3)

pyautogui.hotkey('ctrl', 'a')
time.sleep(0.3)

pyautogui.hotkey('ctrl', 'c')
time.sleep(0.5)

pyautogui.hotkey('alt', 'f4')
time.sleep(1)

copied_text = pyperclip.paste()

output_dir = r"C:\Users\spatt\Desktop\RemarkableExploit\processed"
os.makedirs(output_dir, exist_ok=True)

today_date = datetime.now().strftime("%Y%m%d")
nums = [int(p.stem.rsplit("_", 1)[-1]) for p in Path(output_dir).glob(f"file_{today_date}_*.md")]
next_n = max(nums, default=0) + 1

filename = f"file_{today_date}_{next_n}.md"
filepath = os.path.join(output_dir, filename)

timestamp = datetime.now().strftime("%Y-%m-%d")
content = f"# Exploit - {timestamp}\n\n{copied_text}"

with open(filepath, "w", encoding="utf-8") as file:
    file.write(content)

print(f"Saved to: {filepath}")
print("Done.")
