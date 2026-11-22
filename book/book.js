// Áve booking portal: shared helpers for /book pages.
(function () {
  var API = 'https://www.xn--ve-lia.com';
  // Local preview only: ?api=http://localhost:3000 points the page at a dev server.
  try {
    var qp = new URLSearchParams(location.search).get('api');
    if (qp && /^(localhost|127\.0\.0\.1)$/.test(location.hostname)) API = qp;
  } catch (e) {}

  // Analytics events go to window.dataLayer, which any tag manager or
  // analytics script added to the site can read (GA4, Plausible, etc.).
  window.dataLayer = window.dataLayer || [];
  function track(event, props) {
    var payload = Object.assign({ event: event }, props || {});
    window.dataLayer.push(payload);
    if (typeof window.plausible === 'function') window.plausible(event, { props: props || {} });
    if (typeof window.gtag === 'function') window.gtag('event', event, props || {});
  }

  function api(path, opts) {
    opts = opts || {};
    var init = { method: opts.method || 'GET', headers: {} };
    if (opts.body) { init.headers['Content-Type'] = 'application/json'; init.body = JSON.stringify(opts.body); }
    var ctrl = typeof AbortController !== 'undefined' ? new AbortController() : null;
    if (ctrl) init.signal = ctrl.signal;
    var timer = ctrl ? setTimeout(function () { ctrl.abort(); }, opts.timeout || 20000) : null;
    return fetch(API + path, init).then(function (res) {
      if (timer) clearTimeout(timer);
      return res.json().catch(function () { return {}; }).then(function (data) {
        data = data || {};
        data._status = res.status;
        data._ok = res.ok;
        return data;
      });
    }, function (err) {
      if (timer) clearTimeout(timer);
      return { _ok: false, _status: 0, _network: true, error: err && err.name === 'AbortError' ? 'This is taking longer than usual. Check your connection and try again.' : 'Could not reach Áve. Check your connection and try again.' };
    });
  }

  function money(n) {
    n = Number(n) || 0;
    return '$' + (n % 1 === 0 ? n.toFixed(0) : n.toFixed(2));
  }
  function prettyDate(d) {
    if (!d) return '';
    var p = d.split('-').map(Number);
    return new Date(Date.UTC(p[0], p[1] - 1, p[2], 12)).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' });
  }
  function prettyTime(t) {
    if (!t) return '';
    var p = t.split(':').map(Number);
    var ap = p[0] >= 12 ? 'pm' : 'am';
    var h = p[0] % 12 || 12;
    return p[1] ? h + ':' + String(p[1]).padStart(2, '0') + ' ' + ap : h + ' ' + ap;
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; });
  }

  window.Ave = { API: API, api: api, track: track, money: money, prettyDate: prettyDate, prettyTime: prettyTime, esc: esc };
})();
