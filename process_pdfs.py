import fitz  # PyMuPDF
import os
import json
import re

input_dir = "/app/input"
output_dir = "/app/output"

def extract_title(doc):
    """Extracts the title from PDF metadata or first page header."""
    title = doc.metadata.get("title", "").strip()
    if title and len(title.split()) > 1:
        return title

    first_page = doc[0]
    blocks = first_page.get_text("dict")["blocks"]
    lines = []

    for b in blocks:
        if "lines" in b:
            for l in b["lines"]:
                line_text = " ".join([s["text"] for s in l["spans"]]).strip()
                if len(line_text) > 10 and not re.search(r"\.{3,}", line_text):
                    lines.append(line_text)

    return lines[0] if lines else ""

def extract_outline(doc):
    """Extracts headings based on font size and structure."""
    outline = []
    font_size_levels = {}

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        text = s["text"].strip()
                        size = round(s["size"], 1)

                        if len(text) < 4 or not re.match(r"\d+[\.\d+]*", text[:5]) and not text[0].isupper():
                            continue

                        if size not in font_size_levels:
                            font_size_levels[size] = None

                        line_text = text
                        font_size_levels[size] = None

                        outline.append({
                            "font_size": size,
                            "text": line_text,
                            "page": page_num
                        })

    # Sort font sizes descending & assign levels
    sorted_sizes = sorted(font_size_levels.keys(), reverse=True)
    level_map = {size: f"H{i+1}" for i, size in enumerate(sorted_sizes)}

    # Build outline with levels
    result = []
    for item in outline:
        level = level_map[item["font_size"]]
        result.append({
            "level": level,
            "text": item["text"],
            "page": item["page"]
        })

    return result

def process_pdf(file_path):
    doc = fitz.open(file_path)
    title = extract_title(doc)
    outline = extract_outline(doc)
    return {
        "title": title,
        "outline": outline
    }

def main():
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            print(f"Processing: {filename}")
            path = os.path.join(input_dir, filename)
            result = process_pdf(path)
            output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
