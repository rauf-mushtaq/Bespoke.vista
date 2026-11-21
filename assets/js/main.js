// Bespoke Vista — site behaviour. No third-party libraries.
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var params = new URLSearchParams(window.location.search);

  /* ---------- Analytics ----------
     Events go to dataLayer (Google Tag Manager), gtag (GA4) and Microsoft Clarity when those
     are installed (IDs are configured in build.py). Without them, tracking is a harmless no-op.
     Events: scorecard_start, scorecard_complete, result_download, result_email,
     assessment_view, sample_view, booking_start, assessment_enquiry_start, pilot_cta,
     pilot_enquiry_submit, contact_submit, scorecard_lead_submit, lead_submit.
     booking_completed must be configured inside Microsoft Bookings / Power Automate,
     because Bookings runs on Microsoft's site. */
  function track(name, data) {
    data = data || {};
    try { (window.dataLayer = window.dataLayer || []).push(Object.assign({ event: name }, data)); } catch (e) {}
    try { if (typeof window.gtag === 'function') window.gtag('event', name, data); } catch (e) {}
    try { if (typeof window.clarity === 'function') window.clarity('event', name); } catch (e) {}
  }
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-track]');
    if (el) track(el.getAttribute('data-track'), { href: el.getAttribute('href') || '' });
  });

  /* ---------- Cookie consent ----------
     Only active when GA4 or Clarity IDs are configured in build.py (window.BV_ANALYTICS).
     Nothing is loaded until the visitor accepts. The choice is kept in localStorage. */
  var cfg = window.BV_ANALYTICS, banner = $('.consent'), analyticsLoaded = false;
  function getConsent() { try { return localStorage.getItem('bv-consent'); } catch (e) { return null; } }
  function setConsent(v) { try { localStorage.setItem('bv-consent', v); } catch (e) {} }
  function loadAnalytics() {
    if (!cfg || analyticsLoaded) return;
    analyticsLoaded = true;
    if (cfg.ga4) {
      var g = document.createElement('script');
      g.async = true; g.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(cfg.ga4);
      document.head.appendChild(g);
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag('js', new Date()); window.gtag('config', cfg.ga4);
    }
    if (cfg.clarity) {
      (function (c, l, a, r, i, t, y) {
        c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
        t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
        y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
      })(window, document, 'clarity', 'script', encodeURIComponent(cfg.clarity));
    }
  }
  if (cfg && banner) {
    var choice = getConsent();
    if (choice === 'accept') loadAnalytics(); else if (!choice) banner.hidden = false;
    $$('[data-consent]').forEach(function (b) {
      b.addEventListener('click', function () {
        var v = b.getAttribute('data-consent');
        var wasLoaded = analyticsLoaded;
        setConsent(v); banner.hidden = true;
        if (v === 'accept') loadAnalytics();
        else if (wasLoaded) window.location.reload(); // stop analytics already running on this page
      });
    });
    $$('[data-consent-open]').forEach(function (b) { b.addEventListener('click', function () { banner.hidden = false; }); });
  }

  /* ---------- Mobile navigation ---------- */
  var toggle = $('.nav-toggle'), links = $('.nav-links');
  if (toggle && links) {
    var close = function () { links.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); };
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    links.addEventListener('click', function (e) { if (e.target.closest('a')) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && links.classList.contains('open')) { close(); toggle.focus(); } });
  }

  /* ---------- Sticky call to action on phones: shown after the hero, hidden near the footer ---------- */
  var sticky = $('.sticky-cta'), footer = $('.site-footer');
  if (sticky) {
    var onScroll = function () {
      var nearFooter = footer && footer.getBoundingClientRect().top < window.innerHeight;
      var consentOpen = banner && !banner.hidden;
      sticky.classList.toggle('show', window.scrollY > 600 && !nearFooter && !consentOpen);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  var year = $('#year');
  if (year) year.textContent = new Date().getFullYear();

  /* ---------- Reveal on scroll ---------- */
  var items = $$('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
    }, { threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else items.forEach(function (el) { el.classList.add('visible'); });

  /* ---------- Assessment offer viewed ---------- */
  var assess = $('#assessment');
  if (assess && 'IntersectionObserver' in window) {
    var seen = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) { track('assessment_view', { page: location.pathname }); seen.disconnect(); }
    }, { threshold: 0.5 });
    seen.observe(assess);
  }
  if (params.get('topic') === 'assessment') track('assessment_view', { page: 'contact' });

  /* ---------- Sticky jump bar: highlight the section in view ---------- */
  var subLinks = $$('.subnav a');
  if (subLinks.length && 'IntersectionObserver' in window) {
    var byId = {};
    subLinks.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        subLinks.forEach(function (a) { a.classList.remove('active'); a.removeAttribute('aria-current'); });
        var link = byId[e.target.id];
        if (link) {
          link.classList.add('active');
          link.setAttribute('aria-current', 'true');
          var bar = link.closest('ul');
          bar.scrollLeft = link.offsetLeft - (bar.clientWidth - link.offsetWidth) / 2;
        }
      });
    }, { rootMargin: '-35% 0px -60% 0px' });
    Object.keys(byId).forEach(function (id) { var el = document.getElementById(id); if (el) spy.observe(el); });
  }

  /* ---------- London and Lahore clocks; follow-the-sun timeline ---------- */
  function partsIn(tz) {
    var f = new Intl.DateTimeFormat('en-GB', { timeZone: tz, hour: '2-digit', minute: '2-digit', weekday: 'short', hour12: false });
    var out = {};
    f.formatToParts(new Date()).forEach(function (p) { out[p.type] = p.value; });
    out.h = parseInt(out.hour, 10) % 24; out.m = parseInt(out.minute, 10);
    return out;
  }
  function tick() {
    var ldn = partsIn('Europe/London'), lhr = partsIn('Asia/Karachi');
    $$('[data-clock="london"]').forEach(function (el) { el.textContent = ldn.hour + ':' + ldn.minute; });
    $$('[data-clock="lahore"]').forEach(function (el) { el.textContent = lhr.hour + ':' + lhr.minute; });
    // Office hours assumed 09:00–18:00 Pakistan time, Monday to Friday. Adjust if needed.
    var weekday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'].indexOf(lhr.weekday) > -1;
    var open = weekday && lhr.h >= 9 && lhr.h < 18;
    $$('[data-status="lahore"]').forEach(function (el) { el.textContent = open ? 'Lahore office hours' : 'Outside Lahore office hours'; });
    $$('.clocks .dot').forEach(function (d) { d.classList.toggle('on', open); });

    var offset = ((lhr.h * 60 + lhr.m) - (ldn.h * 60 + ldn.m) + 1440) % 1440 / 60;
    $$('[data-offset]').forEach(function (el) { el.textContent = offset; });
    $$('.sun-timeline').forEach(function (tl) {
      var lStart = 9 - offset, lEnd = 18 - offset, uStart = 9, uEnd = 17.5;
      var pct = function (h) { return (h / 24 * 100) + '%'; };
      var fmt = function (h) { var hh = Math.floor(h), mm = Math.round((h - hh) * 60); return (hh < 10 ? '0' : '') + hh + ':' + (mm < 10 ? '0' : '') + mm; };
      var set = function (sel, a, b, lbl) {
        var el = $(sel, tl); if (!el) return;
        el.style.left = pct(a); el.style.width = pct(b - a);
        el.textContent = lbl + ' ' + fmt(a) + '–' + fmt(b);
      };
      set('.lahore', lStart, lEnd, 'Lahore');
      set('.uk', uStart, uEnd, 'UK');
      set('.overlap', Math.max(lStart, uStart), Math.min(lEnd, uEnd), 'Live overlap');
      $$('.tl-now', tl).forEach(function (n) { n.style.left = pct(ldn.h + ldn.m / 60); });
    });
  }
  if ($('[data-clock]') || $('.sun-timeline')) { tick(); setInterval(tick, 30000); }

  /* ---------- Monthly / annual billing toggle ---------- */
  var billBtns = $$('[data-billing]');
  function setBilling(mode) {
    billBtns.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-billing') === mode ? 'true' : 'false'); });
    $$('.amount[data-monthly]').forEach(function (el) {
      var m = parseFloat(el.getAttribute('data-monthly'));
      el.textContent = '£' + (mode === 'annual' ? Math.round(m * 10 / 12) : m).toLocaleString('en-GB');
      var per = el.nextElementSibling;
      if (per && per.classList.contains('per')) {
        per.textContent = mode === 'annual' ? 'per month, billed annually (£' + (m * 10).toLocaleString('en-GB') + '/yr)' : 'per month, ex VAT';
      }
    });
  }
  billBtns.forEach(function (b) { b.addEventListener('click', function () { setBilling(b.getAttribute('data-billing')); }); });

  /* ---------- Scorecards (data in the JSON block inside each .quiz) ---------- */
  $$('.quiz[data-quiz]').forEach(function (quiz) {
    var D = JSON.parse($('.quiz-data', quiz).textContent);
    var steps = D.questions.map(function (q) { return { dim: q.dim, text: q.text, options: q.options, scored: true }; })
      .concat(D.context.map(function (c) { return { id: c.id, text: c.text, options: c.options, scored: false }; }));
    var dimName = {}; D.dims.forEach(function (d) { dimName[d.id] = d.name; });
    var host = $('.questions', quiz);
    steps.forEach(function (q, i) {
      var fs = document.createElement('fieldset');
      fs.className = 'q';
      var html = '<legend>' + q.text + '</legend>';
      q.options.forEach(function (o, v) {
        html += '<label class="opt"><input type="radio" name="' + D.id + '-q' + i + '" value="' + v + '"><span>' + o + '</span></label>';
      });
      fs.innerHTML = html;
      host.appendChild(fs);
    });
    var cur = 0, total = steps.length, started = false, pointer = false, lastText = '';
    var prev = $('.q-prev', quiz), next = $('.q-next', quiz), bar = $('.progress span', quiz);
    var sets = $$('.q', quiz);
    var picked = function (i) { return $('input[name="' + D.id + '-q' + i + '"]:checked', quiz); };
    function render(focus) {
      sets.forEach(function (s, i) { s.classList.toggle('active', i === cur); });
      $('.q-count', quiz).textContent = 'Question ' + (cur + 1) + ' of ' + total;
      $('.q-dim', quiz).textContent = steps[cur].scored ? dimName[steps[cur].dim] : 'About you';
      bar.style.width = (cur / total * 100) + '%';
      prev.disabled = cur === 0;
      next.disabled = !picked(cur);
      next.innerHTML = cur === total - 1 ? 'See my result <span class="arr" aria-hidden="true">→</span>' : 'Next <span class="arr" aria-hidden="true">→</span>';
      if (focus) { var f = picked(cur) || $('.q.active input', quiz); if (f) f.focus({ preventScroll: true }); }
    }
    // Auto-advance only after a mouse or touch choice. Keyboard users move between
    // options with the arrow keys, so they confirm with the Next button instead.
    quiz.addEventListener('pointerdown', function (e) { if (e.target.closest('.opt')) pointer = true; });
    quiz.addEventListener('change', function (e) {
      if (!e.target.matches('.q input')) return;
      if (!started) { started = true; track('scorecard_start', { scorecard: D.id }); }
      next.disabled = false;
      if (pointer && cur < total - 1) setTimeout(function () { cur++; render(true); }, 220);
      pointer = false;
    });
    prev.addEventListener('click', function () { if (cur > 0) { cur--; render(true); } });
    next.addEventListener('click', function () {
      if (!picked(cur)) return;
      if (cur < total - 1) { cur++; render(true); } else showResult();
    });
    render(false);

    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    function serviceCard(s, lbl) {
      return '<div class="rec-card"><span class="label">' + esc(lbl) + '</span><h4>' + s.name + '</h4><p>' + s.what +
        '</p><div class="rec-meta"><span>' + s.price + ' · ex VAT</span><a href="' + s.href + '">Details →</a></div></div>';
    }

    function showResult() {
      var sums = {}, counts = {}, sum = 0, n = 0, ctx = {};
      steps.forEach(function (q, i) {
        var v = parseInt(picked(i).value, 10);
        if (q.scored) { sum += v; n++; sums[q.dim] = (sums[q.dim] || 0) + v; counts[q.dim] = (counts[q.dim] || 0) + 1; }
        else ctx[q.id] = v;
      });
      var score = Math.round(sum / (n * 3) * 100);
      var band = D.bands.filter(function (b) { return score <= b.max; })[0] || D.bands[D.bands.length - 1];
      var pct = {};
      D.dims.forEach(function (d) { pct[d.id] = Math.round((sums[d.id] || 0) / ((counts[d.id] || 1) * 3) * 100); });
      var ranked = D.dims.slice().sort(function (a, b) { return pct[a.id] - pct[b.id]; });
      var weakest = ranked.slice(0, 2);

      ['.questions', '.quiz-nav', '.q-meta'].forEach(function (s) { $(s, quiz).style.display = 'none'; });
      bar.style.width = '100%';
      var r = $('.result', quiz);
      r.classList.add('show');
      $('.r-score', r).textContent = score;
      $('.r-band', r).textContent = band.name;
      $('.r-title', r).textContent = band.title;
      $('.r-text', r).textContent = band.text;
      var C = 2 * Math.PI * 88, arc = $('.r-arc', r);
      arc.style.strokeDasharray = C; arc.style.strokeDashoffset = C;
      setTimeout(function () { arc.style.strokeDashoffset = C * (1 - score / 100); }, 80);

      var bars = $('.r-bars', r); bars.innerHTML = '';
      D.dims.forEach(function (d) {
        var row = document.createElement('div');
        row.className = 'bar-row';
        row.innerHTML = '<span>' + d.name + '</span><div class="track" role="img" aria-label="' + d.name + ' ' + pct[d.id] + '%"><div class="fill"></div></div><span class="v">' + pct[d.id] + '%</span>';
        bars.appendChild(row);
        setTimeout(function () { $('.fill', row).style.width = pct[d.id] + '%'; }, 120);
      });
      $('.r-risks', r).innerHTML = band.risks.map(function (x) { return '<li>' + x + '</li>'; }).join('');
      $('.r-actions', r).innerHTML = band.actions.map(function (x) { return '<li>' + x + '</li>'; }).join('');

      var cards = serviceCard(band.service, 'Best fit for your result');
      var also = weakest.filter(function (d) { return d.service && pct[d.id] < 67 && d.service.name !== band.service.name; })[0];
      if (also) cards += serviceCard(also.service, 'Also consider: ' + also.name + ' scored ' + pct[also.id] + '%');
      $('.r-recs', r).innerHTML = cards;

      var notes = [];
      Object.keys(D.notes || {}).forEach(function (k) { var note = D.notes[k][String(ctx[k])]; if (note) notes.push(note); });
      var ctxEl = $('.r-context', r);
      ctxEl.innerHTML = notes.join(' '); // notes are trusted, static site content from build.py
      ctxEl.style.display = notes.length ? '' : 'none';

      var nx = $('.r-next', r);
      nx.textContent = band.next.label;
      nx.href = band.next.href;
      nx.setAttribute('data-track', band.next.track || 'result_next_step');
      $('.r-next-title', r).textContent = band.next.label;
      $('.r-next-text', r).textContent = band.next.text;

      lastText = D.title + ' — Bespoke Vista\n' +
        'Score: ' + score + '/100\nResult: ' + band.name + '\n\n' + band.title + '\n' + band.text + '\n\n' +
        'Scores by area:\n' + D.dims.map(function (d) { return '- ' + d.name + ': ' + pct[d.id] + '%'; }).join('\n') + '\n\n' +
        'Principal risks:\n' + band.risks.map(function (x) { return '- ' + x; }).join('\n') + '\n\n' +
        'Recommended actions:\n' + band.actions.map(function (x, i) { return (i + 1) + '. ' + x; }).join('\n') + '\n\n' +
        'Most suitable service: ' + band.service.name + ' (' + band.service.price + ', ex VAT)\n' +
        'Next step: ' + band.next.label + '\n\n' +
        D.context.map(function (c) { return c.text.replace(/\?$/, '') + ': ' + c.options[ctx[c.id]]; }).join('\n') + '\n\n' +
        'This result is a guide based on your answers, not a formal assessment.\n' + location.href.split('#')[0];
      $('.r-summary', r).value = lastText;
      $('.r-email', r).href = 'mailto:?subject=' + encodeURIComponent('My ' + D.title + ' result') + '&body=' + encodeURIComponent(lastText);

      track('scorecard_complete', { scorecard: D.id, score: score, band: band.name });
      r.scrollIntoView({ behavior: 'smooth', block: 'start' });
      r.focus({ preventScroll: true });
    }

    $('.r-download', quiz).addEventListener('click', function () {
      var blob = new Blob([lastText], { type: 'text/plain;charset=utf-8' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'bespoke-vista-' + D.id + '-scorecard-result.txt';
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
      track('result_download', { scorecard: D.id });
    });
    $('.r-email', quiz).addEventListener('click', function () { track('result_email', { scorecard: D.id }); });
    $('.r-retake', quiz).addEventListener('click', function () {
      $$('.q input', quiz).forEach(function (i) { i.checked = false; });
      $('.result', quiz).classList.remove('show');
      ['.questions', '.quiz-nav', '.q-meta'].forEach(function (s) { $(s, quiz).style.display = ''; });
      cur = 0; render(true);
      quiz.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  /* ---------- Contact form pre-fill from links ---------- */
  var topicSelect = $('#topic');
  if (topicSelect && params.get('topic')) {
    $$('option', topicSelect).forEach(function (o) { if (o.value === params.get('topic')) topicSelect.value = o.value; });
  }
  // Virtual Consultancy: ?plan=trial|essentials|professional|partner pre-selects the plan.
  var planSelect = $('#vc-plan');
  if (planSelect && params.get('plan')) {
    $$('option', planSelect).forEach(function (o) { if (o.value === params.get('plan')) planSelect.value = o.value; });
  }
  $$('a[href*="plan="][href$="#book"]').forEach(function (a) {
    if (!planSelect || a.pathname.split('/').pop() !== location.pathname.split('/').pop()) return;
    a.addEventListener('click', function () {
      var v = new URL(a.href).searchParams.get('plan');
      $$('option', planSelect).forEach(function (o) { if (o.value === v) planSelect.value = v; });
    });
  });
  var msgField = $('#message');
  if (msgField && params.get('message')) msgField.value = params.get('message');

  /* ---------- Forms ----------
     With data-endpoint set (Power Automate HTTP trigger, Formspree or similar), forms POST
     to it. Without one, they open the visitor's email app, and say so on screen, so the
     form never pretends to have sent something it hasn't. */
  $$('form[data-email]').forEach(function (form) {
    var endpoint = form.getAttribute('data-endpoint');
    var mode = $('.form-mode', form);
    if (mode) mode.textContent = endpoint
      ? 'Your details are sent securely to Bespoke Vista.'
      : 'Sending opens your email app with your details filled in, ready for you to send.';
    var status = $('.form-status', form);
    var show = function (msg, ok) { if (!status) return; status.textContent = msg; status.className = 'form-status show ' + (ok ? 'ok' : 'err'); };
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = new FormData(form);
      // Spam trap: real visitors never see or fill the hidden "website" field.
      if (data.get('website')) { form.reset(); show('Thank you.', true); return; }
      data.delete('website');
      var evt = form.getAttribute('data-event') || 'lead_submit';
      if (data.get('topic') === 'pilot') evt = 'pilot_enquiry_submit';
      track(evt, { topic: data.get('topic') || '', via: endpoint ? 'endpoint' : 'email_app' });
      if (endpoint) {
        // JSON works directly with a Power Automate "When an HTTP request is received" trigger and with Formspree.
        var payload = { form: form.getAttribute('data-subject') || form.id || 'enquiry', page: location.pathname, submittedAt: new Date().toISOString() };
        data.forEach(function (v, k) { payload[k] = v; });
        fetch(endpoint, { method: 'POST', body: JSON.stringify(payload), headers: { 'Content-Type': 'application/json', Accept: 'application/json' } })
          .then(function (r) { if (!r.ok) throw new Error(); form.reset(); show('Thank you. Your message has been sent and we will reply within one working day.', true); })
          .catch(function () { show('Sorry, your message could not be sent. Please email ' + form.getAttribute('data-email') + ' instead.', false); });
        return;
      }
      var lines = [];
      data.forEach(function (v, k) { if (k !== 'message' && k !== 'results' && v) lines.push(k.charAt(0).toUpperCase() + k.slice(1) + ': ' + v); });
      var subFrom = form.getAttribute('data-subject-from') && $('[name="' + form.getAttribute('data-subject-from') + '"]', form);
      if (subFrom && subFrom.selectedOptions && subFrom.selectedOptions[0]) form.setAttribute('data-subject', 'Virtual Consultancy request: ' + subFrom.selectedOptions[0].text);
      var subject = form.getAttribute('data-subject') || ('Enquiry: ' + ((topicSelect && topicSelect.selectedOptions[0]) ? topicSelect.selectedOptions[0].text : 'General'));
      var body = lines.join('\n') + (data.get('message') ? '\n\n' + data.get('message') : '') + (data.get('results') ? '\n\n' + data.get('results') : '');
      window.location.href = 'mailto:' + form.getAttribute('data-email') + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      show('Your email app should now be open with your message ready. Please press send there to complete your enquiry.', true);
    });
  });
})();
