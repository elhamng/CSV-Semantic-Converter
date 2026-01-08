import os
import time
import sys
import requests
import json
from dotenv import load_dotenv  # Import dotenv to load .env file
"""this pattern is quite common for API downloads! The general workflow is a standard approach for many APIs that handle bulk data exports:

Common API Download Pattern:
Create Operation/Job → Get operation ID
Poll Status → Check if operation is complete
Check Individual Jobs → Verify each job is ready
Download Files → Get the actual data
Typical Status Flow:
Operation Status: pending → processing → succeeded/completed
Job Status: queued → running → completed
This pattern is used by:
Export APIs (Salesforce, HubSpot, etc.)
Data warehouse exports (BigQuery, Snowflake)
Bulk processing APIs (payment processors, CRM systems)
Report generation APIs
Best Practices (which your code follows):
✅ Polling with timeouts
✅ Checking both operation AND job statuses
✅ Saving status to file for debugging
✅ Only downloading completed jobs
✅ Proper error handling"""



# Load environment variables from .env file
load_dotenv()

BASE = "https://api.example.com/data/version" # <-- replace with correct base URL
TOKEN = os.getenv("EXAMPLE_TOKEN")            # <-- replace or set env var
CONFIG_ID = os.getenv("EXAMPLE_CONFIG_ID")# <-- replace or set env var
FORMAT = os.getenv("EXAMPLE_FORMAT", "csv")                        # Csv or Json
OUT_DIR = "example_exports_csv_data_date"  # Directory to save all downloaded files

if not TOKEN:
    raise RuntimeError("Environment variable 'EXAMPLE_TOKEN' is not set or loaded.")
else:
    print(f"Token loaded successfully: {TOKEN[:10]}...")  # Print the first 10 characters for security


s = requests.Session()
s.headers.update({
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json"
})

def create_operation():
    """Create an operation to fetch data."""
    r = s.post(f"{BASE}/operations", json={
        "configurationId": CONFIG_ID,
        "fileFormat": FORMAT
    }, timeout=60)
    r.raise_for_status()
    data = r.json()
    op_id = data.get("operationId") or data.get("id")
    if not op_id:
        raise RuntimeError(f"No operationId in response: {data}")
    return op_id

def get_status(op_id: str):
    """Get the status of an operation."""
    r = s.get(f"{BASE}/operations/{op_id}/status", timeout=60)
    r.raise_for_status()
    return r.json()

def download_job(job):
    """Download a single job."""
    job_id = job["id"]
    entity = job["entity"]
    download_url = job["links"]["download"]
    file_extension = "csv" if FORMAT.lower() == "csv" else "json"
    file_name = f"{entity}_{job_id}.{file_extension}"
    file_path = os.path.join(OUT_DIR, file_name)

    # Ensure the output directory exists
    os.makedirs(OUT_DIR, exist_ok=True)

    print(f"Downloading {entity} (Job ID: {job_id}) to {file_path}...")
    with s.get(download_url, stream=True, timeout=180) as r:
        r.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
    print(f"Saved {file_path}")

def save_status_to_file(status_data, file_path):
    """Save the operation status to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(status_data, file, indent=4)
    print(f"Operation status saved to {file_path}")

def preprocess_download_links(jobs):
    """Replace incorrect download links with the correct base URL."""
    correct_base_url = "https://api.example.com/data/version/jobs"
    for job in jobs:
        if "links" in job and "download" in job["links"]:
            incorrect_url = job["links"]["download"]
            # Replace the incorrect base URL with the correct one
            job["links"]["download"] = incorrect_url.replace("http://data-api-wrong/version/jobs", correct_base_url)
            print(f"Updated download link for job {job['id']}: {job['links']['download']}")
    return jobs

def main():
    """Main function to create an operation, check status, and download all jobs."""
    op_id = create_operation()
    print("Created operation:", op_id)

    STATUS_FILE_PATH = "operation_status_configID.json"  # File to save the operation status

    # Wait for the operation to complete
    for attempt in range(60):  # ~10 minutes @ 5s intervals
        st = get_status(op_id)
        status = (st.get("status") or st.get("state") or "").lower()
        jobs = st.get("jobs", [])

        # Save the current status to a JSON file
        save_status_to_file(st, STATUS_FILE_PATH)

        print(f"[{attempt}] status={status} jobs={len(jobs)} details={st}")

        if status in {"succeeded", "completed", "done", "ready"}:
            # Preprocess download links to fix incorrect URLs
            jobs = preprocess_download_links(jobs)

            # Download all jobs
            for job in jobs:
                if job["status"].lower() == "completed":
                    download_job(job)
            return

        if status in {"failed", "error"}:
            raise RuntimeError(f"Operation failed: {st}")

        time.sleep(5)

    # If the operation is still running after the timeout, exit gracefully
    raise TimeoutError("Operation did not complete in time. Check the operation_status.json file for details.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:", e, file=sys.stderr)
        sys.exit(1)


        
