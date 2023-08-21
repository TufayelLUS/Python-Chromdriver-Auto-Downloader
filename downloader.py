import requests
import platform
from zipfile import ZipFile
import os


def getLatestStableVersion():
    link = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        resp = requests.get(link, headers=headers).json()
    except:
        print("Failed to open {}".format(link))
        return None
    download_link = resp.get('channels').get(
        'Stable').get('downloads').get('chromedriver')
    if platform.system() == "Windows":
        for data in download_link:
            if data.get('platform') == 'win64':
                return data.get('url')
    if platform.system() == "Linux":
        for data in download_link:
            if data.get('platform') == 'linux64':
                return data.get('url')
    if platform.system() == "Darwin":
        for data in download_link:
            if data.get('platform') == 'mac-x64':
                return data.get('url')
    return None


def downloadLatestChromedriver():
    driver_link = getLatestStableVersion()
    if driver_link is None:
        print("Failed to get latest stable version")
        return None
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    print("Downloading latest stable version of chromedriver, please wait ...")
    try:
        resp = requests.get(driver_link, headers=headers).content
    except:
        print("Failed to open {}".format(driver_link))
    with open("chromedriver.zip", "wb") as f:
        f.write(resp)
    extractZip()
    os.remove("chromedriver.zip")


def extractZip():
    if not os.path.exists("chromedriver.zip"):
        return None
    with ZipFile("chromedriver.zip", 'r') as zObject:
        if platform.system() == "Windows":
            zObject.extract(
                "chromedriver-win64/chromedriver.exe", path=os.getcwd())
        elif platform.system() == "Darwin":
            zObject.extract(
                "chromedriver-mac-x64/chromedriver", path=os.getcwd())
        else:
            zObject.extract(
                "chromedriver-linux64/chromedriver", path=os.getcwd())
        zObject.close()


if __name__ == "__main__":
    downloadLatestChromedriver()
    print("Download completed")
