/* ============================================================
   Northern Edge Joinery Ltd
   Header collapse, drawer, portfolio filter, lightbox, form.

   Restrained by design: one 300ms duration, a fade and a small
   translate, and nothing that moves on its own.
   ============================================================ */

(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]), ' +
    'select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

  // A panel that is mid-transition from visibility:hidden cannot take focus
  // yet, so wait for the style change to paint before moving into it.
  function focusAfterPaint(el) {
    if (!el) return;
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { el.focus(); });
    });
  }

  function trapFocus(container, event) {
    var items = Array.prototype.filter.call(
      container.querySelectorAll(FOCUSABLE),
      function (el) { return el.offsetParent !== null || el === document.activeElement; }
    );
    if (!items.length) return;
    var first = items[0];
    var last = items[items.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  /* ── Header: padding-top collapses 56px → 14px on scroll ── */

  var header = document.getElementById('site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 40);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ── Mobile drawer ──────────────────────────────────────── */

  var burger = document.querySelector('.burger');
  var drawer = document.getElementById('drawer');

  if (burger && drawer) {
    // Held in the markup so a no-JS visitor never meets a stuck panel;
    // from here the CSS visibility transition owns it.
    drawer.hidden = false;

    var setDrawer = function (open) {
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      drawer.classList.toggle('is-open', open);
      document.body.classList.toggle('is-locked', open);
      if (open) {
        focusAfterPaint(drawer.querySelector(FOCUSABLE));
      } else {
        burger.focus();
      }
    };

    burger.addEventListener('click', function () {
      setDrawer(burger.getAttribute('aria-expanded') !== 'true');
    });

    drawer.addEventListener('click', function (e) {
      if (e.target.closest('a')) setDrawer(false);
    });

    document.addEventListener('keydown', function (e) {
      if (!drawer.classList.contains('is-open')) return;
      if (e.key === 'Escape') setDrawer(false);
      if (e.key === 'Tab') trapFocus(drawer, e);
    });
  }

  /* ── Portfolio filter ───────────────────────────────────── */

  var filters = Array.prototype.slice.call(document.querySelectorAll('.filter'));
  var works = Array.prototype.slice.call(document.querySelectorAll('.work'));
  var filterStatus = document.getElementById('filter-status');

  function visibleWorks() {
    return works.filter(function (w) { return !w.classList.contains('is-hidden'); });
  }

  if (filters.length && works.length) {
    filters.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var cat = btn.dataset.filter;

        filters.forEach(function (f) {
          f.setAttribute('aria-pressed', String(f === btn));
        });

        works.forEach(function (w) {
          w.classList.toggle('is-hidden', cat !== 'all' && w.dataset.cat !== cat);
        });

        if (filterStatus) {
          var n = visibleWorks().length;
          filterStatus.textContent = n + (n === 1 ? ' project shown' : ' projects shown');
        }
      });
    });
  }

  /* ── Lightbox ───────────────────────────────────────────── */

  var lightbox = document.getElementById('lightbox');

  if (lightbox && works.length) {
    lightbox.hidden = false;

    var lbImg = document.getElementById('lightbox-img');
    var lbCaption = document.getElementById('lightbox-caption');
    var lbCat = document.getElementById('lightbox-cat');
    var lbCount = document.getElementById('lightbox-count');
    var lastFocused = null;
    var current = 0;

    var show = function (index) {
      var list = visibleWorks();
      if (!list.length) return;
      current = (index + list.length) % list.length;
      var item = list[current];
      var img = item.querySelector('img');

      lbImg.src = item.dataset.full;
      lbImg.alt = img ? img.alt : '';
      lbCaption.textContent = item.dataset.caption || '';
      lbCat.textContent = item.dataset.catLabel || '';
      lbCount.textContent = (current + 1) + ' / ' + list.length;
    };

    var open = function (item) {
      lastFocused = document.activeElement;
      show(visibleWorks().indexOf(item));
      lightbox.classList.add('is-open');
      document.body.classList.add('is-locked');
      focusAfterPaint(lightbox.querySelector('[data-lb="close"]'));
    };

    var close = function () {
      lightbox.classList.remove('is-open');
      document.body.classList.remove('is-locked');
      if (lastFocused) lastFocused.focus();
    };

    works.forEach(function (item) {
      item.addEventListener('click', function () { open(item); });
    });

    lightbox.addEventListener('click', function (e) {
      var action = e.target.closest('[data-lb]');
      if (action) {
        var what = action.dataset.lb;
        if (what === 'close') close();
        if (what === 'prev') show(current - 1);
        if (what === 'next') show(current + 1);
        return;
      }
      // click the backdrop to dismiss
      if (e.target === lightbox) close();
    });

    document.addEventListener('keydown', function (e) {
      if (!lightbox.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowLeft') show(current - 1);
      else if (e.key === 'ArrowRight') show(current + 1);
      else if (e.key === 'Tab') trapFocus(lightbox, e);
    });
  }

  /* ── Enquiry form ───────────────────────────────────────── */

  var form = document.getElementById('enquiry-form');

  if (form) {
    var okPanel = document.getElementById('form-ok');
    var failPanel = document.getElementById('form-fail');

    var RULES = {
      name: function (v) {
        if (!v.trim()) return 'Please tell us your name.';
        if (v.trim().length > 120) return 'That is longer than we can accept.';
        return '';
      },
      email: function (v) {
        if (!v.trim()) return 'We need an email address to reply to.';
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim())) return 'That does not look like an email address.';
        return '';
      },
      project: function (v) {
        if (!v) return 'Please choose the closest project type.';
        return '';
      },
      message: function (v) {
        if (!v.trim()) return 'Please tell us a little about the room.';
        if (v.trim().length < 10) return 'A sentence or two would help us reply usefully.';
        if (v.trim().length > 4000) return 'That is longer than we can accept.';
        return '';
      }
    };

    var setFieldError = function (input, message) {
      var field = input.closest('.field');
      var slot = document.getElementById(input.id + '-error');
      field.setAttribute('data-invalid', message ? 'true' : 'false');
      input.setAttribute('aria-invalid', message ? 'true' : 'false');
      if (slot) {
        slot.textContent = message;
        input.setAttribute('aria-describedby', slot.id);
      }
    };

    var validateField = function (input) {
      var rule = RULES[input.name];
      if (!rule) return true;
      var message = rule(input.value);
      setFieldError(input, message);
      return !message;
    };

    Object.keys(RULES).forEach(function (name) {
      var input = form.elements[name];
      if (!input) return;
      input.addEventListener('blur', function () { validateField(input); });
      input.addEventListener('input', function () {
        if (input.closest('.field').getAttribute('data-invalid') === 'true') validateField(input);
      });
    });

    var showPanel = function (panel) {
      [okPanel, failPanel].forEach(function (p) {
        if (p) p.classList.toggle('is-visible', p === panel);
      });
      if (panel) {
        panel.focus();
        panel.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'center' });
      }
    };

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var firstBad = null;
      Object.keys(RULES).forEach(function (name) {
        var input = form.elements[name];
        if (input && !validateField(input) && !firstBad) firstBad = input;
      });
      if (firstBad) { firstBad.focus(); return; }

      // Honeypot: a filled hidden field means a bot. Accept it silently
      // so the bot learns nothing, and send nothing.
      if (form.elements['company-website'] && form.elements['company-website'].value) {
        showPanel(okPanel);
        form.reset();
        return;
      }

      var submit = form.querySelector('[type="submit"]');
      var original = submit.textContent;
      submit.disabled = true;
      submit.textContent = 'Sending…';

      var endpoint = form.dataset.endpoint || '/api/enquiry';

      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
        body: new URLSearchParams(new FormData(form)).toString()
      })
        .then(function (res) {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          showPanel(okPanel);
          form.reset();
          Object.keys(RULES).forEach(function (name) {
            var input = form.elements[name];
            if (input) setFieldError(input, '');
          });
        })
        .catch(function (err) {
          if (window.console) {
            console.warn('Enquiry submission failed. Is the form endpoint configured? ' +
              'See README.md → Forms.', err);
          }
          showPanel(failPanel);
        })
        .then(function () {
          submit.disabled = false;
          submit.textContent = original;
        });
    });
  }

  /* ── Scroll reveals ─────────────────────────────────────── */

  var reveals = document.querySelectorAll('.reveal');

  if (reveals.length) {
    if (reduceMotion || !('IntersectionObserver' in window)) {
      Array.prototype.forEach.call(reveals, function (el) { el.classList.add('is-in'); });
    } else {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            observer.unobserve(entry.target);
          }
        });
      }, { rootMargin: '0px 0px -12% 0px', threshold: 0.05 });

      Array.prototype.forEach.call(reveals, function (el) { observer.observe(el); });
    }
  }
})();
