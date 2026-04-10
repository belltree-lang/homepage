import os
import datetime
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
BASE_DOMAIN = "https://bellmfit.com"

def get_url_info(file_path):
    rel_path = os.path.relpath(file_path, PROJECT_ROOT)
    # Convert windows path to standard url
    url_path = rel_path.replace("\\", "/")
    
    if url_path == "index.html":
        final_url = BASE_DOMAIN + "/"
        priority = "1.0"
    else:
        # replace index.html with / for clean urls
        if url_path.endswith("index.html"):
            url_path = url_path[:-10]
        final_url = f"{BASE_DOMAIN}/{url_path}"
        
        # Calculate priority based on depth
        depth = url_path.strip("/").count("/")
        if depth == 0:
            priority = "0.8"
        elif depth == 1:
            priority = "0.7"
        else:
            priority = "0.5"
            
    # Get last modification time
    mod_time = os.path.getmtime(file_path)
    lastmod = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')
    
    return final_url, lastmod, priority


def generate_sitemap():
    exclude_dirs = {"templates", "scripts", "agents", ".git", ".github", "governance", "node_modules", "lolipop_staging", "reports", "assets"}
    
    urls = []

    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Filter directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
        
        for file in files:
            if file.endswith(".html") and file != "maintenance.html":
                file_path = os.path.join(root, file)
                urls.append(get_url_info(file_path))
                
    # Sort urls: root first, then shorter paths
    urls.sort(key=lambda x: (len(x[0]), x[0]))

    # Build XML
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    for loc, lastmod, obj_priority in urls:
        url_elem = ET.SubElement(urlset, "url")
        loc_elem = ET.SubElement(url_elem, "loc")
        loc_elem.text = loc
        lastmod_elem = ET.SubElement(url_elem, "lastmod")
        lastmod_elem.text = lastmod
        priority_elem = ET.SubElement(url_elem, "priority")
        priority_elem.text = obj_priority
        
    # Write to file
    tree = ET.ElementTree(urlset)
    sitemap_path = os.path.join(PROJECT_ROOT, "sitemap.xml")
    
    # Pretty print hack (just indenting manually if needed, or simply write)
    ET.indent(tree, space="  ", level=0)
    
    with open(sitemap_path, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding="utf-8")
        
    print(f"Sitemap generated at: {sitemap_path}")
    print(f"Total URLs: {len(urls)}")

if __name__ == "__main__":
    generate_sitemap()
