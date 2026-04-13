import json
from pathlib import Path
import re

def normalize_stem(name: str) -> str:
    """
    Remove extension, lower-case, and drop a trailing version suffix like _04 or _12.
    """
    stem = Path(name).stem.lower().strip()
    stem = re.sub(r"_\d{2}$", "", stem)  # remove trailing _04, _12, etc.
    return stem

def resolve_file_path(record, repo_root):
    """
    Try exact path first. If missing, search pdf_outputs for a file whose stem
    matches after normalizing away the trailing version suffix.
    """
    repo_root = Path(repo_root)

    # Exact path from metadata
    relative_path = Path(*record["path"].replace("\\", "/").split("/"))
    full_path = repo_root / relative_path

    if full_path.exists():
        return full_path

    # Fallback: search by normalized stem
    target_stem = normalize_stem(record.get("file_name", full_path.stem))

    search_dir = repo_root / "parsed_documents"
    if not search_dir.exists():
        return None

    candidates = []
    for candidate in search_dir.glob("*"):
        if candidate.is_file():
            candidate_stem = normalize_stem(candidate.name)
            if candidate_stem == target_stem or target_stem in candidate_stem or candidate_stem in target_stem:
                candidates.append(candidate)

    if candidates:
        # Prefer the shortest / most specific match
        candidates.sort(key=lambda p: len(p.name))
        return candidates[0]

    return None

def build_concatenated_text(submitted_metadata, metadata_map_path, repo_root=".", output_path="combined_output.txt"):
    """
    submitted_metadata: dict with keys like domain, submitted_for_country, helpdeskname,
                        segmentname, content_type, content_subtype
    metadata_map_path: path to metadata_map.json
    repo_root: base folder where parsed documents live
    output_path: file where concatenated text will be written
    """
    metadata_map_path = Path(metadata_map_path)
    repo_root = Path(repo_root)
    output_path = Path(output_path)

    with metadata_map_path.open("r", encoding="utf-8") as f:
        metadata_records = json.load(f)

    filter_fields = [
        "domain",
        "submitted_for_country",
        "helpdeskname",
        "segmentname",
        "content_type",
        "content_subtype",
    ]

    matches = []
    for record in metadata_records:
        ok = True
        for field in filter_fields:
            submitted_value = submitted_metadata.get(field)
            if submitted_value is None or submitted_value == "":
                continue
            if str(record.get(field, "")).strip() != str(submitted_value).strip():
                ok = False
                break
        if ok:
            matches.append(record)

    parts = []
    for record in matches:
        resolved_path = resolve_file_path(record, repo_root)

        display_name = record.get("file_name", "unknown_file")

        if resolved_path and resolved_path.exists():
            text = resolved_path.read_text(encoding="utf-8", errors="ignore")
            parts.append(f"===== {display_name} =====\n{text}")
        else:
            parts.append(f"===== {display_name} =====\n[FILE NOT FOUND]")

    combined_text = "\n\n".join(parts)
    output_path.write_text(combined_text, encoding="utf-8")

    return matches, combined_text


submitted_json = {
    "domain": "IT"
}

# Quick Example usage

matches, combined_text = build_concatenated_text(
    submitted_metadata=submitted_json,
    metadata_map_path="metadata_map_IT.json",
    repo_root=".",
    output_path="concatenated_docs.txt"
)

print(f"Matched {len(matches)} documents")