import asyncio
import json
import sys
import traceback
from ytSearch import VideosSearch, CustomSearch


## Test file to check youtubesearchpython functionality

async def run_query(query: str):
	print(f"Query: {query}")

	try:
		videos_search = VideosSearch(query, limit=20)
		videos_data = await videos_search.next()
		print("VideosSearch response keys:", list(videos_data.keys()))
		print(
			json.dumps(
				{
					"result_count": len(videos_data.get("result", [])),
					"first_result": videos_data.get("result", [None])[0],
				},
				indent=2,
			)
		)
	except Exception as exc:
		print("VideosSearch raised:", repr(exc))
		traceback.print_exc()

	try:
		custom_search = CustomSearch(query=query, searchPreferences="EgIYAw==", limit=1)
		custom_data = await custom_search.next()
		print("CustomSearch response keys:", list(custom_data.keys()))
		print(json.dumps(custom_data, indent=2))
	except Exception as exc:
		print("CustomSearch raised:", repr(exc))
		traceback.print_exc()


async def main(argv):
	if not argv:
		print("Usage: python3 test.py <search-query-or-url>")
		return
	query = argv[0]
	await run_query(query)


if __name__ == "__main__":
	asyncio.run(main(sys.argv[1:]))
