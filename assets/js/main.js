// Bespoke Vista — site behaviour
(function () {
  // Mobile navigation
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Footer year
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Reveal on scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('visible'); });
  }

  // Pre-select enquiry type from ?topic= on the contact page
  var topicSelect = document.getElementById('topic');
  if (topicSelect) {
    var topic = new URLSearchParams(window.location.search).get('topic');
    if (topic) {
      Array.prototype.forEach.call(topicSelect.options, function (o) {
        if (o.value === topic) topicSelect.value = topic;
      });
    }
  }

  // Contact form
  // Set data-endpoint on the form to a form service URL (e.g. Formspree) to submit via fetch.
  // Without an endpoint the form falls back to opening the visitor's email client.
  var form = document.getElementById('contact-form');
  if (form) {
    var status = document.getElementById('form-status');
    var show = function (msg, ok) {
      status.textContent = msg;
      status.className = 'form-status show ' + (ok ? 'ok' : 'err');
    };
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = new FormData(form);
      var endpoint = form.getAttribute('data-endpoint');
      if (endpoint) {
        fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
          .then(function (r) {
            if (!r.ok) throw new Error();
            form.reset();
            show('Thank you — your message has been sent. We will be in touch within one working day.', true);
          })
          .catch(function () {
            show('Sorry, something went wrong sending your message. Please email us directly instead.', false);
          });
      } else {
        var to = form.getAttribute('data-email');
        var subject = 'Enquiry: ' + (data.get('topic') || 'General') + ' — ' + data.get('name');
        var body =
          'Name: ' + data.get('name') + '\n' +
          'Organisation: ' + (data.get('organisation') || '') + '\n' +
          'Email: ' + data.get('email') + '\n' +
          'Phone: ' + (data.get('phone') || '') + '\n' +
          'Topic: ' + (data.get('topic') || '') + '\n\n' +
          data.get('message');
        window.location.href = 'mailto:' + to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
        show('Your email app should now open with your message ready to send.', true);
      }
    });
  }
})();
