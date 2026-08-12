/**
 * POST /api/enquiry — server-side validation for the enquiry form.
 *
 * Mirrors the rules in server.py (local dev) and js/main.js (client side), so
 * a submission that passes in the browser passes here, and a submission that
 * skips the browser entirely still gets checked.
 *
 * Set ENQUIRY_FORWARD_URL to forward valid submissions to an email service
 * (Formspree, Resend, Postmark …). Without it the function validates, logs and
 * returns 200 — safe, but nothing is delivered, so set it before launch.
 */

const LIMITS = { name: 120, email: 200, project: 80, message: 4000 };
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const PROJECTS = new Set([
  'Bespoke joinery',
  'Custom fitted wardrobes',
  'Fitted furniture',
  'Not sure yet',
]);

function validate(f) {
  const errors = {};

  for (const [key, limit] of Object.entries(LIMITS)) {
    if ((f[key] || '').length > limit) errors[key] = 'Too long.';
  }

  if (!(f.name || '').trim()) errors.name = 'Please tell us your name.';

  const email = (f.email || '').trim();
  if (!email) errors.email = 'We need an email address to reply to.';
  else if (!EMAIL_RE.test(email)) errors.email = 'That does not look like an email address.';

  if (!f.project) errors.project = 'Please choose the closest project type.';
  else if (!PROJECTS.has(f.project)) errors.project = 'Unrecognised project type.';

  if ((f.message || '').trim().length < 10) {
    errors.message = 'Please tell us a little about the room.';
  }

  return errors;
}

const json = (statusCode, body) => ({
  statusCode,
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
});

export async function handler(event) {
  if (event.httpMethod !== 'POST') {
    return json(405, { error: 'Method not allowed' });
  }
  if ((event.body || '').length > 64000) {
    return json(413, { error: 'Too large' });
  }

  const fields = Object.fromEntries(new URLSearchParams(event.body || ''));

  // Honeypot: accept and discard, so the bot learns nothing from the response.
  if ((fields['company-website'] || '').trim()) {
    return json(200, { ok: true });
  }

  const errors = validate(fields);
  if (Object.keys(errors).length) {
    return json(422, { ok: false, errors });
  }

  const forward = process.env.ENQUIRY_FORWARD_URL;
  if (forward) {
    const res = await fetch(forward, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        name: fields.name.trim(),
        email: fields.email.trim(),
        project: fields.project,
        message: fields.message.trim(),
        _subject: `Website enquiry — ${fields.project}`,
      }),
    });
    if (!res.ok) {
      console.error('Forward failed', res.status, await res.text());
      return json(502, { ok: false, error: 'Could not deliver the enquiry.' });
    }
  } else {
    console.warn('ENQUIRY_FORWARD_URL is not set — enquiry validated but not delivered.');
    console.info('Enquiry', { email: fields.email, project: fields.project });
  }

  return json(200, { ok: true });
}
