# AICTE Certificate Reverse Proxy

A Flask-based reverse proxy that fetches AICTE certificate pages and allows custom modifications.

## ⚠️ Important Disclaimer

This application is for **educational purposes only**. It creates a mirror of AICTE certificate pages under your own domain. **Do not use this to misrepresent official certificates or for any fraudulent purposes.**

## How It Works

1. Browser requests `https://yourdomain.com/verify?cert=...&name=...`
2. Flask app fetches the original page from `https://aictecert.eduskillsfoundation.org`
3. App modifies the HTML (replaces name or injects JavaScript)
4. Returns the modified HTML to the browser under your domain
5. URL bar shows `yourdomain.com`, not AICTE domain

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Locally

```bash
python proxy_app.py
```

The app will start on `http://localhost:8000`

## Usage

### Basic usage:
```
http://localhost:8000/verify?cert=bddb5c7b067006561a618c7fcc017d03
```

### With custom name:
```
http://localhost:8000/verify?cert=bddb5c7b067006561a618c7fcc017d03&name=CUSTOM%20NAME
```

## Features

- **Static Replacement**: Hardcoded name replacement in Python
- **Dynamic Replacement**: JavaScript injection that reads the `name` query parameter
- **Error Handling**: Graceful handling of network errors and missing parameters

## Deployment

For production deployment:

1. Use a production WSGI server (e.g., Gunicorn):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 proxy_app:app
```

2. Set up HTTPS with a reverse proxy (Nginx/Apache)
3. Configure your domain to point to your server
4. Consider adding:
   - Rate limiting
   - Caching
   - Proper header forwarding
   - Security headers

## Files

- `proxy_app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Notes

- The modified content is only visible through your proxy domain
- Original AICTE website remains unchanged
- This is effectively a custom mirror under your control
- Use responsibly and ethically
