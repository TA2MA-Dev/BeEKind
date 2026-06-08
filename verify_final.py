import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 5000})
        file_path = "file://" + os.path.abspath("index.html")
        await page.goto(file_path)
        await page.wait_for_timeout(3000)
        await page.screenshot(path="verification/final_full_page.png", full_page=True)

        # Verify specific sections exist
        pillars = await page.query_selector("#tecnologie")
        rewards = await page.query_selector("#ricompense")

        print(f"Pillars section found: {pillars is not None}")
        print(f"Rewards section found: {rewards is not None}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
