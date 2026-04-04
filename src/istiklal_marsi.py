import argparse
import threading
import time
from pathlib import Path

import docx
import pygame


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Play Istiklal Marsi letters as notes")
    parser.add_argument("--docx", required=True, help="Path to .docx file with the lyrics")
    parser.add_argument("--notes-dir", required=True, help="Directory containing per-letter .wav files")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between notes in seconds")
    return parser.parse_args()


def read_text_from_docx(path: Path) -> str:
    document = docx.Document(str(path))
    return "\n".join(p.text for p in document.paragraphs)


def main() -> None:
    args = parse_args()
    docx_path = Path(args.docx)
    notes_dir = Path(args.notes_dir)

    if not docx_path.exists():
        raise FileNotFoundError(f"Docx file not found: {docx_path}")
    if not notes_dir.exists():
        raise FileNotFoundError(f"Notes directory not found: {notes_dir}")

    istiklal = read_text_from_docx(docx_path)
    reversed_istiklal = "".join(reversed(istiklal))

    pygame.mixer.init()

    notes = {}
    for char in set(istiklal.lower()):
        if char.isalpha():
            wav_path = notes_dir / f"{char}.wav"
            if wav_path.exists():
                notes[char] = pygame.mixer.Sound(str(wav_path))

    def play_sound(char: str) -> None:
        sound = notes.get(char)
        if sound is None:
            return
        channel = pygame.mixer.Channel(0)
        channel.play(sound)
        time.sleep(args.delay)

    class PlayRegularIstiklal(threading.Thread):
        def run(self):
            for char in istiklal:
                char = char.lower()
                if char.isalpha():
                    play_sound(char)

    class PlayReversedIstiklal(threading.Thread):
        def run(self):
            for char in reversed_istiklal:
                char = char.lower()
                if char.isalpha():
                    play_sound(char)

    regular = PlayRegularIstiklal()
    reversed_thread = PlayReversedIstiklal()
    regular.start()
    reversed_thread.start()
    regular.join()
    reversed_thread.join()


if __name__ == "__main__":
    main()