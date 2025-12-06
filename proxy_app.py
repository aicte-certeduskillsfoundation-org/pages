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

    # 2. Clone the entire HTML page
    html = r.text
    
    # 3. Inject JavaScript to replace name and cert ID from URL parameters
    custom_name = request.args.get("name", "")
    custom_cert = request.args.get("cert", "")
    # 3. Inject JavaScript to replace name and cert ID from URL parameters
    custom_name = request.args.get("name", "")
    custom_cert = request.args.get("cert", "")
    
    inject_js = f"""
<script>
console.log('Custom modification script loaded');

(function() {{
    // Get URL parameters
    var params = new URLSearchParams(window.location.search);
    var customName = params.get('name') || decodeURIComponent('{custom_name}');
    var customCert = params.get('cert') || '{custom_cert}';
    
    console.log('Custom Name:', customName);
    console.log('Custom Cert:', customCert);
    
    // Function to replace certificate ID and name
    function replaceContent() {{
        var replaced = false;
        
        // Find and replace all h4 elements
        var h4Elements = document.querySelectorAll('h4');
        h4Elements.forEach(function(el) {{
            var text = el.textContent || el.innerText;
            
            // Replace Certificate ID
            if (customCert && text.includes('Certificate ID:')) {{
                el.innerHTML = '<strong>Certificate ID:</strong> ' + customCert;
                replaced = true;
                console.log('Replaced cert ID');
            }}
            
            // Replace Issued To name
            if (customName && text.includes('Issued To:')) {{
                el.innerHTML = '<strong>Issued To:</strong> ' + customName;
                replaced = true;
                console.log('Replaced name');
            }}
        }});
        
        // Also check Angular binding elements
        var ngElements = document.querySelectorAll('.ng-binding');
        ngElements.forEach(function(el) {{
            var text = el.textContent || el.innerText;
            
            if (customCert && text.includes('Certificate ID:')) {{
                el.innerHTML = '<strong>Certificate ID:</strong> ' + customCert;
                replaced = true;
            }}
            
            if (customName && text.includes('Issued To:')) {{
                el.innerHTML = '<strong>Issued To:</strong> ' + customName;
                replaced = true;
            }}
        }});
        
        if (replaced) {{
            console.log('Content replaced successfully');
        }}
        
        return replaced;
    }}
    
    // Try to replace immediately
    var success = replaceContent();
    
    // If not successful, wait for DOM ready
    if (!success) {{
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', replaceContent);
        }} else {{
            replaceContent();
        }}
    }}
    
    // Keep trying at intervals to catch Angular updates
    setTimeout(replaceContent, 300);
    setTimeout(replaceContent, 800);
    setTimeout(replaceContent, 1500);
    setTimeout(replaceContent, 3000);
}})();
</script>
"""
    
    # 4. Insert the script before closing body tag
    if "</body>" in html:
        html = html.replace("</body>", inject_js + "\n</body>")
    elif "</BODY>" in html:
        html = html.replace("</BODY>", inject_js + "\n</BODY>")
    else:
        # If no closing body tag, append at the end
        html = html + inject_js

    # 5. Return the cloned and modified HTML
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
