import argparse
from seleniumbase import SB

def run_scraper():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, default="https://api.ipify.org/")
    parser.add_argument("--proxy", type=str, default=None)
    parser.add_argument("--headless", type=str, default=None)
    parser.add_argument("--incognito", type=str, default=None)
    parser.add_argument("--block-images", type=str, default=None)
    parser.add_argument("--ad-block", type=str, default=None)
    parser.add_argument("--xvfb", type=str, default=None)
    args = parser.parse_args()

    # uc=True is our only hardcoded default
    sb_settings = {"uc": True}

    # Helper to only add settings if they are explicitly set
    def add_if_not_none(key, value, is_bool=False):
        if value is not None and value != "" and value.lower() != "default":
            if is_bool:
                sb_settings[key] = str(value).lower() == "true"
            else:
                sb_settings[key] = value

    add_if_not_none("proxy", args.proxy)
    add_if_not_none("headless", args.headless, is_bool=True)
    add_if_not_none("incognito", args.incognito, is_bool=True)
    add_if_not_none("block_images", args.block_images, is_bool=True)
    add_if_not_none("ad_block", args.ad_block, is_bool=True)
    add_if_not_none("xvfb", args.xvfb, is_bool=True)

    print(f"--- SeleniumBase Settings: {sb_settings} ---")

    with SB(**sb_settings) as sb:
        sb.activate_cdp_mode(args.url)
        sb.sleep(10)
        html = sb.get_page_source()
        
        print("-" * 30)
        print(f"URL: {args.url} | Content Length: {len(html)}")
        if "ipify" in args.url:
            print(f"IP Result: {sb.get_text('body')}")
        print("-" * 30)

if __name__ == "__main__":
    run_scraper()
