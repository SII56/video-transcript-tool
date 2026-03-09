from datetime import datetime
from pathlib import Path
import whisper

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent
audio_path = BASE_DIR / "samples" / "a.aac"

# 输出目录
output_dir = BASE_DIR / "output"
output_dir.mkdir(exist_ok=True)

# 输出文件
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = output_dir / f"{audio_path.stem}_{timestamp}.txt"

if not audio_path.exists():
    raise FileNotFoundError(f"音频文件不存在: {audio_path}")

print(f"正在识别: {audio_path}")

model = whisper.load_model("small")
result = model.transcribe(str(audio_path), language="zh")

# 写入文件
with open(output_file, "w", encoding="utf-8") as f:
    for segment in result["segments"]:
        text = segment["text"].strip()
        if text:
            f.write(text + "\n")

print("输出文件:", output_file)