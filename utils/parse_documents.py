from liteparse import LiteParse

parser = LiteParse()

# Parse all documents in a directory
result = parser.batch_parse(
    input_dir="./document_source",
    output_dir="./parsed_documents",
    ocr_enabled=True,
    recursive=False,              # Include subdirectories
    extension_filter=".pdf",     # Only PDF files
)

print(f"Output written to: {result.output_dir}")