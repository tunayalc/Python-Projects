import argparse
import json
import os
import re
from pathlib import Path

import praw


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export Reddit comments to JSONL")
    parser.add_argument("--url", required=True, help="Reddit submission URL")
    parser.add_argument("--client-id", help="Reddit API client id (or REDDIT_CLIENT_ID env)")
    parser.add_argument("--client-secret", help="Reddit API client secret (or REDDIT_CLIENT_SECRET env)")
    parser.add_argument("--user-agent", help="Reddit API user agent (or REDDIT_USER_AGENT env)")
    parser.add_argument("--output-dir", default="data", help="Directory to write JSONL output")
    return parser.parse_args()


def clean_filename(filename: str) -> str:
    return re.sub(r"[<>:\"/\\|?*]", "", filename)


def main() -> None:
    args = parse_args()
    client_id = args.client_id or os.getenv("REDDIT_CLIENT_ID")
    client_secret = args.client_secret or os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = args.user_agent or os.getenv("REDDIT_USER_AGENT")

    if not client_id or not client_secret or not user_agent:
        raise SystemExit("Missing Reddit API credentials. Use flags or set env vars.")

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )

    submission = reddit.submission(url=args.url)
    submission.comments.replace_more(limit=0)

    data = []
    for comment in submission.comments:
        if comment.body:
            data.append({
                "prompt": submission.title.strip(),
                "completion": comment.body.strip(),
            })

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    clean_title = clean_filename(submission.title[:50])
    output_file = output_dir / f"{clean_title}.jsonl"

    with output_file.open("w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Comments saved to {output_file}")


if __name__ == "__main__":
    main()