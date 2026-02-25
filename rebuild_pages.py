#!/usr/bin/env python3
"""
Rebuild all no2bounce pages using the new premium design system.
Extracts content from old Webflow pages and reconstructs with new HTML structure.
"""

import os
import re
import glob
from bs4 import BeautifulSoup, Comment

# ============================================================================
# TEMPLATE PARTS
# ============================================================================

def head_template(title, description, canonical, structured_data=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{title}</title>
  <meta content="{description}" name="description" />
  <meta content="{title}" property="og:title" />
  <meta content="{description}" property="og:description" />
  <meta content="https://cdn.prod.website-files.com/66eae2cbd6e32c79aa790593/68820ab1c1147b0eb16168b7_no2bounce%20og.avif" property="og:image" />
  <meta content="width=device-width,initial-scale=1" name="viewport" />
  <link href="https://cdn.prod.website-files.com/66eae2cbd6e32c79aa790593/688b7b9111d7b682ca1dde0f_n2b%20fav%20round.png" rel="icon" />
  <link rel="stylesheet" href="premium-design.css" />
  <link rel="canonical" href="{canonical}" />
  {structured_data}
</head>
'''

NAV_HTML = '''
  <!-- Background Grid -->
  <div class="bg-grid"></div>

  <!-- Floating Nav Pill -->
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
'''

FOOTER_HTML = '''
  <!-- Footer -->
  <footer class="footer">
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

SCRIPTS_HTML = '''
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      // Nav Shrink on Scroll
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

      // FAQ Accordion
      document.querySelectorAll('.faq-q').forEach(q => {
        q.addEventListener('click', () => {
          const item = q.parentElement;
          const isOpen = item.classList.contains('open');
          document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
          if (!isOpen) item.classList.add('open');
        });
      });
    });
  </script>
</body>
</html>
'''


# ============================================================================
# CONTENT EXTRACTION
# ============================================================================

def clean_text(t):
    """Clean extracted text, removing excessive whitespace."""
    if not t:
        return ""
    return re.sub(r'\s+', ' ', t).strip()

def extract_meta(soup):
    """Extract title, description, canonical, and structured data."""
    title_tag = soup.find('title')
    title = title_tag.get_text() if title_tag else "no2bounce"
    
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    description = desc_tag.get('content', '') if desc_tag else ''
    
    canonical_tag = soup.find('link', rel='canonical')
    canonical = canonical_tag.get('href', '') if canonical_tag else ''
    
    # Extract structured data
    structured = ""
    for script in soup.find_all('script', type='application/ld+json'):
        structured += str(script)
    
    return title, description, canonical, structured

def extract_hero(soup):
    """Extract hero section content: heading, subtext, CTA, and image."""
    hero = {}
    
    # Find h1
    h1 = soup.find('h1')
    if h1:
        hero['heading'] = h1.decode_contents()
    
    # Find hero description text
    for cls in ['text-block-8', 'text-33', 'text-desc', 'text-25']:
        desc = soup.find(class_=cls)
        if desc and len(clean_text(desc.get_text())) > 30:
            hero['description'] = clean_text(desc.get_text())
            break
    
    # Find hero image
    for cls in ['n2b-demo', 'image-30', 'image-34']:
        img = soup.find('img', class_=cls)
        if img:
            hero['image_src'] = img.get('src', '')
            hero['image_alt'] = img.get('alt', '')
            break
    
    # If no hero image found, try first large image
    if 'image_src' not in hero:
        for img in soup.find_all('img'):
            w = img.get('width', '')
            if w and str(w).isdigit() and int(w) > 300:
                hero['image_src'] = img.get('src', '')
                hero['image_alt'] = img.get('alt', '')
                break
    
    return hero

def extract_content_sections(soup):
    """Extract main content sections (blocks of heading + text + optional image)."""
    sections = []
    
    # Common content container classes in the old pages
    containers = []
    for cls in ['risky-email-verification', 'smtp-catch-all', 'instant-results', 
                'free-analysis', 'about-us-2', 'email-sender-hero',
                'plans-pricing', 'integration-section', 'features-section']:
        found = soup.find_all(class_=cls)
        containers.extend(found)
    
    # Also look for generic sections with headings
    for tag in soup.find_all(['h2', 'h3']):
        parent = tag.parent
        while parent and parent.name not in ['section', 'div', 'body']:
            parent = parent.parent
        if parent and parent not in containers and parent.name != 'body':
            containers.append(parent)
    
    seen_texts = set()
    for container in containers:
        heading = container.find(['h2', 'h3'])
        heading_text = clean_text(heading.get_text()) if heading else ""
        
        if heading_text in seen_texts or len(heading_text) < 3:
            continue
        seen_texts.add(heading_text)
        
        # Get paragraphs
        paragraphs = []
        for p in container.find_all(['p', 'div']):
            t = clean_text(p.get_text())
            if len(t) > 40 and t not in paragraphs and t != heading_text:
                paragraphs.append(t)
        
        # Get image
        img = container.find('img')
        img_src = img.get('src', '') if img else ''
        img_alt = img.get('alt', '') if img else ''
        
        if heading_text or paragraphs:
            sections.append({
                'heading': heading_text,
                'paragraphs': paragraphs[:3],  # Max 3 paragraphs per section
                'image_src': img_src,
                'image_alt': img_alt
            })
    
    return sections

def extract_faqs(soup):
    """Extract FAQ items."""
    faqs = []
    
    # Look for FAQ headings and answers
    for accordion in soup.find_all(class_='uui-faq01_accordion'):
        q_el = accordion.find(class_='uui-faq01_heading')
        a_el = accordion.find(class_='uui-text-size-medium-2')
        
        if q_el and a_el:
            q = clean_text(q_el.get_text())
            a = clean_text(a_el.get_text())
            if q and a:
                faqs.append({'question': q, 'answer': a})
    
    return faqs

def extract_stats(soup):
    """Extract any stats/numbers sections."""
    stats = []
    for el in soup.find_all(class_='text-38'):
        val = clean_text(el.get_text())
        label_el = el.find_next(class_='text-39')
        label = clean_text(label_el.get_text()) if label_el else ''
        if val and label:
            stats.append({'value': val, 'label': label})
    return stats

def extract_features_list(soup):
    """Extract feature/benefit lists."""
    features = []
    for li in soup.find_all('li'):
        t = clean_text(li.get_text())
        if 10 < len(t) < 200 and t not in features:
            features.append(t)
    return features[:12]  # Max 12


# ============================================================================
# PAGE BUILDERS
# ============================================================================

def build_hero_section(hero, page_type="default"):
    """Build a hero section matching index.html style."""
    heading = hero.get('heading', 'no2bounce')
    desc = hero.get('description', '')
    img_src = hero.get('image_src', '')
    img_alt = hero.get('image_alt', 'no2bounce')
    
    img_html = ""
    if img_src:
        img_html = f'''
    <div class="hero-visual" style="flex:1; display:flex; align-items:center; justify-content:center;">
      <img src="{img_src}" alt="{img_alt}" style="max-width:100%; height:auto; border-radius:var(--radius-xl); box-shadow:var(--shadow-3d);" />
    </div>'''
    
    return f'''
  <!-- Hero Section -->
  <section class="hero wrap">
    <div class="hero-content">
      <div class="hero-tag">Trusted by 3,000+ businesses worldwide</div>
      <h1>{heading}</h1>
      <p>{desc}</p>
      <form class="hero-form" action="https://app.no2bounce.com/sign-up">
        <input type="email" placeholder="Enter your work email..." required />
        <button type="submit">Try Free</button>
      </form>
      <div class="hero-trust">
        <img src="https://cdn.prod.website-files.com/66eae2cbd6e32c79aa790593/687a53193e49c7b9a8aa9215_trustpilot%20black.svg" alt="Trustpilot" height="24" />
        <div class="trust-div"></div>
        <img src="https://cdn.prod.website-files.com/66eae2cbd6e32c79aa790593/687a536faa0228387b5530c8_g2%20review%20black.svg" alt="G2 Review" height="24" />
      </div>
    </div>
    {img_html}
  </section>
'''

def build_content_section(section, index=0):
    """Build a content section as a sticky card or grid section."""
    heading = section.get('heading', '')
    paragraphs = section.get('paragraphs', [])
    img_src = section.get('image_src', '')
    img_alt = section.get('image_alt', '')
    
    para_html = '\n        '.join(f'<p>{p}</p>' for p in paragraphs)
    
    img_html = ""
    if img_src:
        img_html = f'''
      <div class="sc-visual">
        <img src="{img_src}" alt="{img_alt}" />
      </div>'''
    
    return f'''
  <!-- Content Section -->
  <section class="stack-sec">
    <div class="wrap">
      <div class="s-card" style="position:relative;">
        <div class="sc-content">
          <h3>{heading}</h3>
          {para_html}
        </div>
        {img_html}
      </div>
    </div>
  </section>
'''

def build_stats_section(stats):
    """Build a stats grid."""
    if not stats:
        return ""
    
    items = ""
    for s in stats:
        items += f'''
        <div class="t-item">
          <h4 style="font-size:2.5rem; color:var(--primary);">{s['value']}</h4>
          <p>{s['label']}</p>
        </div>'''
    
    return f'''
  <!-- Stats Grid -->
  <section class="grid-sec">
    <div class="wrap">
      <div class="grid-title"><h2>Our Highlights</h2></div>
      <div class="tilt-grid" style="grid-template-columns: repeat({min(len(stats), 4)}, 1fr);">
        {items}
      </div>
    </div>
  </section>
'''

def build_faq_section(faqs):
    """Build FAQ section matching index.html design."""
    if not faqs:
        return ""
    
    items = ""
    for faq in faqs:
        items += f'''
        <div class="faq-item">
          <div class="faq-q">
            <h4>{faq['question']}</h4>
            <span class="faq-icon">+</span>
          </div>
          <div class="faq-a">
            <p>{faq['answer']}</p>
          </div>
        </div>'''
    
    return f'''
  <!-- FAQ Section -->
  <section class="grid-sec" style="background: var(--bg);">
    <div class="wrap">
      <div class="grid-title"><h2>Frequently Asked Questions</h2></div>
      <div class="faq-container">
        {items}
      </div>
    </div>
  </section>
'''

def build_cta_section():
    """Build CTA banner section."""
    return '''
  <!-- CTA Banner -->
  <section class="marquee-sec" style="transform: none; border-radius: 40px; margin: 80px auto; max-width: 1200px;">
    <div class="wrap" style="text-align: center; padding: 60px 40px;">
      <h2 style="font-family: var(--font-h); font-size: 3rem; font-weight: 800; margin-bottom: 16px; color: white;">Join The Best Now!</h2>
      <p style="font-size: 1.25rem; opacity: 0.9; margin-bottom: 32px; color: rgba(255,255,255,0.9);">Validate your emails and get ahead in the game.</p>
      <a href="https://app.no2bounce.com/sign-up" class="nav-btn" style="background: white; color: var(--primary); padding: 18px 40px; font-size: 16px;">Start Free Trial</a>
    </div>
  </section>
'''


# ============================================================================
# MAIN REBUILD
# ============================================================================

def rebuild_page(filepath):
    """Read a page, extract content, rebuild it completely."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract everything
    title, description, canonical, structured_data = extract_meta(soup)
    hero = extract_hero(soup)
    sections = extract_content_sections(soup)
    faqs = extract_faqs(soup)
    stats = extract_stats(soup)
    
    # Build new page
    page = head_template(title, description, canonical, structured_data)
    page += '<body>\n'
    page += NAV_HTML
    page += build_hero_section(hero)
    
    # Content sections (max 6)
    for i, sec in enumerate(sections[:6]):
        page += build_content_section(sec, i)
    
    # Stats
    if stats:
        page += build_stats_section(stats)
    
    # FAQ
    if faqs:
        page += build_faq_section(faqs)
    
    # CTA
    page += build_cta_section()
    
    # Footer
    page += FOOTER_HTML
    
    # Scripts
    page += SCRIPTS_HTML
    
    return page


# ============================================================================
# RUN
# ============================================================================

SKIP_FILES = ['index.html', 'old.index.html', 'llm-info.html']

# Add FAQ CSS to premium-design.css
faq_css = """

/* FAQ SECTION */
.faq-container {
    max-width: 900px;
    margin: 0 auto;
}

.faq-item {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 20px;
    margin-bottom: 16px;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
}

.faq-item:hover {
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
}

.faq-q {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 28px 32px;
    cursor: pointer;
    gap: 20px;
}

.faq-q h4 {
    font-family: var(--font-h);
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-main);
    margin: 0;
}

.faq-icon {
    font-size: 1.5rem;
    font-weight: 300;
    color: var(--primary);
    transition: transform 0.3s;
    flex-shrink: 0;
}

.faq-item.open .faq-icon {
    transform: rotate(45deg);
}

.faq-a {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.4s cubic-bezier(0.16, 1, 0.3, 1), padding 0.4s;
    padding: 0 32px;
}

.faq-item.open .faq-a {
    max-height: 500px;
    padding: 0 32px 28px;
}

.faq-a p {
    font-size: 1rem;
    line-height: 1.7;
    color: var(--text-muted);
}

/* PAGE HERO (for subpages) */
.page-hero {
    padding: 160px 0 80px;
    text-align: center;
    position: relative;
}

.page-hero h1 {
    font-family: var(--font-h);
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: #020617;
    margin-bottom: 20px;
}

.page-hero h1 span {
    color: var(--primary);
}

.page-hero p {
    font-size: 1.25rem;
    color: var(--text-muted);
    max-width: 600px;
    margin: 0 auto 40px;
}

/* CONTENT CARDS for subpages */
.content-card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 32px;
    padding: 60px;
    display: flex;
    align-items: center;
    gap: 60px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
    margin-bottom: 40px;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.content-card:hover {
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
    transform: translateY(-5px);
}

.content-card:nth-child(even) {
    flex-direction: row-reverse;
}

.content-card .cc-text {
    flex: 1;
}

.content-card .cc-text h3 {
    font-family: var(--font-h);
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 16px;
    line-height: 1.15;
}

.content-card .cc-text p {
    font-size: 1.05rem;
    color: var(--text-muted);
    line-height: 1.7;
    margin-bottom: 12px;
}

.content-card .cc-img {
    flex: 0 0 40%;
}

.content-card .cc-img img {
    width: 100%;
    height: auto;
    border-radius: 20px;
    box-shadow: var(--shadow-3d);
}

@media (max-width: 1024px) {
    .content-card {
        flex-direction: column !important;
        text-align: center;
        padding: 40px;
    }
    .content-card .cc-img {
        flex: none;
        width: 100%;
    }
}

/* LONG FORM TEXT (for legal/policy pages) */
.long-form {
    padding: 160px 0 80px;
}

.long-form h1 {
    font-family: var(--font-h);
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 40px;
    letter-spacing: -0.03em;
}

.long-form h2 {
    font-family: var(--font-h);
    font-size: 1.8rem;
    font-weight: 700;
    margin: 40px 0 16px;
}

.long-form h3 {
    font-family: var(--font-h);
    font-size: 1.4rem;
    font-weight: 700;
    margin: 32px 0 12px;
}

.long-form p, .long-form li {
    font-size: 1.05rem;
    line-height: 1.8;
    color: var(--text-muted);
    margin-bottom: 16px;
}

.long-form ul, .long-form ol {
    padding-left: 24px;
    margin-bottom: 24px;
}

.long-form a {
    color: var(--primary);
    text-decoration: underline;
}
"""

# Append FAQ/page CSS to premium-design.css if not already there
css_path = 'premium-design.css'
with open(css_path, 'r') as f:
    css_content = f.read()

if '.faq-container' not in css_content:
    with open(css_path, 'a') as f:
        f.write(faq_css)
    print("✅ Added FAQ & page styles to premium-design.css")

# Process each HTML file
html_files = sorted(glob.glob('*.html'))
for filepath in html_files:
    if filepath in SKIP_FILES:
        print(f"⏭️  Skipping {filepath}")
        continue
    
    print(f"🔄 Rebuilding {filepath}...")
    try:
        new_html = rebuild_page(filepath)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"   ✅ Done! ({len(new_html)} bytes)")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n🎉 All pages rebuilt!")
