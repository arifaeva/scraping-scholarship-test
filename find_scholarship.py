import chromadb
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
import asyncio
import json

async def main():
    chroma = await chromadb.AsyncHttpClient("localhost", 8000)
    collection = await chroma.get_collection(
        name="scholarship_list",
        embedding_function=ONNXMiniLM_L6_V2(),
    )

    queries = await collection.query(
        query_texts=["Beasiswa Fully Funded untuk ASEAN di singapore"],
        n_results=2,
        where={"scholarship_type": "Fully Funded"}
    )

    print(json.dumps(queries, indent=4))

if __name__ == "__main__":
    asyncio.run(main())