from datetime import datetime
from pathlib import Path
import whisper
from faster_whisper import WhisperModel
from tqdm import tqdm
import os


from src.downloader import download_media
from src.llm import deepseek_punctuate


def chunk_segments(segments, chunk_size=5):
    chunks = []
    for i in range(0, len(segments), chunk_size):
        chunk = segments[i:i + chunk_size]
        text = "\n".join(seg["text"].strip() for seg in chunk if seg["text"].strip())
        if text:
            chunks.append(text)
    return chunks

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent
download_dir = BASE_DIR / "downloads"

print("Please enter the video url: ")
url = input()
audio_path = download_media(url, download_dir)
print(f"Downloaded: {audio_path}")

output_dir = BASE_DIR / "output"
output_dir.mkdir(exist_ok=True)

# 输出文件
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = output_dir / f"{audio_path.stem}_{timestamp}.txt"

if not audio_path.exists():
    raise FileNotFoundError(f"音频文件不存在: {audio_path}")

print(f"正在识别: {audio_path}")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

segments, info = model.transcribe(
    str(audio_path),
    language="zh",
    vad_filter=True
)

segment_list = []
for segment in segments:
    segment_list.append({
        "start": segment.start,
        "end": segment.end,
        "text": segment.text
    })

chunks = chunk_segments(segment_list, chunk_size=5)

processed_chunks = []
for chunk in tqdm(chunks, desc="DeepSeek 后处理"):
    new_text = deepseek_punctuate(chunk)
    processed_chunks.append(new_text)

final_text = "\n".join(processed_chunks)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(final_text)

KEEP_DOWNLOAD = False
if not KEEP_DOWNLOAD and os.path.exists(audio_path):
    os.remove(audio_path)

print(f"已写入: {output_file}")
