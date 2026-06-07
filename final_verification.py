import asyncio
from playwright.async_api import async_playwright
import os

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load local file
        file_path = f"file://{os.getcwd()}/index.html"
        await page.goto(file_path)

        # Check title
        title = await page.title()
        print(f"Title: {title}")

        # Take screenshot
        os.makedirs("verification", exist_ok=True)
        await page.screenshot(path="verification/final_landing_page.png", full_page=True)

        # Verify specific sections
        mission = await page.is_visible("#mission")
        pillars = await page.is_visible("#pillars")
        rewards = await page.is_visible("#rewards")
        social_heading = await page.is_visible("text=Seguici sui Social")

        print(f"Mission visible: {mission}")
        print(f"Pillars visible: {pillars}")
        print(f"Rewards visible: {rewards}")
        print(f"Social heading visible: {social_heading}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
