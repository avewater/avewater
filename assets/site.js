// Áve shared components for avewater.org.
//   AveSite.reviews(el)          guest review carousel (Airtable OS Reviews via the API)
//   AveSite.playlistPopup(opts)  free Áve Playlist pop-up, once per session
//   AveSite.track(event, props)  analytics events into window.dataLayer
(function () {
  var API = 'https://www.xn--ve-lia.com';
  try {
    var qp = new URLSearchParams(location.search).get('api');
    if (qp && /^(localhost|127\.0\.0\.1)$/.test(location.hostname)) API = qp;
  } catch (e) {}
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  window.dataLayer = window.dataLayer || [];
  function track(event, props) {
    window.dataLayer.push(Object.assign({ event: event }, props || {}));
    if (typeof window.gtag === 'function') window.gtag('event', event, props || {});
    if (typeof window.plausible === 'function') window.plausible(event, { props: props || {} });
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; });
  }

  // ── Review carousel ────────────────────────────────────────────────
  function reviews(root) {
    if (!root) return;
    root.hidden = true;
    fetch(API + '/api/reviews').then(function (r) { return r.json(); }).then(function (d) {
      var items = (d && d.reviews) || [];
      if (!items.length) return;
      root.hidden = false;
      var n = items.length, i = 0, timer = null, paused = false;
      root.setAttribute('role', 'region');
      root.setAttribute('aria-roledescription', 'carousel');
      root.setAttribute('aria-label', 'Guest reviews');
      root.innerHTML =
        '<div class="rv-eyebrow">What guests say</div>' +
        '<div class="rv-viewport"><div class="rv-track" aria-live="off">' +
        items.map(function (it, k) {
          return '<div class="rv-slide" role="group" aria-roledescription="slide" aria-label="' + (k + 1) + ' of ' + n + '"' + (k ? ' aria-hidden="true"' : '') + '>' +
            '<blockquote>“' + esc(it.quote) + '”</blockquote><div class="rv-attr">' + esc(it.attribution) + '</div></div>';
        }).join('') +
        '</div></div>' +
        '<div class="rv-controls">' +
          '<button type="button" class="rv-btn rv-prev" aria-label="Previous review">‹</button>' +
          '<div class="rv-dots">' + items.map(function (_, k) { return '<button type="button" class="rv-dot" aria-label="Show review ' + (k + 1) + ' of ' + n + '"' + (k ? '' : ' aria-current="true"') + '></button>'; }).join('') + '</div>' +
          '<span class="rv-pos" aria-hidden="true">1 / ' + n + '</span>' +
          '<button type="button" class="rv-btn rv-next" aria-label="Next review">›</button>' +
        '</div>';
      var track = root.querySelector('.rv-track');
      var slides = root.querySelectorAll('.rv-slide');
      var dots = root.querySelectorAll('.rv-dot');
      var pos = root.querySelector('.rv-pos');
      if (n < 2) root.querySelector('.rv-controls').hidden = true;
      function go(k) {
        i = (k + n) % n;
        track.style.transform = 'translateX(' + (-100 * i) + '%)';
        for (var j = 0; j < n; j++) {
          slides[j].setAttribute('aria-hidden', j === i ? 'false' : 'true');
          if (j === i) dots[j].setAttribute('aria-current', 'true'); else dots[j].removeAttribute('aria-current');
        }
        pos.textContent = (i + 1) + ' / ' + n;
      }
      function start() { if (reduceMotion || n < 2) return; stop(); timer = setInterval(function () { if (!paused && !document.hidden) go(i + 1); }, 7000); }
      function stop() { if (timer) clearInterval(timer); timer = null; }
      root.querySelector('.rv-prev').addEventListener('click', function () { go(i - 1); });
      root.querySelector('.rv-next').addEventListener('click', function () { go(i + 1); });
      Array.prototype.forEach.call(dots, function (dt, k) { dt.addEventListener('click', function () { go(k); }); });
      root.addEventListener('mouseenter', function () { paused = true; });
      root.addEventListener('mouseleave', function () { paused = false; });
      root.addEventListener('focusin', function () { paused = true; });
      root.addEventListener('focusout', function (e) { if (!root.contains(e.relatedTarget)) paused = false; });
      root.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft') { go(i - 1); e.preventDefault(); }
        if (e.key === 'ArrowRight') { go(i + 1); e.preventDefault(); }
      });
      var x0 = null;
      root.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; paused = true; }, { passive: true });
      root.addEventListener('touchend', function (e) {
        if (x0 != null) { var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) go(i + (dx < 0 ? 1 : -1)); }
        x0 = null; paused = false;
      });
      start();
    }).catch(function () {});
  }

  // ── Playlist pop-up ────────────────────────────────────────────────
  var PP_KEY = 'ave_playlist_popup';
  var BUILD_URL = '/redeem/';
  var COPY = {
    venue: { body: 'Build the mood for your experience. Your guests can vote on the music they want to hear as they move through your venue.' },
    home: { body: 'Pick a mood and we build it in about a minute.' },
  };
  function ppDone() { try { return !!sessionStorage.getItem(PP_KEY); } catch (e) { return false; } }
  function ppMark(v) { try { sessionStorage.setItem(PP_KEY, v); } catch (e) {} }

  // opts: { variant: 'home'|'venue', trigger: string, phone?: '6195551234', returnFocus?: Element }
  function playlistPopup(opts) {
    opts = opts || {};
    if (ppDone() || document.querySelector('.ave-pp-backdrop')) return;
    ppMark('shown');
    var variant = opts.variant === 'venue' ? 'venue' : 'home';
    var opener = opts.returnFocus || document.activeElement;
    track('playlist_popup_shown', { trigger: opts.trigger || '', variant: variant });

    var wrap = document.createElement('div');
    wrap.className = 'ave-pp-backdrop';
    wrap.innerHTML =
      '<div class="ave-pp" role="dialog" aria-modal="true" aria-labelledby="pp-title" aria-describedby="pp-body">' +
        '<button type="button" class="pp-close" aria-label="Close">×</button>' +
        '<div class="pp-eyebrow">A gift from Áve</div>' +
        '<h2 id="pp-title">Your free Áve Playlist</h2>' +
        '<p id="pp-body">' + esc(COPY[variant].body) + '</p>' +
        '<p class="pp-note">Takes about a minute.</p>' +
        '<div class="pp-actions">' +
          '<a class="pp-btn pp-primary" href="' + BUILD_URL + '">Build my playlist</a>' +
          '<button type="button" class="pp-btn pp-secondary pp-show-text">Text me the link</button>' +
        '</div>' +
        '<form class="pp-text" hidden novalidate>' +
          '<label for="pp-phone">Mobile number</label>' +
          '<input type="tel" id="pp-phone" inputmode="tel" autocomplete="tel-national" placeholder="(619) 000-0000" />' +
          '<p class="pp-consent">By tapping Send, you agree to receive SMS messages from Áve Water LLC delivering your playlist link. Up to 2 messages. Message and data rates may apply. Reply STOP to opt out, HELP for help. Consent is not a condition of purchase.</p>' +
          '<button type="submit" class="pp-btn pp-primary">Send</button>' +
          '<div class="pp-status" role="status" aria-live="polite"></div>' +
        '</form>' +
        '<p style="font-size:11px;margin:16px 0 0;color:#6B6258;">Playlists save to Spotify. Apple Music coming soon.</p>' +
      '</div>';
    document.body.appendChild(wrap);
    var dialog = wrap.querySelector('.ave-pp');
    var prevOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    requestAnimationFrame(function () { wrap.classList.add('open'); });

    function focusables() {
      return Array.prototype.filter.call(dialog.querySelectorAll('a[href], button, input, [tabindex]:not([tabindex="-1"])'), function (el) {
        return !el.disabled && el.offsetParent !== null;
      });
    }
    function close(reason) {
      if (reason !== 'claimed' && reason !== 'texted') track('playlist_popup_closed', { variant: variant });
      ppMark(reason || 'closed');
      document.removeEventListener('keydown', onKey, true);
      document.body.style.overflow = prevOverflow;
      wrap.remove();
      if (opener && opener.focus) opener.focus();
    }
    function onKey(e) {
      if (e.key === 'Escape') { e.preventDefault(); close('closed'); return; }
      if (e.key !== 'Tab') return;
      var f = focusables(); if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { last.focus(); e.preventDefault(); }
      else if (!e.shiftKey && document.activeElement === last) { first.focus(); e.preventDefault(); }
    }
    document.addEventListener('keydown', onKey, true);
    wrap.addEventListener('mousedown', function (e) { if (e.target === wrap) close('closed'); });
    dialog.querySelector('.pp-close').addEventListener('click', function () { close('closed'); });
    dialog.querySelector('.pp-primary').addEventListener('click', function () {
      track('playlist_popup_claimed', { variant: variant });
      ppMark('claimed');
    });
    var form = dialog.querySelector('.pp-text');
    var phoneEl = dialog.querySelector('#pp-phone');
    if (opts.phone) phoneEl.value = opts.phone;
    dialog.querySelector('.pp-show-text').addEventListener('click', function () {
      form.hidden = false;
      this.hidden = true;
      phoneEl.focus();
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = form.querySelector('.pp-status');
      var digits = phoneEl.value.replace(/\D/g, '').replace(/^1(?=\d{10}$)/, '');
      if (digits.length !== 10) { status.className = 'pp-status err'; status.textContent = 'Enter a 10-digit mobile number.'; phoneEl.focus(); return; }
      var btn = form.querySelector('button[type=submit]');
      btn.disabled = true; status.className = 'pp-status'; status.textContent = 'Sending';
      fetch(API + '/api/auth/redeem', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone: '+1' + digits, trigger: 'direct' }),
      }).then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); }).then(function (res) {
        if (res.ok && res.d && res.d.success) {
          track('playlist_popup_text_link', { variant: variant });
          ppMark('texted');
          status.textContent = 'Sent. Check your texts.';
          setTimeout(function () { close('texted'); }, 1800);
        } else {
          btn.disabled = false; status.className = 'pp-status err';
          status.textContent = res.d && res.d.error === 'Too many requests' ? 'Please wait a minute and try again.' : 'Could not send right now. Try Build my playlist instead.';
        }
      }).catch(function () { btn.disabled = false; status.className = 'pp-status err'; status.textContent = 'Could not send right now. Try Build my playlist instead.'; });
    });
    setTimeout(function () { var f = focusables(); (f[1] || f[0]).focus(); }, 30);
  }

  window.AveSite = { API: API, track: track, reviews: reviews, playlistPopup: playlistPopup, esc: esc };
})();
