import argparse
from seleniumbase import SB

def run_scraper():
    # 1. Parse Arguments (So the YAML inputs actually work)
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, default="https://www.immowelt.de/expose/861ec471-b596-49ab-a962-fedd794d2bd9")
    parser.add_argument("--proxy", type=str, default="http://34.107.127.238:8888")
    parser.add_argument("--headless", type=str, default="false") 
    args = parser.parse_args()

    # 2. JavaScript to Spoof WebGL (Your existing logic)
    spoof_js = """
    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
        if (parameter === 37446) return 'NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0';
        if (parameter === 37445) return 'Google Inc. (NVIDIA)';
        return getParameter(parameter);
    };
    """

    print(f"--- Starting Scraper ---")
    print(f"Target: {args.url}")
    print(f"Proxy: {args.proxy if args.proxy else 'None'}")

    # 3. Configure SB
    # We force a Windows 10 User Agent because 'windows-latest' on GitHub 
    # is actually Windows Server, which looks suspicious to anti-bots.
    sb_args = {
        "uc": True,
        "test": True,
        "locale_code": "de-DE",  # Important for German sites
        "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }

    # Handle Proxy
    if args.proxy:
        sb_args["proxy"] = args.proxy

    # Handle Headless (Use 'headless2' for better stealth)
    if args.headless.lower() == "true":
        sb_args["headless2"] = True
    else:
        sb_args["headless"] = False

    with SB(**sb_args) as sb:
        # 4. Apply WebGL Spoof BEFORE navigation
        sb.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": spoof_js})

        # 5. Set realistic window size
        sb.set_window_size(1920, 1080)

        # 6. Open URL
        try:
            sb.open(args.url)
            
            # 7. Random sleep to mimic human load time
            sb.sleep(8) 
            
            # 8. Check if we are blocked
            title = sb.get_title()
            print(f"Page Title: {title}")
            
            if "Robot" in title or "Captcha" in title or "Access Denied" in title:
                print("!!! DETECTED AS BOT !!!")
            else:
                html = sb.get_page_source()
                print(f"Success! HTML Length: {len(html)}")
                # Print a safe snippet (e.g., first 500 chars)
                print(html[:500])

        except Exception as e:
            print(f"Error during scraping: {e}")
            # Take a screenshot to debug on GitHub Artifacts
            sb.save_screenshot("error_screenshot.png")

if __name__ == "__main__":
    run_scraper()
