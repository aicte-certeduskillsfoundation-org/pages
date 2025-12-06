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

    # 2. Rewrite HTML (example: replace name + optionally inject JS)
    html = r.text
    
    # Get custom name from URL parameter
    custom_name = request.args.get("name")

    # If custom name provided, replace it in the HTML
    if custom_name:
        # Try direct replacement of known name
        html = html.replace(
            "CHINNAPAREDDY  VENKATA KARTHIK REDDY",
            custom_name
        )
        html = html.replace(
            "CHINNAPAREDDY VENKATA KARTHIK REDDY",
            custom_name
        )

    # Inject JavaScript to dynamically replace name from query parameter
    inject_js = """
<script>
(function () {
  var params = new URLSearchParams(window.location.search);
  var customName = params.get('name');
  if (!customName) return;
  
  // Wait for page to load
  window.addEventListener('DOMContentLoaded', function() {
    var issuedNodes = document.querySelectorAll('h4.ng-binding');
    issuedNodes.forEach(function (el) {
      if (el.textContent.indexOf('Issued To:') === 0) {
        el.textContent = 'Issued To: ' + customName;
      }
    });
    
    // Also try to find and replace in other possible locations
    var allH4 = document.querySelectorAll('h4');
    allH4.forEach(function (el) {
      var text = el.textContent || el.innerText;
      if (text && text.indexOf('Issued To:') >= 0) {
        var nameMatch = text.match(/Issued To:\s*(.+)/);
        if (nameMatch) {
          el.textContent = 'Issued To: ' + customName;
        }
      }
    });
  });
})();
</script>
"""
    html = html.replace("</body>", inject_js + "</body>")

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
