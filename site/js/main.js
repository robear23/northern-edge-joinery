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

  /* ── Scroll progress: one listener, one frame, N subscribers ─ */

  /* A track maps an element's travel through the viewport onto 0…1. `from`
     and `to` are viewport fractions measured from the top: progress is 0 when
     the element's top edge sits at `from`, and 1 when its bottom edge reaches
     `to`. Subscribers are all read in the same frame, so adding an effect
     costs no extra scroll listener. */

  var tracks = [];
  var framePending = false;

  function trackProgress(el, from, to, onProgress) {
    tracks.push({ el: el, from: from, to: to, run: onProgress });
  }

  function progressOf(track) {
    var rect = track.el.getBoundingClientRect();
    var vh = window.innerHeight || document.documentElement.clientHeight;
    var zero = vh * track.from;
    var one = vh * track.to;
    // An element taller than its own travel window would divide by zero or
    // less; treat it as finished rather than letting it jump.
    var distance = rect.height + zero - one;
    if (distance <= 0) return 1;
    return Math.min(1, Math.max(0, (zero - rect.top) / distance));
  }

  function readTracks() {
    framePending = false;
    tracks.forEach(function (t) { t.run(progressOf(t)); });
  }

  function queueTracks() {
    if (framePending) return;
    framePending = true;
    requestAnimationFrame(readTracks);
  }

  /* ── Text reveals: the shared word split ─────────────────── */

  /* Split on whitespace and keep the gaps as real text nodes, so the heading's
     text content, wrapping and accessible name are all unchanged. Words, not
     characters: at display size a per-character ripple reads as an effect, and
     a per-word one reads as the sentence arriving.

     The recessed colour lives on these spans and nowhere else, so a script
     that throws before this runs leaves the heading at full colour rather
     than stranding it mid-reveal. */
  function splitWords(el, className) {
    var frag = document.createDocumentFragment();
    var words = [];

    el.textContent.split(/(\s+)/).forEach(function (part) {
      if (!part) return;
      if (/^\s+$/.test(part)) {
        frag.appendChild(document.createTextNode(part));
        return;
      }
      var span = document.createElement('span');
      span.className = className;
      span.textContent = part;
      frag.appendChild(span);
      words.push(span);
    });

    el.textContent = '';
    el.appendChild(frag);
    return words;
  }

  /* ── Hero headline: resolves on load ─────────────────────── */

  /* The hero is the full viewport at scroll 0, so there is no travel to scrub
     against — this one runs on a timer, and it is the only thing on the site
     that does. The delay is carried as an index and the timing lives in the
     stylesheet, so there are no JS timers to leak or to fall out of step. */
  if (!reduceMotion) {
    var heroHeading = document.querySelector('.hero h1');
    if (heroHeading) {
      splitWords(heroHeading, 'hero__word').forEach(function (word, i) {
        word.style.setProperty('--word-index', i);
      });
    }
  }

  /* ── Intro statement: words resolve as you read past them ── */

  if (!reduceMotion) {
    Array.prototype.forEach.call(
      document.querySelectorAll('.intro__statement'),
      function (statement) {
        var words = splitWords(statement, 'statement__word');
        var lit = 0; // monotonic — a word that has resolved never recedes

        // Finishes when the statement's bottom edge is 75% down the viewport,
        // so the last word lands while the sentence is still sitting in the
        // middle of the screen. Ending it any later — 0.45 was the first
        // attempt — lights the closing words as they leave the top, which is
        // exactly when nobody is looking at them.
        trackProgress(statement, 0.9, 0.75, function (p) {
          var target = Math.round(p * words.length);
          while (lit < target) {
            words[lit].classList.add('is-lit');
            lit++;
          }
        });
      }
    );
  }

  /* ── Process: each step's rule draws in as you reach it ──── */

  /* Service pages reuse .process__grid as a plain two-column layout, so the
     steps rather than the grid decide whether any of this runs. */
  var processGrid = document.querySelector('.process__grid');
  var steps = processGrid
    ? Array.prototype.slice.call(processGrid.querySelectorAll('.step'))
    : [];

  if (steps.length && !reduceMotion) {
    // Each step owns a window of the section's travel. The windows overlap so
    // the rules read as one run rather than four separate events, and the last
    // one closes exactly as the section finishes.
    var SPAN = 0.45;
    var LEAD = steps.length > 1 ? (1 - SPAN) / (steps.length - 1) : 0;

    trackProgress(processGrid, 0.75, 0.6, function (p) {
      steps.forEach(function (step, i) {
        var local = Math.min(1, Math.max(0, (p - i * LEAD) / SPAN));
        step.style.setProperty('--step-progress', local.toFixed(3));
        // Halfway, not the first pixel: lighting the numeral the instant its
        // rule starts drawing puts all four up at once and loses the sequence.
        step.classList.toggle('is-active', local > 0.5);
      });
    });
  }

  /* ── Hero Slideshow / Dot Synchronization ────────────────── */

  var heroMedia = document.querySelector('.hero__media');
  var heroSlides = heroMedia ? Array.prototype.slice.call(heroMedia.querySelectorAll('.hero__slide')) : [];
  var heroDots = Array.prototype.slice.call(document.querySelectorAll('.hero__dot'));

  if (heroSlides.length > 1 && heroDots.length === heroSlides.length) {
    var slideDuration = 6000;
    var currentSlideIndex = 0;
    var slideTimer = null;

    var setSlide = function (index, isManualClick) {
      currentSlideIndex = index;

      if (isManualClick && heroMedia) {
        heroMedia.classList.add('is-manual');
        heroSlides.forEach(function (slide, i) {
          slide.classList.toggle('is-active', i === index);
        });
      }

      heroDots.forEach(function (dot, i) {
        var active = (i === index);
        dot.classList.toggle('is-active', active);
        dot.setAttribute('aria-selected', String(active));
      });
    };

    var startAutoSync = function () {
      if (reduceMotion) return;
      slideTimer = setInterval(function () {
        if (heroMedia && heroMedia.classList.contains('is-manual')) return;
        currentSlideIndex = (currentSlideIndex + 1) % heroSlides.length;
        setSlide(currentSlideIndex, false);
      }, slideDuration);
    };

    heroDots.forEach(function (dot, i) {
      dot.addEventListener('click', function () {
        if (slideTimer) clearInterval(slideTimer);
        setSlide(i, true);
      });
    });

    startAutoSync();
  }

  if (tracks.length) {
    readTracks();
    window.addEventListener('scroll', queueTracks, { passive: true });
    window.addEventListener('resize', queueTracks, { passive: true });
  }
})();
