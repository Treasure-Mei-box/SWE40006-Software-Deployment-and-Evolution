import argparse, collections, re, sys

def main():
    p = argparse.ArgumentParser(description="Text file analyser")
    p.add_argument("file", help="path to a text file")
    p.add_argument("--top", type=int, default=5, help="number of top words")
    args = p.parse_args()

    try:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: {args.file} not found")
        sys.exit(1)

    words = re.findall(r"[a-zA-Z']+", text.lower())
    print(f"Lines: {len(text.splitlines())}")
    print(f"Words: {len(words)}")
    print(f"Characters: {len(text)}")
    print(f"Top {args.top} words:")
    for w, c in collections.Counter(words).most_common(args.top):
        print(f"  {w}: {c}")

if __name__ == "__main__":
    main()