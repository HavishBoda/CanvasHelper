import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("CANVAS_BASE_URL")
HEADERS = {
    "Authorization": f"Bearer {os.getenv('CANVAS_ACCESS_TOKEN')}"
}

def get_courses():
    url = f"{BASE_URL}/api/v1/courses"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_course_files(course_id):
    files = []
    url = f"{BASE_URL}/api/v1/courses/{course_id}/files?per_page=100"

    while url:
        response = requests.get(url, headers=HEADERS)
        data = response.json()

        pdfs = [
            {
                "id": f["id"],
                "name": f["display_name"],
                "url": f["url"]
            }
            for f in data
            if f.get("content-type") == "application/pdf"
        ]
        files.extend(pdfs)

        # Check if there's a next page
        links = response.headers.get("Link")
        next_url = None
        if links:
            parts = links.split(",")
            for part in parts:
                if 'rel="next"' in part:
                    next_url = part.split(";")[0].strip().strip("<>").strip()
        url = next_url

    return files



def download_file(file_url, file_name):
    response = requests.get(file_url, headers=HEADERS)
    with open(f"downloads/{file_name}", "wb") as f:
        f.write(response.content)
    return f"downloads/{file_name}"
