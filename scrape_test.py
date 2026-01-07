from seleniumbase import SB

with SB(uc=True, 
        # proxy=PROXY_URL, 
        xvfb=True,
        headless=True,
        locale="en", 
        incognito=True, 
        block_images=True,
        ) as sb:
    
    url = "https://www.immowelt.de/expose/8c1cd9b8-c2be-4fe0-9f12-007137aa2836"
    sb.activate_cdp_mode(url)

    sb.sleep(4)

    html = sb.get_page_source()
    print("HTML Length:", len(html))