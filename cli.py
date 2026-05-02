import argparse
import sys
from converter import convert_url_to_markdown

def main():
    parser = argparse.ArgumentParser(description="Convert web page to Markdown.")
    parser.add_argument("url", help="URL of the web page to convert")
    parser.add_argument("-o", "--output", default="output.md", help="Output Markdown file path (default: output.md)")

    args = parser.parse_args()

    def progress_callback(msg):
        print(msg)

    success, msg = convert_url_to_markdown(args.url, args.output, progress_callback)

    if not success:
        print(f"Błąd: {msg}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
