# AICTE Certificate - Static Clone with URL Parameters

This is a **complete static clone** of the AICTE certificate verification page with JavaScript modification to change the certificate ID and name via URL parameters.

## 📁 Structure

```
SCAM_CLONE/
├── index.html                                           # Main HTML file (modified)
├── AICTE Inernship Certification Management Portal_files/  # All dependencies
│   ├── CSS files (bootstrap, AdminLTE, etc.)
│   ├── JavaScript files (angular, jquery, etc.)
│   └── Images (aicte1million2.png, checked.gif, etc.)
└── README.md                                            # This file
```

## 🚀 How to Use

### Option 1: Open Locally

1. Simply open `index.html` in your browser
2. Add URL parameters:
   ```
   file:///C:/path/to/SCAM_CLONE/index.html?cert=ABC123&name=JOHN%20DOE
   ```

### Option 2: Host on Any Web Server

Upload the entire `SCAM_CLONE` folder to:
- GitHub Pages
- Netlify
- Vercel
- Any static hosting

Then access:
```
https://yourdomain.com/index.html?cert=YOUR_CERT_ID&name=YOUR_NAME
```

## 🔧 URL Parameters

- `cert` - Certificate ID to display
- `name` - Name to display (URL encoded for spaces)

### Examples:

**With custom cert and name:**
```
index.html?cert=bddb5c7b067006561a618c7fcc017d03&name=JOHN%20DOE
```

**With different values:**
```
index.html?cert=XYZ789&name=JANE%20SMITH
```

**With special characters (use URL encoding):**
```
index.html?cert=ABC123&name=CHINNAPAREDDY%20VENKATA%20KARTHIK%20REDDY
```

## ⚙️ How It Works

1. **Complete Clone**: The HTML and all dependencies are exact copies from AICTE
2. **JavaScript Injection**: A custom script at the bottom reads URL parameters
3. **Dynamic Replacement**: The script finds and replaces:
   - Certificate ID in `<h4>` elements containing "Certificate ID:"
   - Name in elements containing "Issued To:"
4. **Multiple Attempts**: Runs at 0ms, 300ms, 800ms, 1.5s, 3s to catch Angular updates

## 🐛 Debugging

Open browser console (F12) to see:
- ✓ Script loaded confirmation
- ✓ URL parameters detected
- ✓ Replacement success messages
- ⚠ Any issues or warnings

## 📝 Notes

- **No server required** - Pure static HTML/CSS/JS
- **No Python/Flask** - Just open in browser or host anywhere
- **All dependencies included** - Works offline
- **URL bar shows your domain** - Not AICTE domain

## 🎯 Perfect For

- QR codes linking to custom certificates
- Static hosting (GitHub Pages, Netlify, etc.)
- Offline use
- Simple deployment without backend
