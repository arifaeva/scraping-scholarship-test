import asyncio
from crawl4ai import AsyncWebCrawler
from ai import client, ScholarshipList, Scholarship
import chromadb
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2

async def main():
    chroma = await chromadb.AsyncHttpClient("localhost", 8000)
    collection = await chroma.get_or_create_collection(
        name="scholarship_list",
        embedding_function=ONNXMiniLM_L6_V2()
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://www.schoters.com/id/beasiswa")
        
        res = client.beta.chat.completions.parse(
            model="gpt-4.1",
            messages=[
                { "role": "system", "content": "Extract scholarship list based on given text" },
                { "role": "user", "content": result.markdown },
            ],
            response_format=ScholarshipList
        )

        response = res.choices[0].message.parsed
        for scholarship in response.scholarships[:5]:
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(scholarship.url)

                res = client.beta.chat.completions.parse(
                    model="gpt-4.1",
                    messages=[
                        { "role": "system", "content": "Extract scholarship list based on given text" },
                        { "role": "user", "content": result.markdown },
                    ],
                    response_format=Scholarship,
                )

                scholarship_data = res.choices[0].message.parsed

                await collection.add(
                    documents=[str(scholarship_data.model_dump())],
                    ids=[scholarship_data.url],
                    metadatas=[
                        {
                            "source": "schoters",
                            "scholarship_type": scholarship.scholarship_type,
                        }
                    ]
                )

                # # Insert to database
                # with open("scholarship.log", "a") as f:
                #     f.write(f"{scholarship_data.model_dump()}\n")

if __name__ == "__main__":
    asyncio.run(main())
