import asyncio
from playwright.async_api import async_playwright
import os

async def run_crawler(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        print(f"🌐 Fetching: {url}")
        try:
            await page.goto(url, wait_until="networkidle", timeout=60000)
            title = await page.title()
            content = await page.content()
            print(f"✅ Success: {title}")
            return {"title": title, "content_length": len(content)}
        except Exception as e:
            print(f"❌ Failed to fetch {url}: {e}")
            return {"error": str(e)}
        finally:
            await browser.close()

if __name__ == "__main__":
    # Test with a simple search or news site
    test_url = "https://www.google.com/search?q=OpenClaw+AI"
    asyncio.run(run_crawler(test_url))
