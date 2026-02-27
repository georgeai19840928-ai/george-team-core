import asyncio
from playwright.async_api import async_playwright
import os
import time

async def threads_recon_search(query, max_scrolls=5):
    """
    Task 1.3: Subject Scout - Automatic scrolling and search crawling.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        search_url = f"https://www.threads.net/search?q={query}"
        print(f"🚀 Starting Recon on: {search_url}")
        
        try:
            await page.goto(search_url, wait_until="networkidle", timeout=60000)
            
            all_posts = []
            for i in range(max_scrolls):
                print(f"  Scrolling... ({i+1}/{max_scrolls})")
                
                # Extract currently visible posts
                posts = await page.query_selector_all("div[data-testid='post-container']")
                for post in posts:
                    try:
                        text_el = await post.query_selector("span") # Basic selector, needs refinement
                        text = await text_el.inner_text() if text_el else ""
                        if text and text not in all_posts:
                            all_posts.append(text)
                    except:
                        continue
                
                # Scroll down
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(3) # Wait for load
            
            print(f"✅ Recon complete. Found {len(all_posts)} unique snippets.")
            return all_posts
            
        except Exception as e:
            print(f"❌ Recon failed: {e}")
            return []
        finally:
            await browser.close()

if __name__ == "__main__":
    # Test query aligned with boss's interest
    test_query = "AI Video Workflow"
    # In a real environment, this would be triggered by a task or cron.
    # For now, we prepare the logic.
    print("Threads Recon Script (Task 1.3) Logic Initialized.")
