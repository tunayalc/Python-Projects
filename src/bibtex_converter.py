import re

# Parses an MLA formatted reference into its components
def parse_mla(reference: str) -> dict:
    pattern = r"(?P<author>[^,]+?,\s*[^,]+?),\s*(?P<title>.+?)\.\s*(?P<publisher>.+?),\s*(?P<year>\d{4})\."
    match = re.match(pattern, reference)
    if match:
        return match.groupdict()
    return {}

# Parses an APA formatted reference into its components
def parse_apa(reference: str) -> dict:
    pattern = r"(?P<author>[^,]+?),\s*\((?P<year>\d{4})\)\.\s*(?P<title>.+?)\.\s*(?P<publisher>.+?)\."
    match = re.match(pattern, reference)
    if match:
        return match.groupdict()
    return {}

# Parses an ISO 690 formatted reference into its components
def parse_iso690(reference: str) -> dict:
    pattern = r"(?P<author>[^,]+?,\s*[^,]+?),\s*(?P<title>.+?)\.\s*(?P<publisher>.+?),\s*(?P<year>\d{4})\."
    match = re.match(pattern, reference)
    if match:
        return match.groupdict()
    return {}

# Generates a BibTeX entry from parsed reference data
def generate_bibtex(parsed_data: dict) -> str:
    author_key = re.sub(r"[^a-zA-Z]", "", parsed_data.get("author", "").split(",")[0])
    title_key = re.sub(r"[^a-zA-Z]", "", parsed_data.get("title", "").split(":")[0])
    year = parsed_data.get('year', '0000')
    bibtex_entry = f"""@book{{{author_key}_{title_key}_{year},
    author = {{{parsed_data.get('author', '')}}},
    title = {{{parsed_data.get('title', '')}}},
    publisher = {{{parsed_data.get('publisher', '')}}},
    year = {{{parsed_data.get('year', '')}}}
}}"""
    return bibtex_entry

# Converts a reference from MLA, APA, or ISO 690 format to BibTeX
def convert_to_bibtex(reference: str, format_type: str) -> str:
    parsers = {
        'MLA': parse_mla,
        'APA': parse_apa,
        'ISO690': parse_iso690
    }
    parser = parsers.get(format_type.upper())
    if not parser:
        raise ValueError(f"Invalid format type '{format_type}'. Choose from 'MLA', 'APA', or 'ISO690'.")
    
    parsed_data = parser(reference)
    if not parsed_data:
        raise ValueError("Unable to parse the reference. Please ensure it follows the correct format.")
    
    return generate_bibtex(parsed_data)

# Main execution block for example usage
if __name__ == "__main__":
    mla_reference = "Hofstadter, Douglas R. Gödel, Escher, Bach: an eternal golden braid. Basic books, 1999."
    apa_reference = "Hofstadter, D. R. (1999). Gödel, Escher, Bach: an eternal golden braid. Basic books."
    iso690_reference = "HOFSTADTER, Douglas R. Gödel, Escher, Bach: an eternal golden braid. Basic books, 1999."
    
    try:
        print("\nMLA to BibTeX:\n", convert_to_bibtex(mla_reference, 'MLA'))
    except ValueError as e:
        print(f"Error in MLA conversion: {e}")
    
    try:
        print("\nAPA to BibTeX:\n", convert_to_bibtex(apa_reference, 'APA'))
    except ValueError as e:
        print(f"Error in APA conversion: {e}")
    
    try:
        print("\nISO 690 to BibTeX:\n", convert_to_bibtex(iso690_reference, 'ISO690'))
    except ValueError as e:
        print(f"Error in ISO690 conversion: {e}")
