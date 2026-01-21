import argparse
from seleniumbase import SB

def run_scraper():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, default="https://api.ipify.org/")
    parser.add_argument("--proxy", type=str, default=None)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--incognito", action="store_true")
    parser.add_argument("--block-images", action="store_true")
    parser.add_argument("--ad-block", action="store_true")
    parser.add_argument("--xvfb", action="store_true")
    args = parser.parse_args()

    # Dynamic settings dictionary
    sb_settings = {"uc": True}
    if args.proxy: sb_settings["proxy"] = args.proxy
    if args.headless: sb_settings["headless"] = True
    if args.incognito: sb_settings["incognito"] = True
    if args.block_images: sb_settings["block_images"] = True
    if args.ad_block: sb_settings["ad_block"] = True
    if args.xvfb: sb_settings["xvfb"] = True

    with SB(**sb_settings) as sb:
        print(f"Target URL: {args.url}")
        
        # Open URL with CDP Mode
        sb.activate_cdp_mode(args.url)
        sb.sleep(10)

        html = sb.get_page_source()
        
        print("-" * 30)
        if "ipify" in args.url:
            # Clean output for IP check
            print(f"Detected IP: {sb.get_text('body')}")
        else:
            print(f"HTML Length: {len(html)}")
            print(f"Snippet: {html[0:1000]}")
        print("-" * 30)

if __name__ == "__main__":
    run_scraper()
