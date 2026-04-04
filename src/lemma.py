import argparse
from pathlib import Path

import pandas as pd
import stanza


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find most common lemma per column")
    parser.add_argument("--input", required=True, help="Path to CSV or Excel file")
    parser.add_argument("--sheet", help="Excel sheet name (if using .xlsx)")
    parser.add_argument("--lang", default="tr", help="Stanza language code")
    parser.add_argument("--no-download", action="store_true", help="Skip stanza model download")
    return parser.parse_args()


def load_dataframe(path: Path, sheet: str | None) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path, sheet_name=sheet)
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    raise ValueError("Unsupported file type. Use .csv or .xlsx")


def find_most_common_lemma(nlp, column) -> str:
    word_counts = {}
    for text in column:
        doc = nlp(text)
        for sentence in doc.sentences:
            for word in sentence.words:
                lemma = word.lemma
                if len(lemma) > 3:
                    word_counts[lemma] = word_counts.get(lemma, 0) + 1

    if not word_counts:
        return ""
    return max(word_counts, key=word_counts.get)


def main() -> None:
    args = parse_args()
    if not args.no_download:
        stanza.download(args.lang)
    nlp = stanza.Pipeline(args.lang)

    path = Path(args.input)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    df = load_dataframe(path, args.sheet)

    for column in df.columns:
        most_common_lemma = find_most_common_lemma(nlp, df[column].apply(str))
        print(f"Most common lemma for '{column}': {most_common_lemma}")


if __name__ == "__main__":
    main()