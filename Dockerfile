FROM python:3.10
WORKDIR /app
COPY process_pdfs.py .
RUN pip install pymupdf
CMD ["python", "process_pdfs.py"]
