import subprocess
import sys
import os
from pathlib import Path

# ====================== 自动安装 yt-dlp ======================
def ensure_yt_dlp():
    try:
        import yt_dlp
        return yt_dlp
    except ImportError:
        print("🔧 yt-dlp 未安装，正在自动安装（只需一次）...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp", "--quiet"])
            print("✅ yt-dlp 安装成功！")
            import yt_dlp
            return yt_dlp
        except Exception as e:
            print(f"❌ 自动安装失败：{e}")
            print("请手动运行：pip install yt-dlp")
            sys.exit(1)

yt_dlp = ensure_yt_dlp()

# ====================== 下载函数 ======================
def download(url, is_audio=False, output_dir=None):
    if output_dir is None:
        output_dir = str(Path.home() / "Downloads" / "YouTube_Downloads")
    os.makedirs(output_dir, exist_ok=True)

    if is_audio:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,
            'progress_hooks': [lambda d: print(f"📥 下载进度: {d.get('status')} - {d.get('_percent_str', '0%')}") if d['status'] == 'downloading' else None],
        }
    else:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'quiet': False,
            'progress_hooks': [lambda d: print(f"📥 下载进度: {d.get('status')} - {d.get('_percent_str', '0%')}") if d['status'] == 'downloading' else None],
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"🚀 开始下载: {url}")
        ydl.download([url])
        print("✅ 下载完成！")

# ====================== 主程序 ======================
if __name__ == "__main__":
    print("="*60)
    print("🎥 YouTube 视频下载器（2026 稳定版）")
    print("仅供个人学习使用，请尊重版权和 YouTube 服务条款！")
    print("="*60)

    url = input("\n📌 请输入 YouTube 视频或播放列表链接：").strip()
    if not url.startswith("http"):
        print("❌ 链接格式错误！")
        sys.exit(1)

    print("\n选择下载类型：")
    print("1. 视频 + 音频（最高画质 MP4）")
    print("2. 仅音频（MP3，高音质）")
    choice = input("输入 1 或 2（默认1）：").strip()

    is_audio = choice == "2"

    custom_path = input("\n保存路径（直接回车 = 默认 Downloads/YouTube_Downloads）：").strip()
    output_dir = custom_path if custom_path else None

    try:
        download(url, is_audio, output_dir)
    except Exception as e:
        print(f"❌ 下载出错：{e}")
        print("提示：检查网络或尝试更新 yt-dlp（pip install -U yt-dlp）")

    input("\n按任意键退出...")