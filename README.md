# Adobe India Hackathon 2025 – Round 1A: PDF Title and Outline Extractor

## Objective
Automatically extract the document title and structured headings (H1, H2, H3) from PDF files and output as JSON.

## Tech Stack
- Python 3.10
- PyMuPDF (`fitz`)
- Docker (offline, CPU-only, AMD64)

## How to Build
```bash
docker build --platform linux/amd64 -t pdf-processor .
