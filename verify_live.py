import asyncio
import sys
import os
import argparse
import logging
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError


async def verify(url: str, timeout: int = 30000, screenshot_on_fail: bool = True) -> bool:
    """Verify a live site by loading the page and checking for identifying content.

    Returns True on success, False on failure.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        logging.info("Checking URL: %s", url)

        try:
            response = await page.goto(url, timeout=timeout, wait_until="domcontentloaded")

            if response is None:
                logging.error("No response object returned when navigating to %s", url)
                return False

            status = response.status
            logging.info("HTTP status: %s", status)

            # Basic HTTP validation
            if status not in (200, 301, 302):
                logging.warning("Unexpected HTTP status: %s", status)

            title = await page.title()
            logging.info("Title: %s", title)

            # Check page content for an identifying string to avoid false-positive generic pages
            content = await page.content()
            if "BeEKind" in content:
                logging.info("BeEKind content found!")
                return True
            else:
                logging.error("BeEKind content NOT found.")
                if screenshot_on_fail:
                    screenshot_path = os.path.join(os.getcwd(), "verify_live_failure.png")
                    await page.screenshot(path=screenshot_path, full_page=True)
                    logging.info("Saved failure screenshot to %s", screenshot_path)
                return False

        except PlaywrightTimeoutError:
            logging.exception("Timeout while loading %s", url)
            return False
        except Exception:
            logging.exception("Unexpected error while verifying %s", url)
            return False
        finally:
            await browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify a live BeEKind deployment.")
    parser.add_argument("--url", "-u", default=os.environ.get("BEEKIND_URL", "https://beekind-live-v1.onrender.com"),
                        help="URL to verify (can also be set via BEEKIND_URL environment variable)")
    parser.add_argument("--timeout", "-t", type=int, default=int(os.environ.get("BEEKIND_TIMEOUT", "30000")),
                        help="Navigation timeout in milliseconds")
    parser.add_argument("--no-screenshot", dest="screenshot", action="store_false",
                        help="Do not save a screenshot on failure")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO,
                        format="%(asctime)s %(levelname)s: %(message)s")

    url = args.url
    timeout = args.timeout
    screenshot = args.screenshot

    logging.info("Starting verification for %s", url)
    try:
        result = asyncio.run(verify(url, timeout=timeout, screenshot_on_fail=screenshot))
    except KeyboardInterrupt:
        logging.warning("Interrupted by user")
        sys.exit(2)

    if result:
        logging.info("Verification succeeded")
        sys.exit(0)
    else:
        logging.error("Verification failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
