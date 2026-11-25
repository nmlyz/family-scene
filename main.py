#!/usr/bin/env python3
"""Write one short family scene to /output/entry.txt.

The scene is one line of at most 280 characters: Grandma's Wi-Fi password
is still the year grandad was born, and she tells every visitor, "He's
gone, but he still lets people in." Running it twice produces
byte-identical output.
"""

import os

MAX_CHARS = 280

SCENE = (
    "Grandma's Wi-Fi password is still the year grandad was born, "
    "and she tells every visitor, \"He's gone, but he still lets people in.\""
)


def output_directory():
    """The directory the entry is written to, /output unless overridden."""
    return os.environ.get("OUTPUT_DIR", "/output")


def validate_scene(text):
    """Check the scene against the entry gate, raising ValueError if it fails.

    The gate requires UTF-8 text of 1 to 280 characters, not only white
    space, and this entry is a single line with no wasted words, so the
    checks also reject line breaks and stray surrounding whitespace.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing white space")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.endswith('."'):
        raise ValueError("entry must end as one sentence")
    return text


def entry_text():
    """The exact scene text, validated before anything is written."""
    return validate_scene(SCENE.strip())


def write_entry(path, text):
    """Write the entry atomically: a partial file is never left behind.

    The text goes to a temporary file in the same directory first, is
    flushed to disk, and only then replaces the destination, so a reader
    never sees a half-written entry.
    """
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
        f.flush()
        os.fsync(f.fileno())
    try:
        os.chmod(tmp_path, 0o644)
    except OSError:
        pass
    os.replace(tmp_path, path)


def main():
    out_dir = output_directory()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    text = entry_text()
    write_entry(path, text)
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
