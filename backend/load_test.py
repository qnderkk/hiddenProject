import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return response.status

async def main(url, count):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for _ in range(count)]
        responses = await asyncio.gather(*tasks)
        print(f"Выполнено {len(responses)} запросов")

if __name__ == "__main__":
    URL = "http://localhost:8080/"
    asyncio.run(main(URL, 100000))