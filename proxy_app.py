from flask import Flask, request, Response
import requests

app = Flask(__name__)

AICTE_BASE = "https://aictecert.eduskillsfoundation.org/pages/home/verify.php"

@app.route("/verify")
def verify():
    cert = request.args.get("cert")
    if not cert:
        return "Missing cert param", 400

    # 1. Fetch original page from AICTE with proper headers
    upstream_url = f"{AICTE_BASE}?cert={cert}"
    
    # Add headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        r = requests.get(upstream_url, headers=headers, timeout=15, allow_redirects=True)
        r.raise_for_status()  # Raise error for bad status codes
    except requests.RequestException as e:
        return f"Error fetching from AICTE: {str(e)}<br><br>URL attempted: {upstream_url}", 502

    # 2. Inject JavaScript to replace name and cert ID from URL parameters
    custom_name = request.args.get("name", "")
    
    inject_js = f"""
<script>
(function() {{
    // Get URL parameters
    var params = new URLSearchParams(window.location.search);
    var customName = params.get('name') || '{custom_name}';
    var customCert = params.get('cert');
    
    // Function to replace text content
    function replaceContent() {{
        // Replace certificate ID
        if (customCert) {{
            var certElements = document.querySelectorAll('h4');
            certElements.forEach(function(el) {{
                if (el.textContent.includes('Certificate ID:')) {{
                    var parts = el.innerHTML.split(':');
                    if (parts.length > 1) {{
                        el.innerHTML = parts[0] + ': ' + customCert;
                    }}
                }}
            }});
        }}
        
        // Replace name if provided
        if (customName) {{
            var nameElements = document.querySelectorAll('h4');
            nameElements.forEach(function(el) {{
                if (el.textContent.includes('Issued To:')) {{
                    var parts = el.innerHTML.split(':');
                    if (parts.length > 1) {{
                        el.innerHTML = '<strong>Issued To:</strong> ' + customName;
                    }}
                }}
            }});
            
            // Also check for ng-binding class
            var ngBindings = document.querySelectorAll('.ng-binding');
            ngBindings.forEach(function(el) {{
                if (el.textContent.includes('Issued To:')) {{
                    el.innerHTML = '<strong>Issued To:</strong> ' + customName;
                }}
            }});
        }}
    }}
    
    // Run on page load
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', replaceContent);
    }} else {{
        replaceContent();
    }}
    
    // Also run after a short delay to catch Angular updates
    setTimeout(replaceContent, 500);
    setTimeout(replaceContent, 1000);
    setTimeout(replaceContent, 2000);
}})();
</script>
"""
    
    # Insert script before closing body tag
    if "</body>" in html:
        html = html.replace("</body>", inject_js + "</body>")
    else:
        html = html + inject_js

    # 3. Return modified HTML
    return Response(html, status=r.status_code,
                    headers={"Content-Type": "text/html; charset=utf-8"})

@app.route("/")
def home():
    return """
    <html>
    <head><title>AICTE Certificate Proxy</title></head>
    <body>
        <h1>AICTE Certificate Proxy</h1>
        <p>Usage: /verify?cert=CERTIFICATE_ID&name=CUSTOM_NAME</p>
        <p>Example: <a href="/verify?cert=bddb5c7b067006561a618c7fcc017d03&name=NEWNAME">/verify?cert=bddb5c7b067006561a618c7fcc017d03&name=NEWNAME</a></p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
