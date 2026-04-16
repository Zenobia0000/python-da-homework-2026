"""
外觀 Facade
===========
意圖：提供一個高階介面，屏蔽下層子系統的複雜度。
口訣：客戶端不該知道內部有 5 個元件協作，只需要呼叫 facade.do_thing()。

對比 Adapter：Adapter 解的是「介面不相容」；Facade 解的是「介面太雜」。

例子：影片轉檔。底下 codec / decoder / encoder / muxer 一堆，
      VideoConverter facade 只暴露 convert(file, target_format)。

跑：python facade.py
"""
from __future__ import annotations


# --- 子系統一堆 ----------------------------------------------------
class FileLoader:
    def load(self, path: str) -> bytes:
        print(f"  [Loader] 讀檔 {path}")
        return b"raw_video_bytes"


class CodecDetector:
    def detect(self, data: bytes) -> str:
        print(f"  [Detector] 偵測 codec")
        return "h264"


class Decoder:
    def decode(self, data: bytes, codec: str) -> bytes:
        print(f"  [Decoder] 用 {codec} 解碼")
        return b"decoded_frames"


class Encoder:
    def encode(self, frames: bytes, target: str) -> bytes:
        print(f"  [Encoder] 編成 {target}")
        return b"encoded_frames"


class Muxer:
    def mux(self, frames: bytes, container: str) -> bytes:
        print(f"  [Muxer] 包進 {container} 容器")
        return b"final_file"


class FileWriter:
    def write(self, data: bytes, path: str) -> None:
        print(f"  [Writer] 寫到 {path}")


# --- Facade --------------------------------------------------------
class VideoConverter:
    """客戶端只需要這一張臉，內部 6 個元件愛怎麼換就怎麼換。"""

    def __init__(self) -> None:
        self.loader = FileLoader()
        self.detector = CodecDetector()
        self.decoder = Decoder()
        self.encoder = Encoder()
        self.muxer = Muxer()
        self.writer = FileWriter()

    def convert(self, src: str, dst: str, target_codec: str) -> None:
        print(f"[Facade] convert {src} → {dst} ({target_codec})")
        raw = self.loader.load(src)
        codec = self.detector.detect(raw)
        frames = self.decoder.decode(raw, codec)
        encoded = self.encoder.encode(frames, target_codec)
        muxed = self.muxer.mux(encoded, container="mp4")
        self.writer.write(muxed, dst)
        print("[Facade] done\n")


def main() -> None:
    VideoConverter().convert("input.avi", "output.mp4", "vp9")


if __name__ == "__main__":
    main()
