import asyncio
from crawl4ai import AsyncWebCrawler
from ai import client, ScholarshipList, Scholarship

async def main():
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
        for scholarship in response.scholarships:
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

                # Insert to database
                with open("scholarship.log", "a") as f:
                    f.write(f"{scholarship_data.model_dump()}\n")

if __name__ == "__main__":
    asyncio.run(main())
