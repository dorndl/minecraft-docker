import requests
import sys
import xml.etree.ElementTree as ET
from packaging.version import Version
import argparse

request_timeout = 15

def vanilla_api(version):
    if args.download:
        print("Fetching version_manifest.json...", end=" ", flush=True)

    try:
        version_manifest_r = requests.get('https://piston-meta.mojang.com/mc/game/version_manifest.json', timeout=request_timeout)
        version_manifest_r.raise_for_status()
        version_manifest = version_manifest_r.json()
        versions = version_manifest["versions"]

    except requests.exceptions.ConnectionError as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print("Could not reach host 'https://piston-meta.mojang.com/'\n")

        sys.exit(1)

    except requests.exceptions.Timeout as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print(f"Connection to host 'https://piston-meta.mojang.com/' timed out after {request_timeout} seconds\n")

        sys.exit(1)

    except requests.exceptions.HTTPError as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print(f"Host at 'https://piston-meta.mojang.com/mc/game/version_manifest.json' responded with status code {e.response.status_code}\n")

        sys.exit(1)

    except KeyError as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print("The key 'versions' does not exist in 'version_manifest.json'; This could be the result of an api change on Mojang's side\n")

        sys.exit(1)

    except Exception as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print("Some unkown error occured\n")

        sys.exit(1)


    if args.download:
        print("\033[1;32mDone\033[0m", flush=True)
        print(f"Searching for version {version}...", end=" ", flush=True)

    try:
        for version_entry in versions:
            if version_entry["id"] == version:
                manifest_url = version_entry["url"]
                break
    
        else:
            manifest_url = None
            if args.download:
                print("\033[1;31mNot Found\033[0m", flush=True)
                print(f"The Minecraft version '{version}' does either not exist or has a typo\n")

            sys.exit(1)

    except KeyError as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print("Either of the keys {'id', 'url'} does not exist in 'version_manifest.json'; This could be the result of an api change on Mojang's side\n")

        sys.exit(1)

    except Exception as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print("Some unknown error occured\n")

        sys.exit(1)

    if args.download:
        print("\033[1;32mDone\033[0m")
        print(f"Fetching {version}.json...", end=" ")

    try:
        manifest_r = requests.get(manifest_url, timeout=request_timeout)
        manifest_r.raise_for_status()
        manifest = manifest_r.json()
        vanilla_download_url = manifest["downloads"]["server"]["url"]
        vanilla_server_name = vanilla_download_url.split("/")[-1]

    except requests.exceptions.ConnectionError as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print("Could not reach host 'https://piston-meta.mojang.com/'\n")

        sys.exit(1)

    except requests.exceptions.Timeout as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print(f"Connection to host 'https://piston-meta.mojang.com/' timed out after {request_timeout} seconds\n")

        sys.exit(1)

    except requests.exceptions.HTTPError as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print(f"Host at 'https://piston-meta.mojang.com/v1/packages/.../{version}.json' responded with status code {e.response.status_code}\n")

        sys.exit(1)

    except KeyError as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print("One or more of the keys {'downloads', 'server', 'url'} do not exist in '{version}.json'; This could be the result of an api change on Mojang's side\n")

        sys.exit(1)

    except Exception as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print("Some unkown error occured\n")

        sys.exit(1)

    if not args.download:
        print(f"vanilla|{version}|<loader_version>|<fabric_installer_version>|{vanilla_download_url}|{vanilla_server_name}")
    else:
        print("\033[1;32mDone\033[0m")
        download_server(vanilla_download_url, vanilla_server_name)


def paper_api(mc_version, project, build_nr):
    if not build_nr:
        build_nr = "latest"
    
    if args.download:
        if build_nr == "latest":
            print("Fetching latest build metadata...", end=" ")
        else:
            print(f"Fetching build #{build_nr} metadata...", end=" ")

    try:
        download = requests.get(f"https://fill.papermc.io/v3/projects/{project}/versions/{mc_version}/builds/{build_nr}").json()
        build_nr = download["id"]
        paper_downloads = download["downloads"]
    
    except requests.exceptions.ConnectionError as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print("Could not reach host 'https://fill.papermc.io'\n")

        sys.exit(1)

    except requests.exceptions.Timeout as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print(f"Connection to host 'https://fill.papermc.io' timed out after {request_timeout} seconds\n")

        sys.exit(1)

    except requests.exceptions.HTTPError as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print(f"Host at 'https://fill.papermc.io/v3/projects/.../{build_nr}' responded with status code {e.response.status_code}\n")

        sys.exit(1)

    except KeyError as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print(f"Either of the keys {'id', 'downloads'} do not exist in '.../builds/{build_nr}'; This could be the result of an api change on Mojang's side\n")

        sys.exit(1)

    except Exception as e:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print("Some unkown error occured\n")

        sys.exit(1)

    try:
        paper_download_url = paper_downloads["server:default"]["url"]

    except:
        if args.download:
            print("\033[1;31mFailed\033[0m", flush=True)
            print("Either of the keys {'id}")

        sys.exit(1)

    paper_server_name = paper_download_url.split("/")[-1]
    if not args.download:
        print(f"{project}|{mc_version}|{build_nr}|<fabric_installer_version>|{paper_download_url}|{paper_server_name}")
    else:
        print("\033[1;32mDone\033[0m")
        download_server(paper_download_url, paper_server_name)


def forge_api(mc_version, forge_version):
    if args.download:
        print("Fetching promotions_slim.json...", end=" ")

    if not forge_version:
        forge_versions = requests.get("https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json").json()
        promos = forge_versions["promos"]

        if args.download:
            print("\033[1;32mDone\033[0m")
            print(f"Searching for {mc_version}-recommended...", end=" ")

        recommended = promos.get(f"{mc_version}-recommended")
        if recommended:
            if args.download:
                print("\033[1;34mFound\033[0m")

            forge_version = recommended
        else:
            if args.download:
                print("\033[1;31mNot Found\033[0m")
                print(f"Searching for {mc_version}-latest", end=" ")

            latest = promos.get(f"{mc_version}-latest")
            if latest:
                if args.download:
                    print("\033[1;34mFound\033[0m")

                forge_version = latest
            else:
                print("error")
                sys.exit(1)

    if args.download:
        print("Constructing url...", end=" ");

    forge_download_url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{mc_version}-{forge_version}/forge-{mc_version}-{forge_version}-installer.jar"
    forge_server_name = forge_download_url.split("/")[-1]
    if not args.download:
        print(f"forge|{mc_version}|{forge_version}|<fabric_installer_version>|{forge_download_url}|{forge_server_name}")
    else:
        print("\033[1;32mDone\033[0m")
        download_server(forge_download_url, forge_server_name)


def neoforge_api(mc_version, neoforge_version):
    if args.download:
        print("Fetching maven-metadata.xml...", end=" ")

    if not neoforge_version:
        version_metadata = requests.get("https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml")
        metadata_xml = ET.fromstring(version_metadata.content)

        if args.download:
            print("\033[1;32mDone\033[0m")
            print("Matching latest version...", end=" ")

        versions = [version.text for version in metadata_xml.findall(".//version")]

        mc_parts = mc_version.split(".")
        if len(mc_parts) == 3 and mc_parts[0] == "1":
            version_prefix = ".".join(mc_parts[1:])
        else:
            version_prefix = mc_version

        filtered_versions = [
            v for v in versions
            if v.startswith(version_prefix + ".") or v == version_prefix
        ]
        neoforge_version = max(filtered_versions, key=Version)

    if args.download:
        print("\033[1;32mDone\033[0m")
        print("Constructing url...", end=" ")

    neoforge_download_url = f"https://maven.neoforged.net/releases/net/neoforged/neoforge/{neoforge_version}/neoforge-{neoforge_version}-installer.jar"
    neoforge_server_name = neoforge_download_url.split("/")[-1]
    if not args.download:
        print(f"neoforge|{mc_version}|{neoforge_version}|<fabric_installer_version>|{neoforge_download_url}|{neoforge_server_name}")
    else:
        print("\033[1;32mDone\033[0m")
        download_server(neoforge_download_url, neoforge_server_name)


def fabric_api(mc_version, fabric_version, installer_version):
    if not installer_version:
        if args.download:
            print("Fetching latest installer version...", end=" ", flush=True)

        installers = requests.get("https://meta.fabricmc.net/v2/versions/installer/").json()
        installer_version = installers[0]["version"]

    if not fabric_version:
        if args.download:
            print("\033[1;32mDone\033[0m\nFetching latest loader version...", end=" ", flush=True)

        loaders = requests.get("https://meta.fabricmc.net/v2/versions/loader/").json()
        fabric_version = loaders[0]["version"]

    if args.download:
        print("\033[1;32mDone\033[0m\nConstructing url...", end=" ", flush=True)

    fabric_download_url = f"https://maven.fabricmc.net/net/fabricmc/fabric-installer/{installer_version}/fabric-installer-{installer_version}.jar"
    fabric_server_name = fabric_download_url.split("/")[-1]
    if not args.download:
        print(f"fabric|{mc_version}|{fabric_version}|{installer_version}|{fabric_download_url}|{fabric_server_name}")
    else:
        print("\033[1;32mDone\033[0m")
        download_server(fabric_download_url, fabric_server_name)


def downloadbar(downloaded, size, nchars):
    percentage = downloaded/size * 100;
    nprogress = int((downloaded/size)*nchars)

    downloaded_mb = downloaded / 1024 / 1024
    size_mb = size / 1024 / 1024

    bar = '#'*nprogress + ' '*(nchars - nprogress)
    print(f"\r[{bar}] {downloaded_mb:.1f}/{size_mb:.1f} MiB ({percentage:.1f}%)", end="")


def download_server(url, filename):
    print(f"\nDownloading {filename}... ")
    downloadbar(0, 1, 50)
    
    downloaded = 0
    with requests.get(url, stream=True) as r:
        size = int(r.headers.get("Content-Length"))
        with open(filename, "wb") as file:
            for chunk in r.iter_content(chunk_size=8192):
                if not chunk:
                    continue

                file.write(chunk)
                downloaded += len(chunk)
                downloadbar(downloaded, size, 50)

    print("\033[1A", end="")
    print(f"\rDownloading {filename}... \033[1;32mDone\033[0m")
    print("")


parser = argparse.ArgumentParser()

# positional args
parser.add_argument("loader")
parser.add_argument("mc_version")

# optional args
parser.add_argument("--loader-version", default=None)
parser.add_argument("--fabric-installer-version", default=None)

# boolean flag
parser.add_argument("--use-folia", action="store_true")
parser.add_argument("--download", action="store_true")


#parse args
args = parser.parse_args()
if args.use_folia and args.loader != "paper":
    parser.error("error")

match args.loader:
    case "vanilla":
        vanilla_api(args.mc_version)
    case "paper":
        if args.use_folia:
            paper_api(args.mc_version, "folia", args.loader_version)
        else:
            paper_api(args.mc_version, "paper", args.loader_version)
    case "forge":
        forge_api(args.mc_version, args.loader_version)
    case "neoforge":
        neoforge_api(args.mc_version, args.loader_version)
    case "fabric":
        fabric_api(args.mc_version, args.loader_version, args.fabric_installer_version)
    case "_":
        parser.error("error")
