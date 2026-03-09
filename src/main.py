from pathlib import Path
import whisper

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 输入音频
audio_path = BASE_DIR / "samples" / "test.mp3"

# 输出目录
output_dir = BASE_DIR / "output"
output_dir.mkdir(exist_ok=True)

# 输出文件
output_file = output_dir / "result.txt"

if not audio_path.exists():
    raise FileNotFoundError(f"音频文件不存在: {audio_path}")

print(f"正在识别: {audio_path}")

model = whisper.load_model("small")

result = model.transcribe(str(audio_path), language="zh")

# 写入文件
with open(output_file, "w", encoding="utf-8") as f:
    f.write(result["text"])

print("识别完成")
print("文本：", result["text"])
print("已写入:", output_file)