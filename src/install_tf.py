import requests
from zipfile import ZipFile
import stat
import platform
import sys
import os

base_url = "https://releases.hashicorp.com/terraform"


def download_file(url):
    local_filename = url.split("/")[-1]
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(f"../{local_filename}", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err}")
        sys.exit(1)
    return local_filename

def get_os_version():
    machine = platform.machine()
    system = platform.system()

    machine_map = {"x86_64": "amd64"}
    system_map = {"Darwin": "darwin", "Linux": "linux"}

    return f"{system_map.get(system)}_{machine_map.get(machine)}"

def calculate_url_name(base_url, version, os_type):
    return f"{base_url}/{version}/terraform_{version}_{os_type}.zip"

def unzip_file(filename):
    try:
        zip = ZipFile(f"../{filename}")
        zip.extractall()
    except OSError as e:
        print(f"Error: {e}")
        sys.exit(1)

def add_execute_file_permission(filename):
    try:
        st = os.stat(f"../{filename}")
        os.chmod(f"../{filename}", st.st_mode | stat.S_IEXEC)
    except OSError as e:
        print(f"Error: {e}")
        sys.exit(1)

def install(tf_ver):
    os_type = get_os_version()
    url = calculate_url_name(base_url, tf_ver, os_type)
    downloaded_filename = download_file(url)
    unzip_file(downloaded_filename)
    add_execute_file_permission("terraform")
