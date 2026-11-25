#!/usr/bin/env python3
"""Write one short family scene to /output/entry.txt.

The scene is one line of at most 280 characters: Grandma's Wi-Fi password
is still the year grandad was born, and she tells every visitor, "He's
gone, but he still lets people in." Running it twice produces
byte-identical output.
"""

import os

SCENE = (
    "Grandma's Wi-Fi password is still the year grandad was born, "
    "and she tells every visitor, \"He's gone, but he still lets people in.\""
)


def output_directory():
    """The directory the entry is written to, /output unless overridden."""
    return os.environ.get("OUTPUT_DIR", "/output")


def main():
    out_dir = output_directory()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    text = SCENE.strip()
    assert 1 <= len(text) <= 280, "entry must be 1 to 280 characters"
    assert "\n" not in text, "entry must be one line"
    assert text.endswith('."'), "entry must end as one sentence"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    verify(path, text)


def verify(path, expected):
    """Read the file back and confirm it holds exactly the entry scene."""
    with open(path, encoding="utf-8", newline="\n") as f:
        written = f.read()
    assert written == expected + "\n", "entry.txt does not match the scene"
    print(path)
    print(expected)


if __name__ == "__main__":
    main()
