from seleniumbase import SB

with SB(uc=True, 
        proxy="http://10.156.0.22:8888", 
        # xvfb=True,
        headless=False,
        locale="en", 
        incognito=True, 
        block_images=True,
        ) as sb:
    
    url = "https://www.immowelt.de/expose/f6dd6b66-3ec3-4682-80f8-25533496f226"
    sb.activate_cdp_mode(url)

    sb.sleep(6)

    html = sb.get_page_source()
    print("HTML Length:", len(html))
    print(html[0:2000])
