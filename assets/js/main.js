// Bespoke Vista — site behaviour
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var params = new URLSearchParams(window.location.search);

  /* ---------- Mobile navigation ---------- */
  var toggle = $('.nav-toggle'), links = $('.nav-links');
  if (toggle && links) {
    var close = function () { links.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); };
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    links.addEventListener('click', function (e) { if (e.target.closest('a')) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }

  /* ---------- Footer year ---------- */
  var year = $('#year');
  if (year) year.textContent = new Date().getFullYear();

  /* ---------- Reveal on scroll ---------- */
  var items = $$('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
    }, { threshold: 0.1 });
    items.forEach(function (el) { io.observe(el); });
  } else items.forEach(function (el) { el.classList.add('visible'); });

  /* ---------- Sticky jump bar: highlight section in view ---------- */
  var subLinks = $$('.subnav a');
  if (subLinks.length && 'IntersectionObserver' in window) {
    var byId = {};
    subLinks.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        subLinks.forEach(function (a) { a.classList.remove('active'); });
        var link = byId[e.target.id];
        if (link) {
          link.classList.add('active');
          var bar = link.closest('ul');
          bar.scrollLeft = link.offsetLeft - (bar.clientWidth - link.offsetWidth) / 2;
        }
      });
    }, { rootMargin: '-35% 0px -60% 0px' });
    Object.keys(byId).forEach(function (id) { var el = document.getElementById(id); if (el) spy.observe(el); });
  }

  /* ---------- Live clocks: London and Lahore ---------- */
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
    var weekday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'].indexOf(lhr.weekday) > -1;
    var online = weekday && lhr.h >= 9 && lhr.h < 18;
    $$('[data-status="lahore"]').forEach(function (el) {
      el.textContent = online ? 'Lahore team working now' : 'Lahore team offline';
    });
    $$('.clocks .dot').forEach(function (d) { d.classList.toggle('on', online); });

    // Follow-the-sun timeline (positions in UK local time)
    var tl = $('.sun-timeline');
    if (tl) {
      var offset = ((lhr.h * 60 + lhr.m) - (ldn.h * 60 + ldn.m) + 1440) % 1440 / 60; // hours ahead
      var lStart = 9 - offset, lEnd = 18 - offset, uStart = 9, uEnd = 17.5;
      var pct = function (h) { return (h / 24 * 100) + '%'; };
      var fmt = function (h) { var hh = Math.floor(h), mm = Math.round((h - hh) * 60); return (hh < 10 ? '0' : '') + hh + ':' + (mm < 10 ? '0' : '') + mm; };
      var set = function (sel, a, b, label) {
        var el = $(sel, tl); if (!el) return;
        el.style.left = pct(a); el.style.width = pct(b - a);
        if (label) el.textContent = label + ' ' + fmt(a) + '–' + fmt(b);
      };
      set('.lahore', lStart, lEnd, 'Lahore');
      set('.uk', uStart, uEnd, 'UK');
      set('.overlap', Math.max(lStart, uStart), Math.min(lEnd, uEnd), 'Live overlap');
      var now = $('.tl-now', tl);
      if (now) $$('.tl-now', tl).forEach(function (n) { n.style.left = pct(ldn.h + ldn.m / 60); });
      $$('[data-offset]').forEach(function (el) { el.textContent = offset; });
    }
  }
  if ($('[data-clock]') || $('.sun-timeline')) { tick(); setInterval(tick, 30000); }

  /* ---------- Monthly / annual billing toggle ---------- */
  var billBtns = $$('[data-billing]');
  function setBilling(mode) {
    billBtns.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-billing') === mode ? 'true' : 'false'); });
    $$('.amount[data-monthly]').forEach(function (el) {
      var m = parseFloat(el.getAttribute('data-monthly'));
      var v = mode === 'annual' ? Math.round(m * 10 / 12) : m;
      el.textContent = '£' + v.toLocaleString('en-GB');
      var per = el.nextElementSibling;
      if (per && per.classList.contains('per')) {
        per.textContent = mode === 'annual'
          ? 'per month, billed annually (£' + (m * 10).toLocaleString('en-GB') + '/yr)'
          : 'per month, ex VAT';
      }
    });
  }
  billBtns.forEach(function (b) { b.addEventListener('click', function () { setBilling(b.getAttribute('data-billing')); }); });

  /* ---------- Scorecards (data-driven: see the JSON block inside each .quiz) ---------- */
  function track(name, data) {
    // Pushes events for Google Tag Manager / GA4 if installed; harmless otherwise.
    try { (window.dataLayer = window.dataLayer || []).push(Object.assign({ event: name }, data || {})); } catch (e) {}
  }
  $$('.quiz[data-quiz]').forEach(function (quiz) {
    var D = JSON.parse($('.quiz-data', quiz).textContent);
    var steps = D.questions.map(function (q) { return { dim: q.dim, text: q.text, options: q.options, scored: true }; })
      .concat(D.context.map(function (c) { return { id: c.id, dim: null, text: c.text, options: c.options, scored: false }; }));
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
    var cur = 0, total = steps.length, started = false;
    var prev = $('.q-prev', quiz), next = $('.q-next', quiz), bar = $('.progress span', quiz);
    var sets = $$('.q', quiz);
    var picked = function (i) { return $('input[name="' + D.id + '-q' + i + '"]:checked', quiz); };
    function render() {
      sets.forEach(function (s, i) { s.classList.toggle('active', i === cur); });
      $('.q-count', quiz).textContent = 'Question ' + (cur + 1) + ' of ' + total;
      $('.q-dim', quiz).textContent = steps[cur].scored ? dimName[steps[cur].dim] : 'About you';
      bar.style.width = (cur / total * 100) + '%';
      prev.disabled = cur === 0;
      next.disabled = !picked(cur);
      next.innerHTML = cur === total - 1 ? 'See my result <span class="arr">→</span>' : 'Next <span class="arr">→</span>';
    }
    quiz.addEventListener('change', function (e) {
      if (!e.target.matches('.q input')) return;
      if (!started) { started = true; track('scorecard_start', { scorecard: D.id }); }
      next.disabled = false;
      if (cur < total - 1) setTimeout(function () { cur++; render(); var f = $('.q.active input', quiz); if (f) f.focus({ preventScroll: true }); }, 220);
    });
    prev.addEventListener('click', function () { if (cur > 0) { cur--; render(); } });
    next.addEventListener('click', function () {
      if (!picked(cur)) return;
      if (cur < total - 1) { cur++; render(); } else showResult();
    });
    render();

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
      var top = ranked.slice(0, 2);

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
        row.innerHTML = '<span>' + d.name + '</span><div class="track"><div class="fill"></div></div><span class="v">' + pct[d.id] + '%</span>';
        bars.appendChild(row);
        setTimeout(function () { $('.fill', row).style.width = pct[d.id] + '%'; }, 120);
      });

      $('.r-recs', r).innerHTML = top.map(function (d) {
        var s = d.service;
        return '<div class="rec-card"><span class="label">' + d.name + ' · ' + pct[d.id] + '%</span><h4>' + s.name + '</h4><p>' + s.what +
          '</p><div class="rec-meta"><span>' + s.price + '</span><a href="' + s.href + '">Details →</a></div></div>';
      }).join('');

      var notes = [];
      Object.keys(D.notes || {}).forEach(function (k) {
        var note = D.notes[k][String(ctx[k])];
        if (note) notes.push(note);
      });
      var ctxEl = $('.r-context', r);
      ctxEl.textContent = notes.join(' ');
      ctxEl.style.display = notes.length ? '' : 'none';

      var ctxText = D.context.map(function (c) { return c.text.replace(/\?$/, '') + ': ' + c.options[ctx[c.id]]; }).join('\n');
      var summary = D.title + ': ' + score + '/100 (' + band.name + ')\n' +
        D.dims.map(function (d) { return '- ' + d.name + ': ' + pct[d.id] + '%'; }).join('\n') +
        '\nTop opportunities: ' + top.map(function (d) { return d.service.name; }).join(', ') + '\n' + ctxText;
      $('.r-summary', r).value = summary;
      track('scorecard_complete', { scorecard: D.id, score: score, band: band.name });
      r.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    $('.r-retake', quiz).addEventListener('click', function () {
      $$('.q input', quiz).forEach(function (i) { i.checked = false; });
      $('.result', quiz).classList.remove('show');
      ['.questions', '.quiz-nav', '.q-meta'].forEach(function (s) { $(s, quiz).style.display = ''; });
      cur = 0; render();
      quiz.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  /* ---------- Contact form ---------- */
  var topicSelect = $('#topic');
  if (topicSelect && params.get('topic')) {
    $$('option', topicSelect).forEach(function (o) { if (o.value === params.get('topic')) topicSelect.value = o.value; });
  }
  var msgField = $('#message');
  if (msgField && params.get('message')) msgField.value = params.get('message');
  var emailField = $('#email');
  if (emailField && params.get('email')) emailField.value = params.get('email');

  // Set data-endpoint on a form to a form-service URL (e.g. Formspree) to submit directly.
  // Without one, the form opens the visitor's email app with the message filled in.
  $$('form[data-email]').forEach(function (form) {
    var status = $('.form-status', form);
    var show = function (msg, ok) { if (!status) return; status.textContent = msg; status.className = 'form-status show ' + (ok ? 'ok' : 'err'); };
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      track('lead_submit', { form: form.getAttribute('data-subject') || form.id || 'form' });
      var data = new FormData(form);
      var endpoint = form.getAttribute('data-endpoint');
      if (endpoint) {
        fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
          .then(function (r) { if (!r.ok) throw new Error(); form.reset(); show('Thank you, your message has been sent. We’ll be in touch within one working day.', true); })
          .catch(function () { show('Sorry, something went wrong. Please email us directly instead.', false); });
        return;
      }
      var lines = [];
      data.forEach(function (v, k) { if (k !== 'message' && v) lines.push(k.charAt(0).toUpperCase() + k.slice(1) + ': ' + v); });
      var subject = form.getAttribute('data-subject') || ('Enquiry: ' + (data.get('topic') || 'General'));
      var body = lines.join('\n') + (data.get('message') ? '\n\n' + data.get('message') : '');
      window.location.href = 'mailto:' + form.getAttribute('data-email') + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      show('Your email app should now open with your message ready to send.', true);
    });
  });
})();
