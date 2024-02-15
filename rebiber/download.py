import tqdm
import requests
import time

confs = ['eccv', 'iccv', 'bmvc', 'cvpr', 'neurips', 'iclr', 'icml']
years = list(range(2020, 2025))

for conf in tqdm.tqdm(confs):
    for year in years:
        cites = ''
        for step in range(10):
            print(step, conf, year)
            s = f'https://dblp.org/search/publ/api?q=conf/{conf}/{year}&h=1000&f={step*1000}&format=bib'
            while True:  # Keep trying until the request is successful
                res = requests.get(s)
                if res.status_code == 429:  # Check if we've hit the rate limit
                    retry_after = int(res.headers.get("Retry-After", 60))  # Default to 60 seconds if header is missing
                    print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                    time.sleep(retry_after)  # Wait for the specified time
                    continue  # Retry the request
                break  # Exit loop if the request was successful or the error is not due to rate limiting

            cs = res.text
            if cs == '':
                print('stop')
                break
            cites += cs
        with open(f'./raw_data/{conf}{year}.bib', 'w') as f:
            f.write(cites)
