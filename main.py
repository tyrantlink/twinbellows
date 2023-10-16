from asyncio import run
from client import Client


async def main() -> None:
	client = Client()
	await client.start()

run(main())