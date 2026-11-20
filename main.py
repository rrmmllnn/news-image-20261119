#!/usr/bin/env python3
"""news-image-20261119 entry: write the composed front page to /output/entry.png.

The image (entry.png, 1024x1024, PNG) sums up Thursday 19 November 2026's
world news in one picture. Six stories fill the front page:

1. Trump, Xi Jinping and Vladimir Putin hold the first three-way summit
   in Shenzhen and issue a peace declaration on nuclear risks.
2. The International Court of Justice rules that Myanmar committed
   genocide against the Rohingya.
3. Ukraine hits the Kerch Bridge for the third time this week; the rail
   section is struck and train traffic halted.
4. Israeli tanks push into central Gaza, and a Houthi missile damages a
   tower in Riyadh.
5. Anthropic's IPO sets a record: about $81bn raised at $83 a share.
6. The footer carries four more: Cyclone Akvan, the Bangladesh unrest,
   North Korea's expanding uranium enrichment, and Denmark's Greenland
   security deal.

The panels are drawn illustrations of the day's events; the headlines and
captions state the day's reported facts.

The program only copies the bundled image, so two runs write identical
bytes. No network, no randomness, no other file read. Pass --verify to
check the bundled image without writing anything; pass --output to choose
where the copy lands; pass --stories to list the six stories and exit.
"""
import argparse
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DEFAULT_DST = "/output/entry.png"
MAX_BYTES = 1024 * 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
# A complete PNG ends with a 12-byte IEND chunk: zero length, the ASCII
# tag "IEND", and its CRC. Checking the tail catches a truncated file
# that still has a valid header and IHDR dimensions.
PNG_IEND_TAIL = b"\x00\x00\x00\x00IEND\xaeB`\x82"

STORIES = [
    "Trump, Xi and Putin meet in Shenzhen: first three-way summit, peace declaration on nuclear risks",
    "ICJ rules Myanmar committed genocide against the Rohingya",
    "Kerch Bridge hit a third time: rail section struck, trains halted",
    "Israeli tanks push into central Gaza; Houthi missile damages a tower in Riyadh",
    "Anthropic IPO sets a record: about $81bn raised at $83 a share",
    "Also: Cyclone Akvan, Bangladesh unrest, North Korea enrichment, Denmark Greenland deal",
]


def read_png(path):
    """Return the bytes of a file after checking it is a PNG."""
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != PNG_SIGNATURE:
        raise ValueError(f"{path} is not a PNG file")
    return data


def png_dimensions(data):
    """Read width and height from the PNG IHDR chunk."""
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def verify(data):
    """Check the bundled image against the competition's caps.

    The rules cap the image at 1 MiB and 1024 by 1024 pixels; anything
    larger is refused by the gate before judging, so this fails loudly
    here instead of silently submitting a bad file. The IEND tail check
    also rejects a truncated file whose header still looks fine.
    """
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    width, height = png_dimensions(data)
    if (width, height) != (1024, 1024):
        raise ValueError(f"entry.png is {width}x{height}, expected 1024x1024")
    if not data.endswith(PNG_IEND_TAIL):
        raise ValueError("entry.png is truncated: missing the IEND chunk")
    return width, height


def print_stories():
    """List the six stories the front page carries."""
    print("stories on the front page:")
    for i, story in enumerate(STORIES, 1):
        print(f"  {i}. {story}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=DEFAULT_DST,
                        help="where to write the copy (default: %(default)s)")
    parser.add_argument("--verify", action="store_true",
                        help="check the bundled image and exit without writing")
    parser.add_argument("--stories", action="store_true",
                        help="list the six stories and exit without writing")
    args = parser.parse_args(argv)

    if args.stories:
        print_stories()
        return 0
    data = read_png(SRC)
    width, height = verify(data)
    digest = hashlib.sha256(data).hexdigest()
    if args.verify:
        print(f"entry.png OK: {width}x{height}, {len(data)} bytes, sha256 {digest}")
        print_stories()
        return 0
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    shutil.copyfile(SRC, args.output)
    # Re-read the copy and confirm it matches the source byte for byte;
    # a short write (full disk, interrupted copy) must not pass silently.
    written = read_png(args.output)
    if hashlib.sha256(written).hexdigest() != digest:
        raise ValueError(f"{args.output} does not match the bundled image")
    print(f"wrote {args.output} {len(data)} bytes sha256 {digest}")
    print_stories()
    return 0


if __name__ == "__main__":
    sys.exit(main())
