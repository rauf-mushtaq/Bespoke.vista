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

  /* ---------- AI Readiness Scorecard ---------- */
  var quiz = $('#scorecard');
  if (quiz) {
    var Q = [
      ['Strategy', 'Does your leadership team agree on what AI should achieve for the business?',
        ['Not discussed yet', 'Talked about, nothing agreed', 'Some goals agreed for specific areas', 'Clear goals, with owners and measures']],
      ['Strategy', 'Have you identified specific processes where AI could save time or money?',
        ['No', 'A few ideas', 'A shortlist with rough value', 'A prioritised, costed pipeline']],
      ['People', 'How are your people using AI tools today?',
        ['Not at all, or we don’t know', 'A few enthusiasts, on their own', 'Several teams use approved tools', 'Widely used, part of how we work']],
      ['People', 'Have staff been trained to use AI well and safely?',
        ['No training', 'Informal tips and videos', 'Some formal training', 'Role-based training with ongoing support']],
      ['Process', 'How well documented are your core processes?',
        ['Mostly in people’s heads', 'Some documents, often out of date', 'Key processes documented', 'Documented, owned and kept current']],
      ['Process', 'How much repetitive manual work do teams do (re-keying, chasing, copying between systems)?',
        ['A lot, it’s a daily burden', 'Quite a bit', 'Some, we’ve automated the worst', 'Very little, most is automated']],
      ['Data & tools', 'Where does your business information live?',
        ['Scattered across email, desktops and paper', 'Shared drives, hard to find things', 'Mostly in Microsoft 365 / SharePoint, reasonably organised', 'Well structured, searchable, clear permissions']],
      ['Data & tools', 'Which AI tools do you have access to?',
        ['None', 'Free consumer tools only', 'Business licences for some (Copilot, ChatGPT, Claude)', 'Business tools connected to our systems']],
      ['Governance', 'Do you have an AI usage policy?',
        ['No', 'Being drafted', 'Yes, but few people know it', 'Yes, communicated and reviewed regularly']],
      ['Governance', 'Do you know what company data is going into AI tools?',
        ['No idea', 'We suspect it happens', 'Partly, with some controls', 'Yes, with controls and monitoring']]
    ];
    var host = $('#questions', quiz);
    Q.forEach(function (q, i) {
      var fs = document.createElement('fieldset');
      fs.className = 'q' + (i === 0 ? ' active' : '');
      var html = '<legend>' + q[1] + '</legend>';
      q[2].forEach(function (o, v) {
        html += '<label class="opt"><input type="radio" name="q' + i + '" value="' + v + '"><span>' + o + '</span></label>';
      });
      fs.innerHTML = html;
      host.appendChild(fs);
    });
    var cur = 0, total = Q.length;
    var prev = $('#q-prev', quiz), next = $('#q-next', quiz), bar = $('.progress span', quiz);
    var counter = $('#q-count', quiz), dim = $('#q-dim', quiz);
    var sets = $$('.q', quiz);
    function answered(i) { return !!$('input[name="q' + i + '"]:checked', quiz); }
    function render() {
      sets.forEach(function (s, i) { s.classList.toggle('active', i === cur); });
      counter.textContent = 'Question ' + (cur + 1) + ' of ' + total;
      dim.textContent = Q[cur][0];
      bar.style.width = (cur / total * 100) + '%';
      prev.disabled = cur === 0;
      next.disabled = !answered(cur);
      next.innerHTML = cur === total - 1 ? 'See my score <span class="arr">→</span>' : 'Next <span class="arr">→</span>';
    }
    quiz.addEventListener('change', function () {
      next.disabled = !answered(cur);
      if (cur < total - 1) setTimeout(function () { cur++; render(); var f = $('.q.active input', quiz); if (f) f.focus({ preventScroll: true }); }, 220);
    });
    prev.addEventListener('click', function () { if (cur > 0) { cur--; render(); } });
    next.addEventListener('click', function () {
      if (!answered(cur)) return;
      if (cur < total - 1) { cur++; render(); } else showResult();
    });
    render();

    function showResult() {
      var dims = {}, sum = 0;
      Q.forEach(function (q, i) {
        var v = parseInt($('input[name="q' + i + '"]:checked', quiz).value, 10);
        sum += v; dims[q[0]] = (dims[q[0]] || 0) + v;
      });
      var score = Math.round(sum / (total * 3) * 100);
      var bands = [
        [35, 'Explorer', 'Start with clarity',
          'AI is on the radar but not yet in the business. The quickest win is an agreed view of where AI will genuinely pay off, and a few safe rules so people can start experimenting without putting data at risk.',
          [['AI Readiness Assessment', 'services.html#ai'], ['Executive AI Intelligence', 'pricing.html#intelligence']]],
        [60, 'Experimenter', 'Turn pockets of use into a plan',
          'People are already using AI, but in pockets and without much structure. Now is the time to agree priorities, put governance in place and pick two or three use cases worth scaling.',
          [['AI Readiness Assessment', 'services.html#ai'], ['AI Governance Pack', 'pricing.html#projects']]],
        [80, 'Adopter', 'Scale what works',
          'You have the foundations. The value now comes from rolling out proven use cases, automating end-to-end workflows and measuring the benefit properly.',
          [['Copilot Adoption Programme', 'pricing.html#projects'], ['AI Advisory subscription', 'pricing.html#advisory']]],
        [101, 'Leader', 'Optimise and run',
          'You’re ahead of most UK organisations. The next step is getting more from your existing tools and having a team that runs and improves AI workflows every month.',
          [['AI Optimisation Review', 'pricing.html#projects'], ['AI Operations Team', 'managed-teams.html#offerings']]]
      ];
      var b = bands.filter(function (x) { return score < x[0]; })[0];
      var weakest = Object.keys(dims).sort(function (a, c) { return dims[a] - dims[c]; })[0];

      $('#questions', quiz).style.display = 'none';
      $('.quiz-nav', quiz).style.display = 'none';
      $('.q-meta', quiz).style.display = 'none';
      bar.style.width = '100%';
      var r = $('#result', quiz);
      r.classList.add('show');
      $('#r-score', r).textContent = score;
      $('#r-band', r).textContent = b[1];
      $('#r-title', r).textContent = b[2];
      $('#r-text', r).textContent = b[3];
      $('#r-weak', r).textContent = weakest;
      var C = 2 * Math.PI * 88;
      var arc = $('#r-arc', r);
      arc.style.strokeDasharray = C;
      arc.style.strokeDashoffset = C;
      requestAnimationFrame(function () { setTimeout(function () { arc.style.strokeDashoffset = C * (1 - score / 100); }, 60); });
      var bars = $('#r-bars', r);
      bars.innerHTML = '';
      Object.keys(dims).forEach(function (k) {
        var p = Math.round(dims[k] / 6 * 100);
        var row = document.createElement('div');
        row.className = 'bar-row';
        row.innerHTML = '<span>' + k + '</span><div class="track"><div class="fill"></div></div><span class="v">' + p + '%</span>';
        bars.appendChild(row);
        setTimeout(function () { $('.fill', row).style.width = p + '%'; }, 120);
      });
      var recs = $('#r-recs', r);
      recs.innerHTML = b[4].map(function (x) { return '<a class="btn btn-line-light btn-sm" href="' + x[1] + '">' + x[0] + '</a>'; }).join('');
      var msg = 'My AI Readiness Scorecard result: ' + score + '/100 (' + b[1] + '). Weakest area: ' + weakest + '.\n\nI would like to discuss next steps.';
      $('#r-discuss', r).href = 'contact.html?topic=scorecard&message=' + encodeURIComponent(msg);
      r.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    $('#r-retake', quiz).addEventListener('click', function () {
      $$('input', quiz).forEach(function (i) { i.checked = false; });
      $('#result', quiz).classList.remove('show');
      $('#questions', quiz).style.display = '';
      $('.quiz-nav', quiz).style.display = '';
      $('.q-meta', quiz).style.display = '';
      cur = 0; render();
    });
  }

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
