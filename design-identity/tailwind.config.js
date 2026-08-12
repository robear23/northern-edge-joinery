/** @type {import('tailwindcss').Config} */
// Design identity extracted from https://nobaandstod.co.uk/
// Generated: 2026-08-12
// Aesthetic: Editorial (luxury editorial — dark, serif-led, flat)
//
// Values commented "inferred" are NOT present in the source stylesheet.
// Using them departs from the original design. See DESIGN.md for the
// five rules that make or break a faithful reproduction.

module.exports = {
  content: ['./src/**/*.{html,js,jsx,ts,tsx,vue,svelte}'],

  // The source has NO dark-mode toggle: no prefers-color-scheme blocks,
  // no [data-theme], no .dark class. It is dark-ONLY by design — the dark
  // palette IS the brand. 'class' is set so you can opt into a light
  // variant if you extend the system; the source never does.
  darkMode: 'class',

  theme: {
    extend: {

      colors: {
        primary: {
          DEFAULT: '#dec497', // champagne gold — the only accent in the system
          dark:    '#cfa968', // inferred — source buttons invert, they never darken
          light:   '#eddec5', // inferred
        },
        secondary: {
          DEFAULT: '#f0eeeb', // warm bone
        },
        accent: {
          DEFAULT: '#ceccc5', // warm stone
        },
        ink:      '#131413',
        charcoal: '#2c2e2c',
        white:    '#ffffff', // default button + nav link text — NOT the warm bone

        // Dark-first scale: 800/900 are the page grounds, 100/300 are the text.
        neutral: {
          50:  '#f9f9f9',
          100: '#f0eeeb', // heading text on dark
          200: '#dfddd8', // inferred
          300: '#ceccc5', // default body text on dark
          400: '#a2a29e', // inferred
          500: '#777777',
          600: '#606060', // inferred
          700: '#494949', // decorative display only — ~1.9:1 on the page ground
          800: '#2c2e2c', // page background
          900: '#131413', // section / footer background
        },

        success:   '#46b450', // Contact Form 7 default — not brand-authored
        warning:   '#ffb900', // Contact Form 7 default — not brand-authored
        error:     '#e74c3c', // theme-authored
        'error-alt': '#dc3232', // Contact Form 7 default
        info:      '#00a0d2', // Contact Form 7 default — not brand-authored

        surface: {
          DEFAULT: '#2c2e2c',            // page background
          sunken:  '#131413',            // section grounds, footer
          gold:    '#dec497',            // closing CTA panel
          light:   '#f0eeeb',            // inverted light sections
          overlay: 'rgba(0, 0, 0, 0.4)', // hero image scrim
        },

        // Alpha compositing values used verbatim in the source
        alpha: {
          'white-30': 'rgba(255, 255, 255, 0.3)', // button borders, nav rules
          'bone-30':  'rgba(240, 238, 235, 0.3)', // section-label hairline
          'stone-30': 'rgba(206, 204, 197, 0.3)', // card hairline
          'ink-70':   'rgba(19, 20, 19, 0.7)',
          'ink-20':   'rgba(19, 20, 19, 0.2)',
        },
      },

      fontFamily: {
        // NOTE: the source declares the serif as "Сormorant" with a leading
        // U+0421 CYRILLIC CAPITAL ES — a typo. Latin spelling used here.
        heading: ['Cormorant', 'Georgia', 'Times New Roman', 'serif'],
        body:    ['Raleway', 'system-ui', '-apple-system', 'sans-serif'],
        mono:    ['monospace'], // source defines none
      },

      fontSize: {
        xs:    ['0.75rem',  { lineHeight: '1.5', letterSpacing: '-0.01em' }], // 12px
        sm:    ['0.875rem', { lineHeight: '1.5', letterSpacing: '0' }],       // 14px — uppercase nav/buttons
        base:  ['1rem',     { lineHeight: '1.6', letterSpacing: '-0.01em' }], // 16px
        lg:    ['1.125rem', { lineHeight: '1.5', letterSpacing: '-0.01em' }], // 18px
        xl:    ['1.25rem',  { lineHeight: '1.5', letterSpacing: '-0.01em' }], // 20px
        '2xl': ['1.5rem',   { lineHeight: '1.2', letterSpacing: '-0.02em' }], // 24px
        '3xl': ['1.875rem', { lineHeight: '1.2', letterSpacing: '-0.02em' }], // 30px
        '4xl': ['2.375rem', { lineHeight: '1.2', letterSpacing: '-0.02em' }], // 38px
        '5xl': ['3rem',     { lineHeight: '1.2', letterSpacing: '-0.02em' }], // 48px
        '6xl': ['4.125rem', { lineHeight: '1',   letterSpacing: '-0.02em' }], // 66px
        '7xl': ['5.5rem',   { lineHeight: '1',   letterSpacing: '-0.02em' }], // 88px
        '8xl': ['8rem',     { lineHeight: '1',   letterSpacing: '-0.02em' }], // 128px
      },

      // Only two weights exist. There is NO bold in this system — using
      // 600+ triggers synthetic faux-bold and breaks the identity.
      fontWeight: {
        normal: '400',
        medium: '500',
      },

      lineHeight: {
        none:    '1',    // hero, display
        tight:   '1.2',  // headings
        normal:  '1.5',  // UI, nav, buttons
        relaxed: '1.6',  // body prose
      },

      letterSpacing: {
        tight:  '-0.02em', // display + headings, 24px and up
        snug:   '-0.01em', // body + UI
        normal: '0',       // uppercase nav and buttons
        wide:   '0.05em',  // inferred — not used in source
        wider:  '0.1em',   // inferred — not used in source
      },

      spacing: {
        px:  '1px',
        1:   '4px',
        2:   '8px',
        3:   '12px',
        4:   '16px',
        5:   '20px',
        6:   '24px',
        7:   '28px',
        8:   '32px',
        10:  '40px',
        12:  '50px',  // source uses 50px, not the conventional 48px
        14:  '56px',  // header top padding at rest
        18:  '72px',
        20:  '80px',
        22:  '90px',
        25:  '100px',
        31:  '125px',
        45:  '180px', // the signature section rhythm

        // Named layout tokens — these carry the identity
        gutter:      '15px',
        'header-pad':    '56px',
        'header-height': '100px',
        'section-y':     '180px', // do not reduce to 64–96px
        'section-y-md':  '100px',
        'section-y-sm':  '80px',
        'grid-gap-x':    '180px',
        'grid-gap-y':    '80px',
      },

      // Deliberately sharp: only buttons curve. Everything else is 0.
      borderRadius: {
        none:    '0',      // THE DEFAULT — cards, images, panels, inputs
        sm:      '0',      // intentionally 0
        md:      '0',      // intentionally 0
        lg:      '0',      // intentionally 0
        xl:      '0',      // intentionally 0
        '2xl':   '0',      // intentionally 0
        pill:    '71px',   // buttons — extracted verbatim
        control: '50px',   // swiper control cluster
        circle:  '50%',    // custom cursor, avatars
        full:    '9999px',
      },

      borderWidth: {
        DEFAULT: '1px', // the only border width in the system
      },

      // The source contains NO shadows — only `box-shadow: none`. Depth
      // comes from colour contrast and full-bleed photography. The ramp
      // below is inferred, tinted with brand ink rather than pure black.
      boxShadow: {
        none: 'none', // THE SYSTEM DEFAULT — use this
        sm:   '0 1px 3px 0 rgba(19,20,19,0.24), 0 1px 2px -1px rgba(19,20,19,0.24)',    // inferred
        md:   '0 4px 6px -1px rgba(19,20,19,0.28), 0 2px 4px -2px rgba(19,20,19,0.28)', // inferred
        lg:   '0 10px 15px -3px rgba(19,20,19,0.32), 0 4px 6px -4px rgba(19,20,19,0.32)', // inferred
        xl:   '0 20px 25px -5px rgba(19,20,19,0.38), 0 8px 10px -6px rgba(19,20,19,0.38)', // inferred
      },

      // 300ms is the ONLY duration in the source.
      transitionDuration: {
        instant: '75ms',  // inferred
        fast:    '150ms', // inferred
        normal:  '300ms', // THE SITE STANDARD — use this for everything
        slow:    '400ms', // inferred
        DEFAULT: '300ms',
      },

      transitionTimingFunction: {
        DEFAULT:       'ease', // the source's implicit default
        'ease-in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
        'ease-out':    'cubic-bezier(0, 0, 0.2, 1)', // inferred
        'ease-in':     'cubic-bezier(0.4, 0, 1, 1)', // inferred
      },

      // Source is authored desktop-first with max-width queries;
      // these are the min-width equivalents.
      screens: {
        sm:    '768px',
        md:    '1100px',
        lg:    '1500px',
        xl:    '1520px',
        '2xl': '1920px',
      },

      maxWidth: {
        container: '1440px', // with 15px gutters
        wide:      '1920px', // full-bleed media ceiling
        measure:   '540px',  // editorial prose measure
        'measure-narrow': '360px',
      },

      zIndex: {
        nav:    '100',
        header: '101',
        cursor: '1000',
      },
    },
  },

  plugins: [],
};
