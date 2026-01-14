#!/usr/bin/env python3
"""
Image Hunter
Searches and downloads images for E-Roll/visual assets.

Supports:
- Google Images (via SerpAPI or direct scraping)
- Pexels API
- Unsplash API
- Direct URL download

Usage:
    python image_hunter.py --query "meditation woman sunlight" --output_dir "./e_roll/" --scene_code "SC_01"
"""

import os
import sys
import json
import argparse
import requests
import hashlib
from pathlib import Path
from typing import Optional, List, Dict
from urllib.parse import urlparse, quote_plus

# Force UTF-8 for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# --- Load .env file ---
try:
    from dotenv import load_dotenv
    # Look for .env in parent directories
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded .env from: {env_path}")
    else:
        # Try current directory
        load_dotenv()
except ImportError:
    print("Note: python-dotenv not installed. Using system environment variables only.")

# --- Configuration ---
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "")
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
OUTSCRAPER_API_KEY = os.getenv("OUTSCRAPER_API_KEY", "")

# --- Blocked Domains (Watermarked Stock Sites) ---
BLOCKED_DOMAINS = [
    "shutterstock.com",
    "vecteezy.com",
    "dreamstime.com",
    "freepik.com",
    "istockphoto.com",
    "gettyimages.com",
    "stock.adobe.com",
    "alamy.com",
    "depositphotos.com",
    "123rf.com",
    "bigstockphoto.com",
    "canstockphoto.com",
    "fotolia.com",
    "stockfresh.com",
]

def is_blocked_url(url: str) -> bool:
    """Check if URL is from a blocked stock site."""
    url_lower = url.lower()
    for domain in BLOCKED_DOMAINS:
        if domain in url_lower:
            return True
    return False

# --- Pexels Search ---
def search_pexels(query: str, count: int = 5, orientation: str = "portrait") -> List[Dict]:
    """Search Pexels for images."""
    if not PEXELS_API_KEY:
        print("Warning: PEXELS_API_KEY not set. Skipping Pexels.")
        return []
    
    print(f"Searching Pexels for: {query}")
    
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "per_page": count,
        "orientation": orientation
    }
    
    try:
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers=headers,
            params=params,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        results = []
        for photo in data.get("photos", []):
            results.append({
                "source": "pexels",
                "id": photo["id"],
                "url": photo["src"]["large2x"],
                "thumbnail": photo["src"]["medium"],
                "photographer": photo["photographer"],
                "alt": photo.get("alt", ""),
                "width": photo["width"],
                "height": photo["height"]
            })
        return results
    except Exception as e:
        print(f"Pexels search failed: {e}")
        return []

# --- Bing Images via SerpAPI (PRIMARY) ---
def search_bing_images(query: str, count: int = 5) -> List[Dict]:
    """Search Bing Images via SerpAPI - PRIMARY SOURCE for metaphorical/cinematic imagery."""
    if not SERPAPI_KEY:
        print("Warning: SERPAPI_KEY not set. Skipping Bing Images.")
        return []
    
    print(f"🔍 Searching Bing Images (PRIMARY) for: {query}")
    
    params = {
        "engine": "bing_images",
        "q": query,
        "count": count,
        "api_key": SERPAPI_KEY
    }
    
    try:
        response = requests.get(
            "https://serpapi.com/search",
            params=params,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        results = []
        for img in data.get("images_results", []):
            # Priority: original image > content_url > thumbnail
            # "source" is the SOURCE PAGE (not the image!), avoid it
            image_url = img.get("original") or img.get("content_url") or img.get("thumbnail", "")
            
            # Skip blocked stock sites with watermarks
            if is_blocked_url(image_url):
                continue
            
            results.append({
                "source": "bing",
                "id": hashlib.md5(image_url.encode()).hexdigest()[:12],
                "url": image_url,  # Actual image file, not the page
                "thumbnail": img.get("thumbnail", ""),
                "title": img.get("title", ""),
                "source_page": img.get("source", ""),  # The page where image is hosted
                "width": img.get("original_width", img.get("width", 0)),
                "height": img.get("original_height", img.get("height", 0))
            })
            
            if len(results) >= count:
                break
                
        print(f"   Found {len(results)} usable results from Bing (filtered stock sites).")
        return results
    except Exception as e:
        print(f"Bing Images search failed: {e}")
        return []

# --- Outscraper Google Images (ALTERNATIVE to SerpAPI) ---
def search_outscraper(query: str, count: int = 5) -> List[Dict]:
    """Search Google Images via Outscraper API - Uses lifetime credits."""
    if not OUTSCRAPER_API_KEY:
        print("Warning: OUTSCRAPER_API_KEY not set. Skipping Outscraper.")
        return []
    
    print(f"🔍 Searching Outscraper (Google Images) for: {query}")
    
    headers = {"X-API-KEY": OUTSCRAPER_API_KEY}
    params = {
        "query": query,
        "async": "false"
    }
    
    try:
        response = requests.get(
            "https://api.outscraper.cloud/google-search-images",
            headers=headers,
            params=params,
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        
        results = []
        # Outscraper returns data in data[0] array
        images = data.get("data", [[]])[0] if isinstance(data.get("data"), list) else []
        
        for img in images:
            image_data = img.get("image", {})
            image_url = image_data.get("url", "")
            
            if not image_url:
                continue
            
            # Skip blocked stock sites with watermarks
            if is_blocked_url(image_url):
                continue
                
            results.append({
                "source": "outscraper",
                "id": hashlib.md5(image_url.encode()).hexdigest()[:12],
                "url": image_url,
                "thumbnail": img.get("preview", {}).get("url", ""),
                "title": img.get("title", ""),
                "source_page": img.get("website", {}).get("url", ""),
                "width": image_data.get("width", 0),
                "height": image_data.get("height", 0)
            })
            
            if len(results) >= count:
                break
                
        print(f"   Found {len(results)} usable results from Outscraper (filtered stock sites).")
        return results
    except Exception as e:
        print(f"Outscraper search failed: {e}")
        return []

# --- Unsplash Search ---
def search_unsplash(query: str, count: int = 5, orientation: str = "portrait") -> List[Dict]:
    """Search Unsplash for images."""
    if not UNSPLASH_ACCESS_KEY:
        print("Warning: UNSPLASH_ACCESS_KEY not set. Skipping Unsplash.")
        return []
    
    print(f"Searching Unsplash for: {query}")
    
    params = {
        "query": query,
        "per_page": count,
        "orientation": orientation,
        "client_id": UNSPLASH_ACCESS_KEY
    }
    
    try:
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params=params,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        results = []
        for photo in data.get("results", []):
            results.append({
                "source": "unsplash",
                "id": photo["id"],
                "url": photo["urls"]["full"],
                "thumbnail": photo["urls"]["small"],
                "photographer": photo["user"]["name"],
                "alt": photo.get("alt_description", ""),
                "width": photo["width"],
                "height": photo["height"]
            })
        return results
    except Exception as e:
        print(f"Unsplash search failed: {e}")
        return []

# --- Google Images via SerpAPI (SECONDARY - for cultural/meme density) ---
def search_google_images(query: str, count: int = 5) -> List[Dict]:
    """Search Google Images via SerpAPI - SECONDARY SOURCE for cultural/meme moments."""
    if not SERPAPI_KEY:
        print("Warning: SERPAPI_KEY not set. Skipping Google Images.")
        return []
    
    print(f"🔍 Searching Google Images (SECONDARY) for: {query}")
    
    params = {
        "q": query,
        "tbm": "isch",
        "num": count,
        "api_key": SERPAPI_KEY
    }
    
    try:
        response = requests.get(
            "https://serpapi.com/search",
            params=params,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        results = []
        for img in data.get("images_results", [])[:count]:
            results.append({
                "source": "google",
                "id": hashlib.md5(img["original"].encode()).hexdigest()[:12],
                "url": img["original"],
                "thumbnail": img.get("thumbnail", ""),
                "title": img.get("title", ""),
                "source_page": img.get("link", ""),
                "width": img.get("original_width", 0),
                "height": img.get("original_height", 0)
            })
        return results
    except Exception as e:
        print(f"Google Images search failed: {e}")
        return []

# --- Direct Google Images Scraping (No API) ---
def search_google_images_direct(query: str, count: int = 5) -> List[Dict]:
    """
    Simple Google Images scraping (backup for when no API is available).
    Note: This may break if Google changes their page structure.
    """
    import re
    
    print(f"Searching Google Images (direct) for: {query}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    search_url = f"https://www.google.com/search?q={quote_plus(query)}&tbm=isch"
    
    try:
        response = requests.get(search_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Extract image URLs using regex (fragile but works)
        # Look for data that contains image URLs
        pattern = r'"(https://[^"]+\.(?:jpg|jpeg|png|webp)[^"]*)"'
        urls = re.findall(pattern, response.text)
        
        # Filter and deduplicate
        seen = set()
        results = []
        for url in urls:
            if url not in seen and "gstatic" not in url:
                seen.add(url)
                results.append({
                    "source": "google_direct",
                    "id": hashlib.md5(url.encode()).hexdigest()[:12],
                    "url": url,
                    "thumbnail": url,
                    "title": query,
                    "width": 0,
                    "height": 0
                })
                if len(results) >= count:
                    break
        
        return results
    except Exception as e:
        print(f"Direct Google search failed: {e}")
        return []

# --- Download Image with Validation ---
MIN_FILE_SIZE_BYTES = 5000  # Minimum 5KB for valid image

def download_image(url: str, output_path: str, max_retries: int = 3) -> Optional[str]:
    """
    Download image from URL with validation and retry logic.
    
    - Validates file size > 5KB
    - Retries up to 3 times on failure
    - Deletes invalid/small files
    """
    print(f"Downloading: {url[:80]}...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=60, stream=True)
            response.raise_for_status()
            
            # Determine extension from content-type or URL
            content_type = response.headers.get("Content-Type", "")
            if "jpeg" in content_type or "jpg" in content_type:
                ext = ".jpg"
            elif "png" in content_type:
                ext = ".png"
            elif "webp" in content_type:
                ext = ".webp"
            elif "gif" in content_type:
                ext = ".gif"
            else:
                # Try from URL
                parsed = urlparse(url)
                ext = os.path.splitext(parsed.path)[1] or ".jpg"
            
            # Ensure output path has extension
            if not output_path.endswith(ext):
                output_path = output_path.rsplit(".", 1)[0] + ext
            
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Validate file size
            file_size = os.path.getsize(output_path)
            if file_size < MIN_FILE_SIZE_BYTES:
                print(f"⚠️ File too small ({file_size} bytes), deleting and retrying...")
                os.remove(output_path)
                if attempt < max_retries - 1:
                    continue
                else:
                    print(f"❌ Failed after {max_retries} attempts - file too small")
                    return None
            
            print(f"✅ Saved: {output_path} ({file_size:,} bytes)")
            return output_path
            
        except Exception as e:
            print(f"⚠️ Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                import time
                time.sleep(1)  # Wait before retry
            else:
                print(f"❌ Download failed after {max_retries} attempts")
                return None
    
    return None

# --- Main Pipeline ---
def hunt_images(
    query: str,
    output_dir: str,
    scene_code: str,
    project_id: str = "PROJECT",
    count: int = 3,
    sources: List[str] = None
) -> List[Dict]:
    """
    Search and download images from multiple sources.
    
    Args:
        query: Search query
        output_dir: Directory to save images
        scene_code: Scene identifier
        project_id: Project identifier
        count: Number of images to download
        sources: List of sources to search ("pexels", "unsplash", "google", "google_direct")
    """
    if sources is None:
        # Default: Bing (metaphor/cinematic) first, then Google (cultural/meme)
        sources = ["bing", "google"]
    
    os.makedirs(output_dir, exist_ok=True)
    
    all_results = []
    
    # Search each source with fallback logic
    for source in sources:
        results = []
        
        if source == "bing":
            results = search_bing_images(query, count)
        elif source == "pexels":
            results = search_pexels(query, count)
        elif source == "unsplash":
            results = search_unsplash(query, count)
        elif source == "google":
            results = search_google_images(query, count)
        elif source == "google_direct":
            results = search_google_images_direct(query, count)
        elif source == "outscraper":
            results = search_outscraper(query, count)
            # Fallback to Bing if Outscraper fails
            if not results:
                print("🔄 Outscraper failed, trying Bing as fallback...")
                results = search_bing_images(query, count)
        else:
            print(f"Unknown source: {source}")
            continue
        
        all_results.extend(results)
    
    # If still no results, try all sources
    if not all_results:
        print("🔄 No results from specified sources, trying all available sources...")
        for fallback in ["bing", "google_direct"]:
            if fallback not in sources:
                print(f"Trying fallback source: {fallback}")
                if fallback == "bing":
                    results = search_bing_images(query, count)
                else:
                    results = search_google_images_direct(query, count)
                if results:
                    all_results.extend(results)
                    break
    
    if not all_results:
        print("No images found from any source.")
        return []
    
    # Download top results
    downloaded = []
    for i, result in enumerate(all_results[:count]):
        filename = f"{project_id}_{scene_code}_IMG_{i+1:02d}"
        output_path = os.path.join(output_dir, filename)
        
        saved_path = download_image(result["url"], output_path)
        if saved_path:
            result["local_path"] = saved_path
            downloaded.append(result)
    
    # Save manifest
    manifest_path = os.path.join(output_dir, f"{project_id}_{scene_code}_IMG_manifest.json")
    manifest = {
        "query": query,
        "scene_code": scene_code,
        "project_id": project_id,
        "images": downloaded
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\nDownloaded {len(downloaded)} images. Manifest: {manifest_path}")
    return downloaded

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Image Hunter - Search and download images")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--output_dir", default="./images/", help="Output directory")
    parser.add_argument("--scene_code", default="SC_01", help="Scene code")
    parser.add_argument("--project_id", default="PROJECT", help="Project ID")
    parser.add_argument("--count", type=int, default=3, help="Number of images to download")
    parser.add_argument("--sources", nargs="+", default=["bing", "google"], 
                       help="Sources to search (bing, google, outscraper, pexels, unsplash, google_direct)")
    
    args = parser.parse_args()
    
    results = hunt_images(
        query=args.query,
        output_dir=args.output_dir,
        scene_code=args.scene_code,
        project_id=args.project_id,
        count=args.count,
        sources=args.sources
    )
    
    if results:
        print(f"\nSuccess! Downloaded {len(results)} images.")
        return 0
    else:
        print("\nNo images downloaded.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
