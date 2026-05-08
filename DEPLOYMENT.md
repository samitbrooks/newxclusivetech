# Xclusivetech Website - Configuration & Deployment Guide

## Development Environment Setup

### Local Development

#### Option 1: Using Python
```bash
# Python 3
python -m http.server 8000

# Python 2 (deprecated)
python -m SimpleHTTPServer 8000
```

#### Option 2: Using Node.js
```bash
# Install http-server globally (one-time)
npm install -g http-server

# Run server
http-server
```

#### Option 3: VS Code Live Server Extension
1. Install "Live Server" extension by Ritwick Dey
2. Right-click on index.html
3. Select "Open with Live Server"

#### Option 4: Using PHP
```bash
php -S localhost:8000
```

### Access the site
Visit `http://localhost:8000` in your browser

---

## Deployment Guide

### Before Deployment Checklist

- [ ] All pages tested in Chrome, Firefox, Safari, Edge
- [ ] Mobile responsiveness verified on multiple devices
- [ ] Contact form backend configured
- [ ] All images optimized and compressed
- [ ] Meta tags and SEO tags updated
- [ ] Analytics code added (if needed)
- [ ] SSL certificate configured
- [ ] Domain DNS configured
- [ ] All links verified
- [ ] Performance tested (Lighthouse, PageSpeed)

---

## Deployment to Netlify

### Method 1: GitHub Integration (Recommended)
1. Push code to GitHub repository
2. Log in to [Netlify](https://www.netlify.com)
3. Click "New site from Git"
4. Connect GitHub account
5. Select repository
6. Configure build settings:
   - Build command: (leave empty)
   - Publish directory: .
7. Click "Deploy site"
8. Configure custom domain in Netlify dashboard

### Method 2: Manual Deployment (Drag & Drop)
1. Go to Netlify
2. Drag and drop project folder
3. Wait for deployment
4. Configure custom domain

---

## Deployment to Vercel

1. Push to GitHub
2. Go to [Vercel](https://vercel.com)
3. Click "New Project"
4. Import GitHub repository
5. Configure settings (no build needed)
6. Click "Deploy"
7. Configure custom domain

---

## Deployment to Traditional Hosting

### Steps
1. Compress all project files into a .zip file
2. Connect to hosting server via FTP/SFTP
3. Upload files to public_html directory
4. Configure domain DNS settings
5. Set up SSL certificate

### Popular Hosting Providers
- GoDaddy
- Bluehost
- HostGator
- SiteGround
- 1&1 IONOS

---

## Domain Configuration

### DNS Settings for .co.ke Domain

Contact your domain registrar and update these records:

**For Netlify:**
```
Type: CNAME
Name: www
Value: (Netlify will provide)

Type: A
Name: @ (root)
Value: (Netlify will provide)
```

**For Traditional Hosting:**
```
Type: A
Name: @ (root)
Value: (Hosting provider IP)

Type: CNAME
Name: www
Value: (Hosting provider value)
```

---

## SSL Certificate Configuration

### For Netlify/Vercel
- Automatically configured (Free Let's Encrypt)
- Auto-renewal enabled by default

### For Traditional Hosting
1. Use Let's Encrypt (Free)
2. Or purchase from:
   - Comodo
   - DigiCert
   - GoDaddy
   - Namecheap

---

## Performance Optimization

### Image Optimization
- Use tools like TinyPNG, ImageOptim
- Convert to WebP format where possible
- Implement lazy loading

### Code Optimization
- Minify CSS and JavaScript
- Use production builds
- Remove unused code

### Caching
- Enable browser caching
- Use CDN (Content Delivery Network)
- Configure server caching headers

---

## SEO Setup

### Search Engine Submission
1. **Google Search Console**
   - Go to [Google Search Console](https://search.google.com/search-console)
   - Add property
   - Verify ownership
   - Submit sitemap.xml

2. **Bing Webmaster Tools**
   - Go to [Bing Webmaster Tools](https://www.bing.com/webmasters)
   - Add site
   - Submit sitemap

### Analytics Setup
1. Google Analytics
   - Create account at analytics.google.com
   - Add tracking code to all pages
   - Configure goals

---

## Contact Form Backend Configuration

### Email Service Integration

#### Using EmailJS (Recommended for Static Site)
```javascript
// Install via CDN in HTML
<script type="text/javascript" src="https://cdn.emailjs.com/sdk/2.3.2/email.min.js"></script>

// Initialize in main.js
emailjs.init("YOUR_PUBLIC_KEY");
```

#### Using Formspree
```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
    <!-- form fields -->
</form>
```

#### Using Basin
```html
<form action="https://usebasin.com/f/YOUR_FORM_ID" method="POST">
    <!-- form fields -->
</form>
```

#### Using Backend Service
- Set up Node.js/Python backend
- Configure API endpoint
- Add CORS headers
- Send emails via Nodemailer/SendGrid

---

## Monitoring & Maintenance

### Regular Tasks
- [ ] Check analytics weekly
- [ ] Monitor uptime monthly
- [ ] Update content as needed
- [ ] Review and respond to contact form submissions
- [ ] Update portfolio with new projects
- [ ] Check for broken links monthly
- [ ] Update SSL certificate (if manual)
- [ ] Review security headers

### Monitoring Tools
- Uptime Robot - Website uptime monitoring
- Google Search Console - SEO monitoring
- Google Analytics - Traffic analytics
- Lighthouse - Performance monitoring

---

## Troubleshooting

### Site Not Loading
1. Check DNS configuration
2. Verify files are uploaded
3. Check domain expiration
4. Clear browser cache

### Contact Form Not Working
1. Verify backend service is running
2. Check API endpoint
3. Verify CORS headers
4. Check browser console for errors

### Performance Issues
1. Optimize images
2. Enable caching
3. Use CDN
4. Minify CSS/JS
5. Reduce HTTP requests

---

## Support & Resources

- Netlify Docs: https://docs.netlify.com
- Vercel Docs: https://vercel.com/docs
- Google Domains: https://domains.google.com
- Let's Encrypt: https://letsencrypt.org

---

**Last Updated:** May 2, 2026
**Version:** 1.0.0
