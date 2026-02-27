import asyncio
from threads_crawler import ThreadsCrawler
import os
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

async def main():
    crawler = ThreadsCrawler(headless=True)
    
    # 1. Attempt login
    print("🚀 Attempting to log in with provided credentials...")
    login_result = await crawler.login()
    
    if login_result == "2FA_REQUIRED":
        print("🛡️ 2FA detected. Please check your SMS/Email for the code.")
    elif login_result:
        print("✅ Login Success! Proceeding to keyword search...")
        
        # 2. Test keyword search
        results = await crawler.search_by_keyword("openclaw")
        print(f"🔍 Found {len(results)} results for 'openclaw'.")
        
        for r in results[:3]:
            print(f"- [{r['user']}]: {r['text'][:100]}...")
    else:
        print("❌ Login Failed.")

if __name__ == "__main__":
    asyncio.run(main())
