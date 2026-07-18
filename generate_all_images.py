#!/usr/bin/env python3
"""
Complete Image Generation Script for "Become an AI Engineer" Book
Generates all images using gemini-create-photo from prepared prompts.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

def load_manifest():
    """Load the image manifest JSON."""
    manifest_path = Path("images_manifest.json")
    if manifest_path.exists():
        with open(manifest_path) as f:
            return json.load(f)
    return {"images": []}

def ensure_dirs():
    """Create all necessary image directories."""
    dirs = [
        "01_rolle", "02_modelle", "03_landschaft", "04_openai_api",
        "05_token", "06_prompt", "07_rag", "08_agents", "09_eval",
        "10_deployment", "11_inference_opt", "12_caching", "13_finetuning",
        "14_multimodal", "15_mlops", "16_security", "appendix"
    ]
    for d in dirs:
        Path(f"images/{d}").mkdir(parents=True, exist_ok=True)

def generate_image(prompt_file: Path, output_file: Path) -> bool:
    """Generate a single image using gemini-create-photo."""
    if output_file.exists():
        print(f"  SKIP: {output_file.name} already exists")
        return True
    
    prompt = prompt_file.read_text().strip()
    print(f"  Generating: {output_file.name}")
    
    try:
        result = subprocess.run([
            "gemini-create-photo",
            "--prompt", prompt,
            "--output", str(output_file),
            "--aspect", "16:9",
            "--style", "technical"
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print(f"  OK: {output_file.name}")
            return True
        else:
            print(f"  ERROR: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT: {output_file.name}")
        return False
    except FileNotFoundError:
        print("  ERROR: gemini-create-photo not found in PATH")
        return False

def main():
    print("=" * 60)
    print("AI Engineer Book - Image Generation")
    print("=" * 60)
    
    # Ensure directories
    ensure_dirs()
    
    # Load manifest
    manifest = load_manifest()
    
    # Also find all .prompt files
    prompt_files = list(Path("images").rglob("*.prompt"))
    print(f"Found {len(prompt_files)} prompt files")
    
    success = 0
    failed = 0
    
    for prompt_file in sorted(prompt_files):
        # Determine output path
        rel = prompt_file.relative_to("images")
        output_file = prompt_file.with_suffix(".png")
        
        if generate_image(prompt_file, output_file):
            success += 1
        else:
            failed += 1
    
    print(f"\n{'=' * 60}")
    print(f"Complete: {success} generated, {failed} failed")
    print(f"{'=' * 60}")
    
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()