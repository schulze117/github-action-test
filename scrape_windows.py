from seleniumbase import SB

spoof_js = """
    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    // Overwrite the GPU info
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
        if (parameter === 37446) return 'NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0';
        if (parameter === 37445) return 'Google Inc. (NVIDIA)';
        return getParameter(parameter);
    };
    """

url = "https://www.immowelt.de/expose/861ec471-b596-49ab-a962-fedd794d2bd9"

with SB(uc=True, 
        proxy="http://34.107.127.238:8888", 
        
        ) as sb:
    # 1. Spoof BEFORE opening the URL
    # This method is valid here because we are NOT in "CDP Mode", we are in "Driver Mode"
    sb.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": spoof_js})

    # 2. Set Window Size (Imitate Laptop)
    sb.set_window_size(1920, 1080)

    # 3. Open URL (Standard driver method)
    # Do NOT call sb.activate_cdp_mode(args.url)
    sb.open(url) 
    
    sb.sleep(5)
    html = sb.get_page_source()
    print("HTML Length:", len(html))
    print(html[0:800])
