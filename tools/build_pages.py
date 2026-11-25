# Generates the content pages (foundation, learn, verticals). Run: python3 tools/build_pages.py
# Edit copy here, then re-run. Pages are plain static HTML.
import json, os, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from proof import row as proof_row
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORG = {"@type": "LocalBusiness", "@id": "https://avewater.org/#business", "name": "Áve Water", "legalName": "Áve Water LLC",
       "url": "https://avewater.org/", "telephone": "+1-619-513-3367", "email": "ave@avewater.org",
       "logo": "https://avewater.org/assets/logo.png", "priceRange": "$$",
       "sameAs": ["https://www.instagram.com/ave.water", "https://www.linkedin.com/company/avewater/", "https://www.xn--ve-lia.com/", "https://share.google/eYlqAkfm1QxrIfZm2"]}
PHONE = '<a href="tel:+16195133367">(619) 513-3367</a>'
RELATED = '<div class="verticals"><a href="/events/">Events</a><a href="/retail/">Retail</a><a href="/hotels/">Hotels</a><a href="/fitness/">Fitness studios</a><a href="/weddings/">Weddings</a><a href="/corporate-events/">Corporate events</a><a href="/infused-water-station-san-diego/">San Diego</a><a href="/orange-county/">Orange County</a><a href="/hydration-station/">Hydration station</a><a href="/non-alcoholic-drink-catering/">Non-alcoholic drinks</a><a href="/employee-appreciation/">Employee appreciation</a><a href="/showers/">Showers</a></div>'
AREA = "Serving Southern California, from San Diego to Santa Barbara."

FAQ = [
 ("How much does an infused water station cost in Southern California?",
  "The Áve Venue Package is $350 and includes four gallons of fresh fruit infused water, 25 16oz bottles, setup and pickup. Bookings in Los Angeles, Ventura and Santa Barbara counties may include a travel fee, shown before you pay.",
  "Bigger events or a custom setup start with a 15-minute consultation, and we size the order with you."),
 ("How many people does four gallons of infused water serve?",
  "Four gallons is 512 ounces, about 64 eight-ounce cups. With the 25 bottles in the package, that is roughly 90 servings.",
  "Hot days, long events and fitness crowds drink more. If you expect more than about 90 guests, book a consultation and we will plan for it."),
 ("What is dwell time and how do you increase it?",
  "Dwell time is how long a visitor stays in your space. You increase it by giving people a reason to pause: something to taste, something to choose and a moment that feels made for them.",
  "Áve does this with cold fruit infused water and a QR code that lets guests vote on the music. At one 4-hour activation at Hammitt La Jolla, walk-by shoppers came into the store and the day led to $700+ in store sales."),
 ("How do I book infused water for an event?",
  "Go to avewater.org/book, check your zip, choose up to two flavors, add your venue details and pick a date and time. You pay on Stripe's secure checkout and get a confirmation right away.",
  "Bookings need 48 hours notice, or 72 hours in Los Angeles, Ventura and Santa Barbara counties. For anything sooner, email ave@avewater.org."),
 ("What is experiential marketing for retail?",
  "Experiential marketing for retail is giving shoppers something to do, taste or feel in your store, not just something to buy. It turns a walk-by into a visit and a visit into a memory of your brand.",
  "An Áve station is one simple version: a cold cup of fresh fruit infused water and a song the guest picked, inside your space, with setup and pickup handled by us."),
]

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="https://avewater.org{path}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="https://avewater.org{path}" />
  <meta name="robots" content="index, follow" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' fill='%23F5F0E8'/><text y='.9em' font-size='90' fill='%238B7355'>Á</text></svg>" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+SC:wght@300;400;500&family=Cormorant+Garamond:ital,wght@0,300;1,300&family=Montserrat:wght@300;400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/book/book.css" />
  <link rel="stylesheet" href="/assets/site.css" />
  <style>
    .content {{ max-width: 760px; margin: 0 auto; padding: 44px 20px 72px; }}
    .content h2 {{ font-size: 26px; margin: 40px 0 10px; }}
    .content p, .content li {{ font-size: 15px; color: var(--ink-2); line-height: 1.75; }}
    .content p + p {{ margin-top: 12px; }}
    .content ul {{ padding-left: 20px; margin-top: 8px; }}
    .answer {{ border-top: 0.5px solid var(--line); padding: 26px 0 6px; }}
    .answer h2 {{ margin-top: 0; font-size: 23px; }}
    .answer .lead {{ color: var(--ink); font-weight: 400; }}
    .cta-row {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 26px 0 8px; }}
    .poured {{ font-family: 'Cormorant SC', serif; font-size: 19px; color: var(--ink); letter-spacing: 0.03em; }}
    .verticals {{ display: flex; flex-wrap: wrap; gap: 8px 18px; margin-top: 10px; }}
    .verticals a {{ min-height: 44px; display: inline-flex; align-items: center; }}
  </style>
  <script type="application/ld+json">{ld}</script>
</head>
<body>
  <header class="top">
    <a class="brand" href="/" aria-label="Áve home">Áve</a>
    <a class="top-link" href="/book/">Book</a>
  </header>
  <main class="content">
'''
FOOT = '''  </main>
  <footer class="foot">© 2026 Áve Water LLC · {area}<br><a href="tel:+16195133367">(619) 513-3367</a> · <a href="mailto:ave@avewater.org">ave@avewater.org</a> · <a href="https://www.instagram.com/ave.water" target="_blank" rel="noopener">Instagram</a> · <a href="https://www.linkedin.com/company/avewater/" target="_blank" rel="noopener">LinkedIn</a> · <a href="/learn/">Learn</a> · <a href="/terms/">Legal</a></footer>
  <script src="/book/book.js"></script>
  <script src="/assets/site.js"></script>
  <script>
    document.querySelectorAll('[data-track]').forEach(function (a) {{
      a.addEventListener('click', function () {{ window.AveSite.track(a.getAttribute('data-track'), {{ page: location.pathname }}); }});
    }});
    var rv = document.getElementById('page-reviews'); if (rv) window.AveSite.reviews(rv);
  </script>
</body>
</html>
'''

def page(path, title, desc, body, ld):
    out = HEAD.format(title=html.escape(title), desc=html.escape(desc), path=path, ld=json.dumps(ld, ensure_ascii=False)) + body + FOOT.format(area=AREA)
    d = os.path.join(ROOT, path.strip('/'))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(out)

def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a + " " + b}} for q, a, b in items]}

BOOK_BTN = '<a class="btn btn-gold" href="/book/" data-track="vertical_book_click">Book your date</a>'

# ── /learn ────────────────────────────────────────────────────────
body = '''    <div class="eyebrow">Learn</div>
    <h1>Infused water for venues, answered.</h1>
    <p class="lede" style="margin-bottom:28px;">Straight answers about cost, servings, booking and why a cold cup keeps people in your space.</p>
''' + ''.join(f'''    <section class="answer" id="q{i+1}">
      <h2>{html.escape(q)}</h2>
      <p class="lead">{html.escape(a)}</p>
      <p>{html.escape(b)}</p>
    </section>
''' for i, (q, a, b) in enumerate(FAQ)) + f'''    <div class="cta-row">{BOOK_BTN}<a class="btn btn-ghost" href="/book/#step-zip">Check your zip</a></div>
    <h2>Áve for your kind of space</h2>
    ''' + RELATED + '''
'''
page('/learn/', 'Infused Water Stations: Cost, Servings and Booking | Áve Water',
     'How much an infused water station costs in Southern California, how many people four gallons serves, how to book and how to increase dwell time.',
     body, [faq_ld(FAQ), {"@context": "https://schema.org", **ORG}])

# ── Verticals ─────────────────────────────────────────────────────
V = {
 'events': dict(
   title='Infused Water Station for Events in Southern California | Áve Water',
   desc='Fresh fruit infused water for corporate events, launches and community gatherings, San Diego to Santa Barbara. Setup and pickup included, from $350.',
   media=['cultura-crowd', 'cultura-stage'],
   eyebrow='Events', h1='Cold water your guests remember.',
   lede='A fresh fruit infused water station for corporate events, brand launches and community gatherings.',
   paras=['We arrive before your start time, set up the station and pour four gallons of fresh fruit infused water with 25 bottles to take along. When the event ends, we pick everything up.',
          'Looking for a drink station or beverage station rental? Ours arrives with everything: the dispensers, the water, the flavors and a person to set it up.',
          'Guests scan a QR code by the water and vote on the next song from their phone, so the room keeps moving with them.'],
   points=['Corporate events and team days', 'Brand launches and pop-ups', 'Community and cultural events', 'Weddings and private celebrations, with a consultation for larger counts'],
   faq=[0, 1, 3]),
 'retail': dict(
   title='In-Store Experience for Retail: Infused Water and Music | Áve Water',
   desc='Give shoppers a reason to stay. Fresh fruit infused water and guest-voted music in your store, San Diego to Santa Barbara. From $350.',
   media=['afternoon', 'boardwalk-guest'],
   eyebrow='Retail', h1='A reason to come in, and a reason to stay.',
   lede='Fresh fruit infused water and a song your shopper chose, poured inside your store.',
   paras=['A cold cup at the door turns a walk-by into a visit. At one 4-hour activation at Hammitt La Jolla, walk-by shoppers came into the store and the day led to $700+ in store sales.',
          'Guests vote on the music from their phone, and we share what we learn about their visit with you.'],
   points=['Store events and trunk shows', 'New collection launches', 'Weekend foot traffic', 'Holiday shopping days'],
   faq=[2, 4, 0]),
 'hotels': dict(
   title='Lobby and Pool Infused Water Station for Hotels | Áve Water',
   desc='A fresh fruit infused water station for hotel lobbies, pools and events, San Diego to Santa Barbara. Setup and pickup included, from $350.',
   media=['flavor-watermelon-basil-wide', 'boardwalk-music'],
   eyebrow='Hotels', h1='The welcome your guests mention later.',
   lede='Fresh fruit infused water for lobbies, pool decks and hotel events.',
   paras=['Watermelon Basil at check-in. Cucumber Mint by the pool. We set up, pour and pick up, so your team stays with your guests.',
          'A QR code by the water lets guests choose the music, and you see what they reached for.'],
   points=['Lobby welcome on busy weekends', 'Pool and cabana days', 'Group arrivals and conferences', 'Hotel events and weddings, with a consultation for larger counts'],
   faq=[0, 1, 3]),
 'fitness': dict(
   title='Infused Water Station for Gyms and Fitness Studios | Áve Water',
   desc='Fresh fruit infused water and member-voted music for gyms, studios and fitness events, San Diego to Santa Barbara. From $350.',
   media=['flavor-citrus-ginger-wide', 'boardwalk-guest'],
   eyebrow='Fitness studios', h1='Cold, ripe, after the last set.',
   lede='Fresh fruit infused water and member-voted music for studios, gyms and fitness events.',
   paras=['Citrus Ginger before class, Cucumber Mint after. We set up the station, pour four gallons with 25 bottles and pick everything up when you are done.',
          'Members scan a QR code and vote on the music, and you see the moods they choose.'],
   points=['Member appreciation days', 'Open houses and new member events', 'Community classes and challenges', 'Studio launches'],
   faq=[1, 0, 3]),
 'infused-water-station-san-diego': dict(
   title='Infused Water Station Rental in San Diego | Áve Water',
   desc='Book a fresh fruit infused water station in San Diego, from La Jolla to Chula Vista and North County. 4 gallons, 25 bottles, setup and pickup, from $350.',
   media=['folklorico-sign', 'cultura-stage'],
   eyebrow='San Diego', h1='Infused water stations across San Diego.',
   lede='Fresh fruit infused water for venues and events, set up and picked up by our team.',
   paras=['Áve started in San Diego, and most of our pop-ups happen here: La Jolla, Pacific Beach, Downtown, North Park, Del Mar, Carlsbad, Encinitas, San Marcos, Escondido, Oceanside, Chula Vista and El Cajon.',
          'Book online with 48 hours notice. Check your zip on the booking page, pick a date and up to two flavors, and pay securely. Guests vote on the music from their phone while they drink.'],
   points=['Store events and launches', 'Corporate and team events', 'Community and cultural events', 'Hotels, pools and private parties'],
   faq=[0, 1, 3]),
 'orange-county': dict(
   title='Infused Water Station Rental in Orange County | Áve Water',
   desc='Fresh fruit infused water stations for Orange County venues and events: Irvine, Newport Beach, Costa Mesa, Huntington Beach, Laguna Beach and more. From $350.',
   media=['boardwalk-guest', 'cultura-crowd'],
   eyebrow='Orange County', h1='Infused water stations in Orange County.',
   lede='Fresh fruit infused water and guest-voted music, set up and picked up by our team.',
   paras=['We serve Irvine, Newport Beach, Costa Mesa, Huntington Beach, Laguna Beach, Anaheim, Tustin, San Clemente and the rest of Orange County.',
          'Book online with 48 hours notice. No travel fee in Orange County. Guests scan a QR code by the water and vote on the next song from their phone.'],
   points=['Store events and launches', 'Corporate and team events', 'Studio and gym events', 'Weddings and private parties, with a consultation for larger counts'],
   faq=[0, 3, 1]),
 'weddings': dict(
   title='Infused Water Station for Weddings in San Diego and Orange County | Áve Water',
   desc='A non-alcoholic drink station for your ceremony, cocktail hour or reception, made for dry and sober weddings too. Fresh fruit infused water, from $350.',
   media=['flavor-watermelon-basil-wide', 'folklorico-sign'],
   eyebrow='Weddings', h1='Cold water, poured beautifully, on your day.',
   lede='A fresh fruit infused water station for your ceremony, cocktail hour or reception.',
   paras=['Your guests arrive to Hibiscus Rose or Watermelon Basil served in glass, set up before the first guest and picked up after the last. Your planner has one less thing to manage.',
          'Planning a dry or sober wedding? Áve gives every guest something beautiful to hold that is not a cocktail, and it sits just as well beside a bar if you have one.',
          'Guests can vote on the music from their phone, and everyone leaves with a personalized playlist from the day.'],
   points=['Ceremonies, especially outdoors', 'Cocktail hour', 'Receptions and after parties', 'Rehearsal dinners and welcome parties'],
   faq=[1, 0, 3]),
 'corporate-events': dict(
   title='Corporate Event Drink Station: Infused Water and Music | Áve Water',
   desc='A fresh fruit infused water station for corporate events, offsites, conferences and office days in Southern California. Setup and pickup included, from $350.',
   media=['cultura-stage', 'cultura-sponsor-wall'],
   eyebrow='Corporate events', h1='The detail your team talks about after.',
   lede='Fresh fruit infused water and guest-voted music for office days, offsites and conferences.',
   paras=['We set up before your start time, pour four gallons of fresh fruit infused water with 25 bottles to take along, and pick up when you wrap. On stage, we can set a bottle at every speaker chair.',
          'Attendees vote on the music from their phone, and you see the moods your team chose.'],
   points=['Office days and team celebrations', 'Corporate wellness days', 'Offsites and retreats', 'Conferences, panels and expos', 'Client events and product launches'],
   faq=[0, 3, 1]),
 'hydration-station': dict(
   title='Hydration Station Rental for Events, Offices and Weddings | Áve Water',
   desc='Rent a hydration station for your event, office or wedding in Southern California. Fresh fruit infused water, glass dispensers, setup and pickup, from $350.',
   media=['cultura-stage', 'boardwalk-guest'],
   eyebrow='Hydration station', h1='A hydration station people actually stop at.',
   lede='Fresh fruit infused water in glass dispensers, set up and picked up by our team.',
   paras=['A plain water cooler gets ignored. Ours has Watermelon Basil, Citrus Ginger, Hibiscus Rose or Cucumber Mint, poured in glass, with 25 bottles to take along.',
          'Use it at the registration table, by the stage, at the finish line or next to the dance floor. Guests scan a QR code by the water and vote on the next song.'],
   points=['Conferences, expos and registration tables', 'Office days and team events', 'Weddings and outdoor ceremonies', 'Races, tournaments and community events'],
   faq=[1, 0, 3]),
 'employee-appreciation': dict(
   title='Employee Appreciation Idea: Infused Water and Music Pop-Up | Áve Water',
   desc='An employee appreciation idea your team will notice: a fresh fruit infused water pop-up with music they choose. Set up at your office, from $350.',
   media=['boardwalk-music', 'cultura-stage'],
   eyebrow='Employee appreciation', h1='A thank you your team will actually notice.',
   lede='A fresh fruit infused water pop-up in your office, with music your team chooses.',
   paras=['We set up in your break room, lobby or patio, pour four gallons of fresh fruit infused water with 25 bottles to take back to desks, and pick everything up when the day is done.',
          'Your team scans a QR code and votes on what plays next. It turns an ordinary afternoon into a small event, with no planning on your side.'],
   points=['Employee appreciation days and weeks', 'Team milestones and wins', 'Summer Fridays and office events', 'New office openings and move-ins'],
   faq=[0, 3, 1]),
 'non-alcoholic-drink-catering': dict(
   title='Non-Alcoholic Drink Catering in San Diego and Orange County | Áve Water',
   desc='Non-alcoholic drink catering for weddings, parties and corporate events. Fresh fruit infused water in four flavors, set up and picked up, from $350.',
   media=['folklorico-sign', 'flavor-watermelon-basil-wide'],
   eyebrow='Non-alcoholic drinks', h1='Non-alcoholic, and still the drink people talk about.',
   lede='Fresh fruit infused water for weddings, parties and corporate events.',
   paras=['Watermelon Basil, Citrus Ginger, Hibiscus Rose and Cucumber Mint, made with whole fruit and fresh herbs and served in glass. Choose up to two for your event.',
          'It works as the main drink at a dry event, or beside the bar so every guest has something good to hold. Guests vote on the music from their phone while they drink.'],
   points=['Dry and sober weddings', 'Corporate events and conferences', 'Quinceañeras, birthdays and family parties', 'Community and cultural events'],
   faq=[0, 1, 3]),
 'showers': dict(
   title='Baby Shower and Bridal Shower Drink Station | Áve Water',
   desc='A fresh fruit infused water drink station for baby showers and bridal showers in San Diego and Orange County. Set up and picked up, from $350.',
   media=['flavor-watermelon-basil-wide', 'flavor-citrus-ginger-wide'],
   eyebrow='Showers', h1='The drink station your shower photos need.',
   lede='Fresh fruit infused water for baby showers and bridal showers.',
   paras=['Hibiscus Rose for a bridal shower, Watermelon Basil for a summer baby shower. Served in glass dispensers with fruit and herbs you can see, so the table looks as good as it tastes.',
          'We set up before guests arrive and pick up after, so the host gets to enjoy the party.'],
   points=['Baby showers and sip and sees', 'Bridal showers and brunches', 'Gender reveals and birthdays', 'Engagement parties'],
   faq=[1, 0, 3]),
}
for slug, v in V.items():
    items = [FAQ[i] for i in v['faq']]
    body = f'''    <div class="eyebrow">{v['eyebrow']}</div>
    <h1>{html.escape(v['h1'])}</h1>
    <p class="lede" style="margin-bottom:22px;">{html.escape(v['lede'])}</p>
''' + ''.join(f'    <p>{html.escape(p)}</p>\n' for p in v['paras']) + proof_row(v['media']) + f'''    <div class="cta-row">{BOOK_BTN}<a class="btn btn-ghost" href="/learn/">Questions</a></div>
    <h2>The Áve Venue Package</h2>
    <ul>
      <li>4 gallons of fresh fruit infused water</li>
      <li>25 16oz bottles</li>
      <li>Up to two flavors: Watermelon Basil, Citrus Ginger, Hibiscus Rose, Cucumber Mint</li>
      <li>Setup and pickup included, from $350</li>
    </ul>
    <h2>Made for</h2>
    <ul>
''' + ''.join(f'      <li>{html.escape(x)}</li>\n' for x in v['points']) + f'''    </ul>
    <h2>Poured at</h2>
    <p class="poured">Hammitt La Jolla · MANA de North County · Ballet Folklórico San Diego · La Jolla Cove</p>
    <div class="ave-reviews" id="page-reviews" hidden style="margin-top:36px;"></div>
    <h2>More ways to book Áve</h2>
    ''' + RELATED.replace(f'<a href="/{slug}/">', '<a aria-current="page" href="/' + slug + '/">') + '''
''' + ''.join(f'''    <section class="answer">
      <h2>{html.escape(q)}</h2>
      <p class="lead">{html.escape(a)}</p>
      <p>{html.escape(b)}</p>
    </section>
''' for q, a, b in items) + f'''    <div class="cta-row">{BOOK_BTN}</div>
    <p class="hint">{AREA}</p>
'''
    ld = [{"@context": "https://schema.org", "@type": "Service", "name": f"Áve Venue Package, {v['eyebrow']}",
           "serviceType": "Infused water station", "provider": ORG,
           "description": "4 gallons of fresh fruit infused water and 25 16oz bottles, setup and pickup included",
           "areaServed": ["San Diego County, CA", "Orange County, CA", "Los Angeles County, CA", "Ventura County, CA", "Santa Barbara County, CA"],
           "offers": {"@type": "Offer", "price": "350", "priceCurrency": "USD", "url": "https://avewater.org/book/"}},
          faq_ld(items)]
    page(f'/{slug}/', v['title'], v['desc'], body, ld)

# ── /foundation (Caregiver voice) ─────────────────────────────────
# The partner line (charitable support) is held until Sid approves it.
body = '''    <div class="eyebrow">Áve Foundation</div>
    <h1>Beyond the cup.</h1>
    <p class="lede" style="margin-bottom:22px;">The Áve Foundation looks after the community that shows up.</p>
    <p>We bring hydration, wellness and music programs to neighborhoods, universities and families. Clean, cold water and a few minutes of music, offered to everyone who comes.</p>
    <p>Venue partners help fund every program. The Foundation is forming as a 501(c)(3).</p>
''' + proof_row(['cultura-crowd', 'folklorico-sign']) + '''    <h2>Who we look after</h2>
    <ul>
      <li><strong>Neighborhoods.</strong> Water, wellness and music at community events, open to all.</li>
      <li><strong>Universities.</strong> Campus partnerships and student-led activations that care for students between classes and games.</li>
      <li><strong>Families.</strong> Programs where kids and parents can slow down together.</li>
    </ul>
    <h2>Work with us</h2>
    <p>Community groups, schools and venue partners can write to <a href="mailto:ave@avewater.org">ave@avewater.org</a>.</p>
    <div class="cta-row"><a class="btn btn-gold" href="mailto:ave@avewater.org?subject=%C3%81ve%20Foundation">Write to us</a><a class="btn btn-ghost" href="/book/">Book Áve for your venue</a></div>
'''
page('/foundation/', 'Áve Foundation | Community Hydration and Wellness, San Diego',
     'The Áve Foundation brings hydration, wellness and music programs to San Diego neighborhoods and universities. 501(c)(3) status in formation.',
     body, {"@context": "https://schema.org", "@type": "Organization", "name": "Áve Foundation",
            "url": "https://avewater.org/foundation/", "parentOrganization": ORG,
            "description": "Hydration, wellness and music programs for San Diego neighborhoods and universities. 501(c)(3) status in formation."})
print('ok')
