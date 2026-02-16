import asyncio
from playwright.async_api import async_playwright
import json
import os

async def scrape_threads_post(url):
    """
    Scrapes a Threads post for content and interaction counts.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        print(f"🚀 Navigating to: {url}")
        try:
            await page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Extract content
            # These selectors might change, need to be robust
            content_selector = "div[data-testid='post-text-container']"
            likes_selector = "span:has-text('likes')"
            replies_selector = "span:has-text('replies')"
            
            # Wait for content to load
            await page.wait_for_selector("div", timeout=10000)
            
            # Simple extraction logic (can be refined with specific selectors)
            data = {
                "url": url,
                "title": await page.title(),
                "text": await page.inner_text("body") # Placeholder for specific extraction
            }
            
            # Try to extract specifically
            try:
                # This is a very basic attempt at finding the text
                elements = await page.query_selector_all("span")
                for el in elements:
                    text = await el.inner_text()
                    if "likes" in text.lower():
                        data["likes"] = text
                    if "replies" in text.lower():
                        data["replies"] = text
            except:
                pass
                
            print(f"✅ Extracted: {data['title']}")
            return data
            
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
            return {"error": str(e), "url": url}
        finally:
            await browser.close()

if __name__ == "__main__":
    # Test URL
    test_url = "https://www.threads.net/@zuck/post/C25v0Yrvz-s"
    # Note: Scrapers often need local browser or specific environment
    # Since I'm in a sandbox, I'll just write the code.
    print("Threads Crawler Logic Prepared.")
