import os, json

with open(os.path.join(os.getcwd(), 'portapp.json'), 'r') as f:
    version = json.load(f)
    version = version['version'] + '-' + version['release']
    f.close()

import requests, hashlib
fetch = json.loads(requests.get('https://api.github.com/repos/portapps/brave-portable/releases/latest').text)
if str(fetch['tag_name']) != str(version):
    link = fetch['assets'][0]['browser_download_url']
    check_sum = (requests.get(fetch['assets'][4]['browser_download_url'])).text
    check_sum = check_sum.split('\n')[0].split()[0]
    file = os.getcwd() + "\\" + link.split('/')[-1]
    response = requests.get(link, stream=True)

    from tqdm.auto import tqdm
    with tqdm.wrapattr(open(file, "wb"), "write", miniters=1,
                       total=int(response.headers.get('content-length', 0)),
                       desc=link.split('/')[-1]) as fout:
        for chunk in response.iter_content(chunk_size=4096):
            fout.write(chunk)
        fout.close()
    print('Checking hash...')
    with open(file, "rb") as f:
        checksum = hashlib.sha256(f.read()).hexdigest()
        print(check_sum)
        print(checksum)
        if checksum == check_sum:
            print('Hash has matched...')
            os.startfile(file)
            import time
            while True:
                time.sleep(1)
                try:
                    os.remove(file)
                    break
                except OSError:
                    pass
        else:
            print('The installation package is corrupted')
else:
    os.system('msg %username% You are using the latest version')