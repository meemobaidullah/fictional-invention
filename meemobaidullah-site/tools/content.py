"""Content for meemobaidullah.com, carried over from the live site (Nov 2026).

Titles, meta descriptions, robots values and body copy match the live pages.
Do not add figures here that are not already on the live site.
"""

WA = 'https://wa.me/8801731558195'
LIVE_CHAT = 'https://tawk.to/chat/65ffe3e31ec1082f04da9409/default'
EMAIL = 'meemobaidullah@gmail.com'
EMAIL_HREF = 'mailto:' + EMAIL
AGENCY_URL = 'https://www.ecommeem.com/'
AGENCY_HEAD = 'Need a full team behind your store?'
AGENCY_TEXT = ('eCommeem.com is the agency I founded: a full-service Amazon and marketplace team '
               'for account management, PPC, listings, brand building and launches.')
DEFAULT_OG = '/assets/images/meemobaidullah.webp'   # existing image on the live server

# Formspree endpoint of the live contact form (e.g. https://formspree.io/f/xxxxxxx).
# Empty = the form opens the visitor's email app addressed to EMAIL instead.
FORM_ENDPOINT = ''

STEPS = [
    ('Review The Brief', 'Audit your current store, compliance status and growth targets.'),
    ('Setup & Configure', 'Configure listings, inventory systems and operational workflows.'),
    ('Manage Daily Ops', 'Handle orders, support and performance monitoring day to day.'),
    ('Scale & Optimize', 'Ongoing optimization to grow revenue while you stay hands-off.'),
]
SERVICE_PROCESS_INTRO = 'Review, configure, manage and optimize — the same core operating model behind every store I run.'

# ---------------------------------------------------------------- services
SERVICES = [
    dict(slug='fba-automation', nav='Amazon FBA & FBM Management', h1='Amazon FBA & FBM Management',
         eyebrow='01 · Amazon', icon='box', cta='Ready to Automate Your Amazon Store?',
         title='Amazon FBA & FBM Management | Meem Obaidullah',
         desc='Hybrid product research, 2-step listing workflows, bulk inventory management, wholesale and private-label operations.',
         hero='Complete Amazon store management for scalable, hands-free business growth. We handle hybrid generic '
              'product research and 2-step listing creation, bulk inventory management, and specialized support for '
              'Wholesale and Private Label brands — helping sellers automate workflows for smooth daily operations.'),
    dict(slug='walmart-automation', nav='Walmart Automation Services', h1='Walmart Automation & WFS',
         eyebrow='02 · Walmart', icon='cart', cta='Ready to Automate Your Walmart Store?',
         title='Walmart Automation & WFS | Meem Obaidullah',
         desc='Order processing, WFS fulfillment, listing updates, performance monitoring and operational support.',
         hero='We manage your Walmart Seller Center from order processing to seller and WFS fulfillment, listing '
              'updates, and real-time performance monitoring. Our system supports consistent sales growth and '
              'operational efficiency across both US and UK Walmart marketplaces.'),
    dict(slug='tiktok-shop-automation-services', nav='TikTok Shop Operations', h1='TikTok Shop Operations',
         eyebrow='03 · TikTok Shop', icon='video', cta='Ready to Automate Your TikTok Store?',
         title='TikTok Shop Operations | Meem Obaidullah',
         desc='Shipping workflows, customer care, returns, account health and affiliate program integration.',
         hero='We manage your TikTok Shop operations end-to-end, including order handling and 2-step shipping through '
              'your preferred courier network or TikTok Fulfilled (FBT). Our team handles customer inquiries, return '
              'processing and shop-performance monitoring.'),
    dict(slug='temu-store-management-services', nav='Temu Seller Management', h1='Temu Seller Management',
         eyebrow='04 · Temu', icon='tag', cta='Ready to Automate Your Temu Store?',
         title='Temu Seller Management | Meem Obaidullah',
         desc='Fast onboarding, compliance support, catalog structuring, optimized listings and daily operations.',
         hero='Complete Temu seller shop management with fast onboarding, compliance support, and fully optimized '
              'listing setup to help you launch and scale quickly. We handle account activation, product catalog '
              'structuring, and day-to-day operations.'),
    dict(slug='ebay-automation-services', nav='eBay Store Management', h1='eBay Store Management',
         eyebrow='05 · eBay', icon='store', cta='Ready to Automate Your eBay Store?',
         title='eBay Store Management | Meem Obaidullah',
         desc='Product research, SEO listings, inventory control, order processing and customer support.',
         hero='Fully managed eBay store operations covering product research, SEO-optimized listings, inventory '
              'control, order processing and customer support. With data-driven strategies and continuous '
              'optimization, we help improve visibility and conversions.'),
    dict(slug='etsy-store-automation-services', nav='Etsy Shop Management', h1='Etsy Shop Management',
         eyebrow='06 · Etsy', icon='hand', cta='Ready to Automate Your Etsy Store?',
         title='Etsy Shop Management | Meem Obaidullah',
         desc='Store setup, listing optimization, inventory control, shipping profiles and automated order workflows.',
         hero='Complete Etsy shop management and setup including seller account creation, store customization, '
              'optimized product listings, and shipping-profile configuration. We support both physical and digital '
              'products across multiple stores.'),
    dict(slug='mercari-seller', nav='Mercari Store Management', h1='Mercari Store Management',
         eyebrow='07 · Mercari', icon='trend', cta='Ready to Automate Your Mercari Store?',
         title='Mercari Store Management | Meem Obaidullah',
         desc='Setup support, listing optimization and performance tracking across key metrics.',
         hero='Complete Mercari shop management, helping sellers build and operate their own stores. Our service '
              'includes step-by-step setup support, product listing optimization, store management, and performance '
              'tracking across sales and GMV.'),
    dict(slug='shopify-automation', nav='Shopify Store Automation', h1='Shopify Store Automation',
         eyebrow='08 · Shopify', icon='bag', cta='Ready to Automate Your Shopify Store?',
         title='Shopify Store Automation | Meem Obaidullah',
         desc='Store creation, customized design, inventory systems, shipping profiles and automated order workflows.',
         hero='Complete Shopify store management covering daily operations such as inventory control, order '
              'fulfillment, product updates, and customer support. We provide structured workflows to improve store '
              'efficiency and support consistent sales growth.'),
]
for _s in SERVICES:
    _s['path'] = '/%s/' % _s['slug']
SERVICE_BY_SLUG = {s['slug']: s for s in SERVICES}
# "Other Services I Manage" shows the first three of these that are not the current page (as on the live site)
OTHER_SERVICES = ['fba-automation', 'walmart-automation', 'tiktok-shop-automation-services', 'temu-store-management-services']

# ---------------------------------------------------------------- home
HOME = dict(
    path='/', og_image='/assets/images/meemobaidullah.webp',
    title='Meem Obaidullah | E-commerce Entrepreneur — Amazon FBA & Walmart WFS Automation',
    desc='Meem Obaidullah — Top-Rated E-commerce Virtual Assistant & Entrepreneur. Amazon FBA, Walmart WFS, '
         'TikTok Shop, Etsy, Temu & eBay store automation for global investors.',
    hero=dict(
        badge='Top-Rated · Active Status',
        h1_html='Hands-Free Infrastructure for USA &amp; Global <span class="swoosh">E-commerce</span> Entrepreneurs.',
        text='My Team build, scale and manage fully automated Amazon FBA, Walmart WFS, TikTok Shop, Etsy, Temu and '
             'eBay storefronts — so investors stay hands-off while the store stays active, compliant and growing.',
        stats=[('4.9★', 'Rated'), ('500+', 'Active Stores & Accounts Managed')],
        platforms=['Amazon', 'Walmart', 'TikTok Shop', 'Etsy', 'eBay', 'Shopify'],
    ),
    process_intro='The operating flow follows the same core model used across the current home experience: '
                  'review, configure, manage and optimize.',
    credentials='Meem Obaidullah builds and manages practical e-commerce systems for entrepreneurs, investors, and '
                'multi-channel sellers who need reliable daily execution without being tied to every operational task.',
    cred_stats=[('7+', 'Years of Experience'), ('24+', 'Countries Served'), ('8+', 'Major Marketplaces')],
    services=[
        dict(num='01', icon='box', title='Amazon FBA & FBM Management', href='/fba-automation/', btn='Learn More ↗',
             text='Hybrid generic product research, 2-step listing workflows, bulk inventory management, wholesale and private-label operations.'),
        dict(num='02', icon='cart', title='Walmart Automation & WFS', href='/walmart-automation/', btn='Learn More ↗',
             text='Order processing, seller and WFS fulfillment, listing updates, performance monitoring and operational support for US & UK marketplaces.'),
        dict(num='03', icon='video', title='TikTok Shop Operations', href='/tiktok-shop-automation-services/', btn='Learn More ↗',
             text='2-step shipping, TikTok Fulfilled workflows, customer care, returns, account health and affiliate program integration.'),
        dict(num='04', icon='tag', title='Temu Seller Management', href='/temu-store-management-services/', btn='Learn More ↗',
             text='Fast onboarding, compliance support, catalog structuring, optimized listings, daily operations and cash-flow-focused management.'),
        dict(num='05', icon='store', title='eBay Store Management', href='/ebay-automation-services/', btn='Learn More ↗',
             text='Product research, SEO listings, inventory control, order processing, customer support and marketplace expansion.'),
        dict(num='06', icon='bag', title='Etsy & Shopify Automation', href='/shopify-automation/', btn='Learn More ↗',
             text='Store creation, customized design, listing optimization, inventory control, shipping profiles and automated order workflows.'),
        dict(num='07', icon='shield', title='Suspended Account Reopen & Compliance', href='#proof', btn='Open Proof Vault ↗',
             text='Structured support for Amazon Section 3 and Walmart store reinstatement workflows, compliance documentation and appeal preparation.'),
        dict(num='08', icon='play', title='YouTube Cash-Cow Infrastructure', href='/contact/', btn='Learn More ↗',
             text='Faceless asset channel layouts designed to build organic discovery pathways toward storefront and e-commerce assets.'),
    ],
    assets=dict(
        intro='Scalable digital business systems with streamlined execution and minimal day-to-day involvement.',
        tabs=['Operational Walkthroughs', 'Storefront Live Results', 'Client Consultations'],
        features=[
            dict(icon='grid', title='Multi-channel control center', text='Store accounting, sourcing, inventory and daily operations overview.'),
            dict(icon='flow', title='Amazon 2-step workflow', text='Listing, fulfillment and performance workflow presentation.'),
            dict(icon='cart', title='Walmart & marketplace operations', text='Order processing and health-monitoring workflow overview.'),
            dict(icon='layers', title='VA infrastructure architecture', text='Systems, automation and team execution framework.'),
        ],
        channels=[('Amazon FBA', 'Operational'), ('Walmart WFS', 'Monitored'), ('TikTok Shop', 'Active'),
                  ('Temu Seller', 'Optimized'), ('eBay Store', 'Managed'), ('Shopify / Etsy', 'Managed')],
        brief='Use the contact form below to submit your marketplace preference, target portfolio parameters and '
              'operations request. The brief is routed to a direct consultation workflow.',
    ),
    work=dict(
        intro='Suspended-store reopen work and documented performance logs across managed marketplaces.',
        # existing screenshots on the live server (same URLs kept)
        images=[('/assets/store/walmartstore.jpeg', 'E-commerce Asset Metrics'),
                ('/assets/store/amazonprivatepabel.jpeg', 'Amazon FBA Inventory Control'),
                ('/assets/store/amazonsucess.jpeg', 'Walmart Dashboard Scaling')],
        note='Full library of case, consultation and testimonial videos available on request.',
    ),
)

# ---------------------------------------------------------------- about
ABOUT = dict(
    path='/about/', og_image='/assets/images/about/about-left-image.png', robots='index, follow, max-image-preview:large',
    title='About Meem Obaidullah | eCommerce Entrepreneur & Top-Rated Freelancer',
    desc='Learn about Meem Obaidullah, an eCommerce Entrepreneur and Award-Winning Top-Rated Freelancer with 7+ years '
         'of experience helping businesses manage and grow Amazon, Walmart, TikTok Shop, Temu, eBay, Etsy, Mercari '
         'and Shopify operations worldwide.',
    intro='I’m Meem Obaidullah — an eCommerce Entrepreneur and Award-Winning Top-Rated Freelancer helping businesses '
          'build, manage and grow profitable online marketplace operations.',
    about=[
        'With 7+ years of industry experience, I’ve worked with businesses, brands and entrepreneurs across 24+ '
        'countries worldwide. My focus is on making eCommerce operations easier, more organized and more scalable — '
        'from marketplace management and product listings to fulfillment, order processing, account operations and '
        'ongoing performance management.',
        'I specialize in supporting sellers and businesses across major marketplaces including Amazon, Walmart, '
        'TikTok Shop, Temu, eBay, Etsy, Mercari and Shopify.',
    ],
    stats=[('7+', 'Years Experience'), ('24+', 'Countries Served'), ('8+', 'Major Marketplaces')],
    what_intro='I help online sellers and businesses manage their day-to-day marketplace operations while creating '
               'systems designed for consistency, efficiency and long-term growth.',
    what=[
        ('fba-automation', 'Amazon FBA & FBM', 'Marketplace operations, listings, orders, inventory, account management and FBA/FBM workflow support.'),
        ('walmart-automation', 'Walmart Marketplace', 'Walmart marketplace operations, WFS support, listings, orders, inventory and store management.'),
        ('tiktok-shop-automation-services', 'TikTok Shop', 'Seller center management, product operations, orders, listings and day-to-day TikTok Shop support.'),
        ('temu-store-management-services', 'Temu Seller Management', 'Product listings, order processing, seller operations and marketplace workflow management.'),
        ('ebay-automation-services', 'eBay Store Management', 'Store operations, product listing management, order processing and inventory workflows.'),
        ('etsy-store-automation-services', 'Etsy Shop Management', 'Shop management, product operations, listing updates and order workflow support.'),
        ('mercari-seller', 'Mercari Management', 'Product management, marketplace operations, inventory and order support.'),
        ('shopify-automation', 'Shopify Automation', 'Store operations, product management, workflow organization and eCommerce automation support.'),
    ],
    rec_intro='As a Top-Rated Freelancer and eCommerce professional, my work is focused on practical marketplace '
              'operations, reliable communication, organized workflows and long-term business support.',
    recognition=[
        ('award', 'Award-Winning Freelancer', 'Recognized for professional freelance and eCommerce service delivery.'),
        ('globe', 'Global eCommerce Experience', 'Supporting businesses and entrepreneurs across 24+ countries worldwide.'),
        ('layers', 'Marketplace Operations', 'Focused on efficient, organized and scalable eCommerce workflows.'),
    ],
    approach_intro='My goal is not simply to complete tasks. I focus on understanding the business workflow, '
                   'identifying operational gaps and helping create systems that make online businesses easier to manage.',
    approach=[
        ('target', 'Business-Focused', "Every task is connected to your store's operational goals and long-term growth."),
        ('zap', 'Efficient Operations', 'Organized workflows help reduce repetitive work and improve day-to-day efficiency.'),
        ('growth', 'Growth Mindset', 'I focus on building sustainable processes that can support your business as it grows.'),
        ('chat', 'Reliable Support', 'Clear communication, organized execution and dependable ongoing marketplace support.'),
    ],
    closing="Whether you're launching a new marketplace store, managing an existing operation or looking for reliable "
            "eCommerce support, let's discuss how I can help you build a more efficient operation.",
)

# ---------------------------------------------------------------- contact
CONTACT = dict(
    path='/contact/',
    title='Contact Meem Obaidullah | Start Your Investment Scope',
    desc='Get in touch with Meem Obaidullah for Amazon FBA, Walmart WFS, and multi-channel e-commerce automation. '
         'WhatsApp, email, and secure contact form.',
    intro="Detail your target portfolio parameters, marketplace preferences and investment scope below — it goes "
          "straight to my inbox and I'll respond directly.",
    cards=[
        ('mail', 'Email', '<a href="mailto:meemobaidullah@gmail.com">meemobaidullah@gmail.com</a>'),
        ('phone', 'BD Operations', '<a href="tel:+8801731558195">+880 173 155 8195</a>'),
        # The live page shows "+1 315 581 95" for USA routing, which is missing digits.
        # Left out until the full number is confirmed.
    ],
)

# ---------------------------------------------------------------- blog / case studies / success
def stub_name(slug):
    """Live stub pages title-case the slug word by word: 'ai-in-ecommerce' -> 'Ai In Ecommerce'."""
    return ' '.join(w.capitalize() for w in slug.split('-'))


HUBS = {
    'blog': dict(
        path='/blog/', label='Blog', h1='Blog', eyebrow='Notes',
        title='Blog | Meem Obaidullah',
        desc="Blog from Meem Obaidullah — Notes on e-commerce operations, marketplace growth and store automation — published as they're written.",
        lead="Notes on e-commerce operations, marketplace growth and store automation — published as they're written.",
        section_lc="blog", stub_line="Content will go live here once it's written with real details.",
        items=['ai-in-ecommerce', 'ai-search-optimization', 'amazon-seo-tips', 'cloudflare-setup', 'competitor-analysis',
               'content-marketing-for-ecommerce', 'core-web-vitals-checklist', 'cross-platform-selling',
               'google-search-console-guide', 'google-shopping-ads', 'image-seo-tips', 'influencer-marketing-seo',
               'keyword-research-strategy', 'local-seo-for-sellers', 'mercari-selling-hacks', 'seo-audit-checklist',
               'shopify-seo-basics', 'temu-marketplace-guide', 'tiktok-shop-success', 'walmart-marketplace-growth'],
    ),
    'case-stady': dict(
        path='/case-stady/', label='Case Studies', h1='Case Studies', eyebrow='Track Record',
        title='Case Studies | Meem Obaidullah',
        desc='Case Studies from Meem Obaidullah — Documented store results and reopen work. Each case study is published only once real client data and permission are in place.',
        lead='Documented store results and reopen work. Each case study is published only once real client data and permission are in place.',
        section_lc='case studies', stub_line="Content will go live here once it's written with real client results and data.",
        items=['amazon-success-story', 'walmart-growth-case', 'tiktok-shop-case', 'temu-breakthrough', 'mercari-case',
               'shopify-case', 'amazon-ranking-4-months', 'walmart-traffic-doubling', 'tiktok-viral-campaign',
               'shopify-traffic-growth'],
    ),
    'sucess': dict(
        path='/sucess/', label='Success & News', h1='Success & News', eyebrow='Milestones',
        title='Success & News | Meem Obaidullah',
        desc='Success & News from Meem Obaidullah — Recognition, partnerships and milestones from across the business — updated as they happen.',
        lead='Recognition, partnerships and milestones from across the business — updated as they happen.',
        section_lc='success & news', stub_line="Content will go live here once it's written with real details.",
        items=['award-recognition', 'client-milestones', 'media-mentions', 'new-service-launch', 'partnership-news',
               'press-coverage', 'industry-recognition', 'community-impact', 'seo-awards', 'global-expansion'],
    ),
}


def stub_meta(key, slug):
    h = HUBS[key]
    name = stub_name(slug)
    return dict(path='/%s/%s/' % (key, slug), robots='noindex, follow',
                title='%s | %s | Meem Obaidullah' % (name, h['label']),
                desc="%s — coming soon on Meem Obaidullah's %s." % (name, h['section_lc']))


ARTICLE = dict(
    path='/blog/amazon-fba-complete-guide/', h1='Amazon FBA Complete Guide', og_image='/assets/images/meemobaidullah.webp',
    title='Amazon FBA Complete Guide (2026) | Meem Obaidullah',
    # TODO: replace with the exact live meta description from the original file before building the article
    desc='A complete, practical guide to Amazon FBA: how it works, FBA vs FBM, real cost categories and getting started steps.',
)

# Live sitemap, same order and lastmod
SITEMAP = [(p, '2026-08-16') for p in (
    ['/', '/about/', '/blog/'] + ['/blog/%s/' % s for s in sorted(HUBS['blog']['items'])] +
    ['/case-stady/'] + ['/case-stady/%s/' % s for s in sorted(HUBS['case-stady']['items'])] +
    ['/contact/', '/ebay-automation-services/', '/etsy-store-automation-services/', '/fba-automation/',
     '/mercari-seller/', '/shopify-automation/', '/sucess/'] +
    ['/sucess/%s/' % s for s in sorted(HUBS['sucess']['items'])] +
    ['/temu-store-management-services/', '/tiktok-shop-automation-services/', '/walmart-automation/']
)] + [('/blog/amazon-fba-complete-guide/', '2026-08-17')]
