# Real activation media used across avewater.org. One place for files, captions and alt text.
import html
M = '/assets/media/'
P = {
 'boardwalk-guest': dict(kind='video', shape='', alt='A guest holding an Áve bottle at a beach pop-up', cap='<strong>Beach pop-up</strong> · San Diego', note='A real guest, shared with permission.'),
 'boardwalk-music': dict(kind='video', shape='', alt='A guest scanning the QR code to pick the next song at an Áve pop-up', cap='<strong>Guests pick the music</strong> · San Diego', note='A real guest, shared with permission.'),
 'cultura-crowd': dict(kind='video', shape='tall', alt='A packed hall on its feet at We Are Cultura', cap='<strong>We Are Cultura</strong> · MANA de North County · San Marcos · Aug 2026'),
 'cultura-stage': dict(kind='video', shape='tall', alt='Áve bottles set under every speaker chair on the We Are Cultura stage', cap='<strong>On stage at We Are Cultura</strong> · San Marcos · Aug 2026'),
 'cultura-sponsor-wall': dict(kind='img', shape='', alt='The Áve logo on the We Are Cultura sponsor wall', cap='<strong>Sponsor wall, We Are Cultura</strong> · San Marcos · Aug 2026'),
 'folklorico-sign': dict(kind='video', shape='wide', alt='The Áve flavor menu sign with a painted hummingbird at Ballet Folklórico San Diego', cap='<strong>Ballet Folklórico San Diego</strong> · Sep 2026'),
 'afternoon': dict(kind='video', shape='tall', alt='An Áve afternoon at Hammitt La Jolla', cap='<strong>Hammitt La Jolla</strong>', note='AI-enhanced from photos of the day.'),
 'flavor-watermelon-basil-wide': dict(kind='img', shape='', alt='A glass bottle of Watermelon Basil infused water beside half a watermelon', cap='<strong>Watermelon Basil</strong>'),
 'flavor-citrus-ginger-wide': dict(kind='img', shape='', alt='A glass bottle of Citrus Ginger infused water beside grapefruit, lemon, lime and ginger', cap='<strong>Citrus Ginger</strong>'),
}

def fig(key, cls='', indent='    '):
    m = P[key]
    shape = (' ' + m['shape']) if m['shape'] else ''
    extra = (' ' + cls) if cls else ''
    alt = html.escape(m['alt'], quote=True)
    if m['kind'] == 'video':
        media = f'<video data-src="{M}{key}.mp4" poster="{M}{key}.jpg" muted loop playsinline preload="none" aria-label="{alt}"></video>'
    else:
        media = f'<img src="{M}{key}.jpg" alt="{alt}" loading="lazy" decoding="async" />'
    note = f'<span class="proof-note">{m["note"]}</span>' if m.get('note') else ''
    return f'{indent}<figure class="proof{shape}{extra}"><div class="proof-frame">{media}</div><figcaption>{m["cap"]}{note}</figcaption></figure>\n'

def row(keys, indent='    '):
    return f'{indent}<div class="proof-row" style="--n:{len(keys)}">\n' + ''.join(fig(k, indent=indent + '  ') for k in keys) + f'{indent}</div>\n'
