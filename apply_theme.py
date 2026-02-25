#!/usr/bin/env python3
"""
Smart theme applicator: Keeps ALL original page content intact.
Only injects: nav, new footer, bg-grid, and CSS link.
Does NOT modify any content sections.
"""

import glob
import re

SKIP_FILES = ['index.html', 'old.index.html', 'llm-info.html']

# CSS link to inject into <head>
CSS_LINK = '<link rel="stylesheet" href="theme-override.css" />'

# New nav to inject right after <body>
NEW_NAV = '''<div class="bg-grid"></div>
<div class="nav-wrap">
  <nav class="nav" id="navPill">
    <a href="index.html" class="nav-logo">
      <svg viewBox="0 0 200 40" height="24" fill="none">
        <path d="M10 20a10 10 0 1020 0 10 10 0 00-20 0z" fill="#2563EB" />
        <text x="35" y="27" font-family="Plus Jakarta Sans" font-weight="800" font-size="24" fill="#0F172A" letter-spacing="-1">no2bounce</text>
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
'''

NEW_FOOTER = '''
  <footer id="n2b-new-footer" class="new-footer">
    <div class="ft-huge">no2bounce</div>
    <div class="ft-grid wrap">
      <div class="ft-brand">
        <svg viewBox="0 0 200 40" height="32" fill="none">
          <path d="M10 20a10 10 0 1020 0 10 10 0 00-20 0z" fill="#06B6D4" />
          <text x="35" y="27" font-family="Plus Jakarta Sans" font-weight="800" font-size="24" fill="#FFFFFF"
            letter-spacing="-1">no2bounce</text>
        </svg>
        <p>Lily Hill House, Lily Hill Road,<br />Bracknell, England, RG12 2SJ</p>
        <p>hello@no2bounce.com</p>
        <div class="ft-socials">
          <a href="https://x.com/no2bounce" target="_blank">Twitter</a> &bull;
          <a href="https://www.linkedin.com/company/no2bounce" target="_blank">LinkedIn</a> &bull;
          <a href="https://www.youtube.com/@no2bounce" target="_blank">YouTube</a>
        </div>
      </div>
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
      <div class="ft-col">
        <h5>Resources</h5>
        <a href="blog.html">Blog</a>
        <a href="newsletter.html">Newsletter</a>
        <a href="api-documentation.html">API Documentation</a>
        <a href="knowledge-base.html">Knowledge Base</a>
        <a href="email-deliverable.html">Email Deliverable</a>
        <a href="case-study.html">Case Study</a>
      </div>
      <div class="ft-col">
        <h5>Compare</h5>
        <a href="no2bounce-vs-bounceban-comparison.html">vs BounceBan</a>
        <a href="no2bounce-vs-millionverifier-comparison.html">vs MillionVerifier</a>
        <a href="no2bounce-vs-neverbounce-comparison.html">vs NeverBounce</a>
        <a href="no2bounce-vs-kickbox-comparison.html">vs Kickbox</a>
        <a href="no2bounce-vs-bouncer-comparison.html">vs Bouncer</a>
      </div>
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
      <p>&copy; 2026 no2bounce. All Rights Reserved.</p>
    </div>
  </footer>
'''

# Nav scroll script
NAV_SCRIPT = '''<script>
document.addEventListener('DOMContentLoaded', () => {
  window.addEventListener('scroll', () => {
    const nav = document.getElementById('navPill');
    if (nav) {
      if (window.scrollY > 50) {
        nav.style.transform = 'scale(0.95) translateY(5px)';
        nav.style.boxShadow = '0 20px 25px -5px rgba(0,0,0,0.05), 0 0 0 1px rgba(0,0,0,0.05)';
      } else {
        nav.style.transform = 'scale(1) translateY(0)';
        nav.style.boxShadow = '0 20px 25px -5px rgba(0,0,0,0.05)';
      }
    }
  });
});
</script>'''

html_files = sorted(glob.glob('*.html'))

for filepath in html_files:
    if filepath in SKIP_FILES:
        print(f"⏭️  Skip {filepath}")
        continue
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    modified = False
    
    # 1. Inject theme-override.css into <head> (before </head>)
    if 'theme-override.css' not in html:
        html = html.replace('</head>', f'{CSS_LINK}\n</head>')
        modified = True
    
    # 2. Inject bg-grid + new nav after <body> tag
    if 'nav-wrap' not in html and 'navPill' not in html:
        html = html.replace('<body>', f'<body>\n{NEW_NAV}')
        modified = True
    
    # 3. Inject NEW_FOOTER + NAV_SCRIPT before </body>
    appends = ''
    if 'n2b-new-footer' not in html:
        appends += f'{NEW_FOOTER}\n'
        modified = True
    if 'navPill' in html and 'scale(0.95)' not in html:
        appends += f'{NAV_SCRIPT}\n'
        modified = True
        
    if appends:
        html = html.replace('</body>', f'{appends}\n</body>')
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ {filepath} — theme and footer applied (content preserved)")
    else:
        print(f"ℹ️  {filepath} — already has theme")

print("\n🎉 Done! All pages themed with new footers and original content intact.")
