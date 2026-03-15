from pathlib import Path
import yt_dlp

def download_media(url: str, download_dir: Path) -> Path:
    download_dir.mkdir(parents=True, exist_ok=True)

    outtmpl = str(download_dir / "%(title)s.%(ext)s")

    def hook(d):
        if d["status"] == "downloading":
            percent = d.get("_percent_str", "").strip()
            speed = d.get("_speed_str", "").strip() if d.get("_speed_str") else ""
            eta = d.get("_eta_str", "").strip() if d.get("_eta_str") else ""
            print(f"\rDownloading {percent} | {speed} | ETA {eta}", end="")
        elif d["status"] == "finished":
            print("\nDownloaded...")

    ydl_opts = {
        "outtmpl": outtmpl,
        # "cookiesfrombrowser": ("chrome",),
        "socket_timeout": 20,
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "progress_hooks": [hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        final_path = Path(ydl.prepare_filename(info))

    return final_path