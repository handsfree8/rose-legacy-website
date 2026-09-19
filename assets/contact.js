(() => {
  'use strict';
  const form = document.getElementById('service-request');
  const notice = document.getElementById('request-notice');
  if (!form || !notice) return;
  const title = document.getElementById('request-notice-title');
  const message = document.getElementById('request-notice-message');
  const button = form.querySelector('button[type="submit"]');
  const buttonLabel = document.getElementById('request-submit-label');
  let pending = false;
  document.getElementById('request-notice-close').addEventListener('click', () => {
    notice.hidden = true;
    button.focus();
  });
  const show = (state, heading, text) => {
    notice.dataset.state = state;
    title.textContent = heading;
    message.textContent = text;
    notice.hidden = false;
  };
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (pending || !form.reportValidity()) return;
    const payload = Object.fromEntries(new FormData(form).entries());
    delete payload._next; // AJAX confirms here; the native fallback still has a return page.
    pending = true;
    const controls = [...form.querySelectorAll('input, select, textarea, button[type="submit"]')];
    const disabled = controls.map(control => control.disabled);
    controls.forEach(control => { control.disabled = true; });
    const label = buttonLabel.textContent;
    buttonLabel.textContent = 'Sending…';
    form.setAttribute('aria-busy', 'true');
    show('sending', 'Sending your request…', 'Please keep this page open for confirmation.');
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 20000);
    try {
      const response = await fetch('https://formsubmit.co/ajax/roselegacyhs@icloud.com', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
        body: JSON.stringify(payload),
        signal: controller.signal
      });
      if (!response.ok) throw new Error('Request failed');
      const result = await response.json();
      if (result.success !== true && result.success !== 'true') throw new Error('Request not accepted');
      form.reset();
      show('success', 'Your request has been sent.', "Thank you for reaching out. We'll contact you to discuss the next steps and confirm an appointment.");
    } catch {
      // A timeout can occur after acceptance, so do not claim the request was not sent.
      show('error', "We couldn't confirm your submission.", 'Your details are still here. You can try again, or call (816) 298-4828 to confirm whether we received your request.');
    } finally {
      clearTimeout(timeout);
      pending = false;
      controls.forEach((control, index) => { control.disabled = disabled[index]; });
      buttonLabel.textContent = label;
      form.removeAttribute('aria-busy');
    }
  });
})();
