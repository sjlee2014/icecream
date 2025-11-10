"""
Test script to run the scraper locally
Usage: python test_local_scraper.py
"""
import asyncio
from backend.core.database import SessionLocal, init_db
from backend.scraper.improved_scraper import run_improved_scraper

async def main():
    print("🚀 Starting scraper test...")
    print("=" * 60)

    # Initialize database
    init_db()

    # Create database session
    db = SessionLocal()

    try:
        # Run scraper
        result = await run_improved_scraper(db)

        # Print results
        print("\n" + "=" * 60)
        print("✅ Scraping completed!")
        print("=" * 60)
        print(f"Status: {result.status}")
        print(f"Products scraped: {result.products_scraped}")
        print(f"New products: {result.products_new}")
        print(f"Updated products: {result.products_updated}")
        print(f"Duration: {result.duration_seconds:.2f} seconds")

        if result.error_message:
            print(f"\n⚠️ Error: {result.error_message}")

        print("\n📊 View results at:")
        print("  - Dashboard: http://localhost:3000")
        print("  - API: http://localhost:8000/products/")
        print("  - Stats: http://localhost:8000/products/stats")

    except Exception as e:
        print(f"\n❌ Error running scraper: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
