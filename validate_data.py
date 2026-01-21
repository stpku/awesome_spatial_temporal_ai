#!/usr/bin/env python3
"""Validate Awesome Spatio-Temporal AI data files"""

import json
import sys
from pathlib import Path

DATA_DIR = Path("awesomelist")
SCHEMA_DIR = Path("schemas")

def validate_github_projects(data: dict) -> list:
    """Validate github_projects.json"""
    errors = []
    required_fields = ["name", "url", "description"]
    
    for i, category in enumerate(data.get("categories", [])):
        for j, project in enumerate(category.get("projects", [])):
            for field in required_fields:
                if field not in project:
                    errors.append(f"Category[{i}][{j}]: missing {field}")
            
            # Validate URL
            if "url" in project and not project["url"].startswith(("http://", "https://")):
                errors.append(f"Project[{i}][{j}]: invalid URL format")
    
    return errors

def validate_latest_projects(data: dict) -> list:
    """Validate latest_projects.json"""
    errors = []
    
    for section in ["spatial_intelligence", "world_models"]:
        for i, project in enumerate(data.get(section, [])):
            if "name" not in project:
                errors.append(f"{section}[{i}]: missing name")
            if "url" not in project:
                errors.append(f"{section}[{i}]: missing url")
            if "description" not in project:
                errors.append(f"{section}[{i}]: missing description")
    
    return errors

def validate_conferences(data: dict) -> list:
    """Validate conferences.json"""
    errors = []
    
    for i, conf in enumerate(data.get("conferences", [])):
        if "name" not in conf:
            errors.append(f"Conference[{i}]: missing name")
        if "url" not in conf:
            errors.append(f"Conference[{i}]: missing url")
    
    return errors

def validate_journals(data: dict) -> list:
    """Validate journals.json"""
    errors = []
    
    for section in ["international", "chinese"]:
        for i, journal in enumerate(data.get(section, [])):
            if "name" not in journal:
                errors.append(f"{section}[{i}]: missing name")
            if "url" not in journal:
                errors.append(f"{section}[{i}]: missing url")
    
    return errors

def validate_media_channels(data: dict) -> list:
    """Validate media_channels.json"""
    errors = []
    
    # Validate wechat publications
    for i, pub in enumerate(data.get("wechat_publications", [])):
        if "name" not in pub:
            errors.append(f"wechat_publications[{i}]: missing name")
    
    # Validate newsletters
    for i, news in enumerate(data.get("newsletters", [])):
        if "name" not in news:
            errors.append(f"newsletters[{i}]: missing name")
        if "url" not in news:
            errors.append(f"newsletters[{i}]: missing url")
    
    return errors

def validate_datasets(data: dict) -> list:
    """Validate datasets.json"""
    errors = []
    
    for i, dataset in enumerate(data.get("datasets", [])):
        if "name" not in dataset:
            errors.append(f"datasets[{i}]: missing name")
        if "url" not in dataset:
            errors.append(f"datasets[{i}]: missing url")
        if "description" not in dataset:
            errors.append(f"datasets[{i}]: missing description")
        
        # Validate URL
        if "url" in dataset:
            url = dataset["url"]
            if not url.startswith(("http://", "https://")):
                errors.append(f"datasets[{i}]: invalid URL format")
    
    return errors

def validate_papers(data: dict) -> tuple:
    """Validate papers.json with data quality checks"""
    errors = []
    warnings = []
    
    for i, paper in enumerate(data.get("papers", [])):
        # Required fields check
        if "title" not in paper:
            errors.append(f"papers[{i}]: missing title")
        if "url" not in paper:
            errors.append(f"papers[{i}]: missing url")
        if "year" not in paper:
            errors.append(f"papers[{i}]: missing year")
        
        # Data quality checks
        if "authors" in paper:
            authors = paper["authors"]
            # Check for placeholder values
            if "unknown" in authors.lower() or "tbd" in authors.lower() or "todo" in authors.lower():
                errors.append(f"papers[{i}]: invalid author placeholder")
        
        if "url" in paper:
            url = paper["url"]
            # Check for placeholder URLs
            if "11111111" in url or "example.com" in url or "placeholder" in url:
                errors.append(f"papers[{i}]: invalid URL placeholder")
            
            # Validate URL format
            if not url.startswith(("http://", "https://")):
                errors.append(f"papers[{i}]: invalid URL format")
        
        if "venue" in paper:
            venue = paper["venue"]
            if venue in ["TBD", "Unknown", "TBA"]:
                errors.append(f"papers[{i}]: invalid venue placeholder")
    
    return errors, warnings


def main():
    """Main validation function"""
    validators = {
        "github_projects.json": validate_github_projects,
        "latest_projects.json": validate_latest_projects,
        "conferences.json": validate_conferences,
        "journals.json": validate_journals,
        "media_channels.json": validate_media_channels,
        "datasets.json": validate_datasets,
        "papers.json": validate_papers,
    }
    
    all_errors = []
    all_warnings = []
    file_count = 0
    
    print("Validating data files...\n")
    
    for filename, validator in validators.items():
        filepath = DATA_DIR / filename
        
        if not filepath.exists():
            all_errors.append(f"{filename}: file not found")
            continue
        
        try:
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
            
            result = validator(data)
            
            # Handle both old style (list) and new style (tuple) return types
            if isinstance(result, tuple):
                errors, warnings = result
            else:
                errors = result
                warnings = []
            
            if errors:
                all_errors.extend([f"{filename}: {e}" for e in errors])
                print(f"[FAIL] {filename}")
            else:
                print(f"[OK]   {filename}")
                file_count += 1
            
            if warnings:
                all_warnings.extend([f"{filename}: {w}" for w in warnings])
                
        except json.JSONDecodeError as e:
            all_errors.append(f"{filename}: invalid JSON - {e}")
            print(f"[FAIL] {filename}")
        except Exception as e:
            all_errors.append(f"{filename}: {e}")
            print(f"[FAIL] {filename}")

    # Optional: JSON Schema validation for github_projects.json
    # JSON Schema validations (if schemas exist)
    schema_map = {
        "github_projects.json": "github_projects.schema.json",
        "latest_projects.json": "latest_projects.schema.json",
        "conferences.json": "conferences.schema.json",
        "journals.json": "journals.schema.json",
        "media_channels.json": "media_channels.schema.json",
        "datasets.json": "datasets.schema.json",
        "papers.json": "papers.schema.json",
    }
    try:
        import jsonschema  # type: ignore
        for data_file, schema_file in schema_map.items():
            schema_path = SCHEMA_DIR / schema_file
            data_path = DATA_DIR / data_file
            if schema_path.exists() and data_path.exists():
                schema = json.loads(schema_path.read_text(encoding="utf-8"))
                payload = json.loads(data_path.read_text(encoding="utf-8"))
                jsonschema.validate(payload, schema)
                print(f"[OK]   {data_file} (schema)")
        print()
    except Exception as e:
        all_errors.append(f"schema validation: {e}")
        print("[FAIL] schema validation\n")
    
    print()
    
    if all_warnings:
        print(f"Warnings ({len(all_warnings)}):")
        for warning in all_warnings:
            print(f"  [!] {warning}")
        print()
    
    if all_errors:
        print(f"Errors ({len(all_errors)}):")
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print(f"All {file_count} files validated successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
