import os
import glob
from bs4 import BeautifulSoup

# The HTML pieces we want to inject:
new_css = '<link rel="stylesheet" href="premium-design.css" />'
bg_grid_html = '<div class="bg-grid"></div>'

nav_html = """
  <div class="nav-wrap">
    <nav class="nav" id="navPill">
      <a href="index.html" class="nav-logo">
        <svg viewBox="0 0 200 40" height="24" fill="none">
          <path d="M10 20a10 10 0 1020 0 10 10 0 00-20 0z" fill="#2563EB" />
          <text x="35" y="27" font-family="Plus Jakarta Sans" font-weight="800" font-size="24" fill="#0F172A"
            letter-spacing="-1">no2bounce</text>
        </svg>
      </a>
      <ul class="nav-links">
        <li><a href="email-verification-tool.html">Product</a></li>
        <li><a href="catch-all-emails.html">Catch-All Engine</a></li>
        <li><a href="pricing.html">Pricing</a></li>
        <li><a href="blog.html">Resources</a></li>
      </ul>
      <a href="https://app.no2bounce.com/sign-up" class="nav-btn">Start Free Trial</a>
    </nav>
  </div>
"""

footer_html = """
  <footer class="footer">
    <div class="ft-huge">no2bounce</div>

    <div class="ft-grid wrap">
      <!-- Brand Column -->
      <div class="ft-brand">
        <svg viewBox="0 0 200 40" height="32" fill="none">
          <path d="M10 20a10 10 0 1020 0 10 10 0 00-20 0z" fill="#06B6D4" />
          <text x="35" y="27" font-family="Plus Jakarta Sans" font-weight="800" font-size="24" fill="#FFFFFF"
            letter-spacing="-1">no2bounce</text>
        </svg>
        <p>Lily Hill House, Lily Hill Road,<br />Bracknell, England, RG12 2SJ</p>
        <p>hello@no2bounce.com</p>
        <div class="ft-socials">
          <a href="https://x.com/no2bounce" target="_blank" aria-label="X/Twitter">Twitter</a> •
          <a href="https://www.linkedin.com/company/no2bounce" target="_blank" aria-label="LinkedIn">LinkedIn</a> •
          <a href="https://www.youtube.com/@no2bounce" target="_blank" aria-label="YouTube">YouTube</a>
        </div>
      </div>

      <!-- Features Column (Platform) -->
      <div class="ft-col">
        <h5>Platform</h5>
        <a href="email-verification-tool.html">Email Validation</a>
        <a href="bulk-email-verifier.html">Bulk Email Validation</a>
        <a href="catch-all-emails.html">Catch-all Verification</a>
        <a href="email-sender-reputation.html">Email Scoring</a>
        <a href="email-finder-tool.html">Email Finder</a>
        <a href="bulk-email-list-cleaning.html">Email Cleaning</a>
        <a href="email-verifier-proxy-infrastructure.html">Proxy Verifier</a>
      </div>

      <!-- Resources Column -->
      <div class="ft-col">
        <h5>Resources</h5>
        <a href="blog.html">Blog</a>
        <a href="newsletter.html">Newsletter</a>
        <a href="api-documentation.html">API Documentation</a>
        <a href="knowledge-base.html">Knowledge Base</a>
        <a href="email-deliverable.html">Email Deliverable</a>
        <a href="case-study.html">Case Study</a>
      </div>

      <!-- Compare Column -->
      <div class="ft-col">
        <h5>Compare</h5>
        <a href="no2bounce-vs-bounceban-comparison.html">vs BounceBan</a>
        <a href="no2bounce-vs-millionverifier-comparison.html">vs MillionVerifier</a>
        <a href="no2bounce-vs-neverbounce-comparison.html">vs NeverBounce</a>
        <a href="no2bounce-vs-kickbox-comparison.html">vs Kickbox</a>
        <a href="no2bounce-vs-bouncer-comparison.html">vs Bouncer</a>
      </div>

      <!-- Company Column -->
      <div class="ft-col">
        <h5>Company</h5>
        <a href="about-us.html">About Us</a>
        <a href="contact-us.html">Contact Us</a>
        <a href="pricing.html">Pricing</a>
        <a href="integration.html">Integrations</a>
        <div class="ft-sub-group">
          <h5>Legal</h5>
          <a href="terms.html">Terms</a>
          <a href="privacy-policy.html">Privacy</a>
          <a href="cookies-policy.html">Cookies</a>
        </div>
      </div>
    </div>

    <div class="ft-bottom wrap">
      <p>© 2026 no2bounce. All Rights Reserved.</p>
    </div>
  </footer>
"""

script_html = """
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      // Nav Shrink
      window.addEventListener('scroll', () => {
        const nav = document.getElementById('navPill');
        if (nav) {
            if (window.scrollY > 50) {
              nav.style.transform = 'scale(0.95) translateY(5px)';
              nav.style.boxShadow = 'var(--shadow-lg), 0 0 0 1px rgba(0,0,0,0.05)';
            } else {
              nav.style.transform = 'scale(1) translateY(0)';
              nav.style.boxShadow = 'var(--shadow-lg)';
            }
        }
      });
    });
  </script>
"""

html_files = glob.glob('*.html')
for file in html_files:
    if file in ['index.html', 'old.index.html']:
        continue
    
    print(f"Processing {file}...")
    with open(file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
    head = soup.find('head')
    if head and not soup.find('link', href='premium-design.css'):
        head.append(BeautifulSoup(new_css, 'html.parser'))
        
    body = soup.find('body')
    if body:
        # Check if bg grid exists
        if not soup.find('div', class_='bg-grid'):
            body.insert(0, BeautifulSoup(bg_grid_html, 'html.parser'))
            
        old_navs = soup.find_all('div', class_='navbar')
        if old_navs:
            for nav in old_navs:
                if 'w-nav' in nav.get('class', []):
                    nav.replace_with(BeautifulSoup(nav_html, 'html.parser'))
        
        old_footers = soup.find_all('footer')
        if old_footers:
            for ft in old_footers:
                ft.replace_with(BeautifulSoup(footer_html, 'html.parser'))
                
        # Inject script for nav behavior
        if not soup.find(string=lambda t: t and 'navPill' in t):
            body.append(BeautifulSoup(script_html, 'html.parser'))
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
