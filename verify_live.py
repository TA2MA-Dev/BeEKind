import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        url = "https://beekind-live-v1.onrender.com"
        print(f"Checking URL: {url}")

        try:
            response = await page.goto(url, timeout=30000)
            print(f"Status: {response.status}")
            title = await page.title()
            print(f"Title: {title}")

            # Check for specific content to ensure it's not a generic 404
            content = await page.content()
            if "BeEKind" in content:
                print("BeEKind content found!")
            else:
                print("BeEKind content NOT found.")

        except Exception as e:
            print(f"Error: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
