#!/bin/python3

import aiofiles, asyncio
from aiohttp import ClientSession
from time import time
from colorama import Fore
import argparse

parser = argparse.ArgumentParser(description='Web Fuzzer For Pentesting.')
parser.add_argument('-u', '--url', help='Enter Target Url!', required=True, metavar='')
parser.add_argument('-w', '--wordlist', help='Enter Wordlist!', required=True, metavar='')

args = parser.parse_args()

results_OK = []

results_RE = []

attempts = 0

async def looker(url, lister, session):

	global attempts

	req = f"http://{url}/{lister}"
	try:
		async with session.get(req, allow_redirects=False) as response:
			if response.status == 200:
				print(Fore.GREEN + f"[>] Url Found ({response.status}) : " + Fore.RESET + f"{req}")
				results_OK.append(req)

			elif response.status in {301,302,307,308}:
				location = response.headers.get('Location', 'No Headers Location')
				print(Fore.CYAN + f"[>] Redirect Url Found ({response.status}) : " + Fore.RESET + f"{req} -> {location}")
				results_RE.append(f"{req} -> {location}")
			else:
				print(Fore.YELLOW + f"[x] Url Not Found ! ({response.status}) " + Fore.RESET + f"[{attempts}]", end='\r', flush=True)
	except Exception as e:
		pass

	attempts += 1

async def insider(dic, session):
	tasks = []
	async with aiofiles.open(dic, 'r') as f:
		lines = await f.readlines()
		tasks = [looker(args.url, line.strip(), session) for line in lines]
		await asyncio.gather(*tasks)


async def main():
	print("w_dEAMON v1.0")
	async with ClientSession() as session:
		await insider(args.wordlist, session)

start = time()
asyncio.run(main())
end = time()
print(f"\nDone in {(end - start):.2f}s")
for result in results_OK:
	print(Fore.GREEN + "FOUND !+> " + Fore.RESET + result)
for result in results_RE:
	print(Fore.CYAN + "Redirect FOUND !+> " + Fore.RESET + result)
