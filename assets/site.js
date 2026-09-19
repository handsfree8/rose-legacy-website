(() => {
  'use strict';
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  const header = document.getElementById('site-header');
  const menu = document.getElementById('menu-btn');
  const nav = document.getElementById('primary-nav');
  if (header && menu && nav) {
    const setMenu = open => {
      header.classList.toggle('menu-open', open);
      menu.setAttribute('aria-expanded', String(open));
      menu.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };
    const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 12);
    onScroll();
    window.addEventListener('scroll', onScroll, {passive: true});
    menu.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
    nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
    document.addEventListener('click', event => {
      if (!header.contains(event.target)) setMenu(false);
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        menu.focus();
      }
    });
    matchMedia('(min-width: 1101px)').addEventListener('change', () => setMenu(false));
  }

  // A native dialog supplies focus containment, Escape, and focus restoration.
  const dialog = document.getElementById('lightbox');
  const items = Array.from(document.querySelectorAll('.gallery-item'));
  if (dialog && items.length) {
    const image = document.getElementById('lb-img');
    const caption = document.getElementById('lb-caption');
    const count = document.getElementById('lb-count');
    let current = 0;
    const render = index => {
      current = (index + items.length) % items.length;
      const item = items[current];
      image.src = item.dataset.img;
      image.alt = item.querySelector('img').alt;
      caption.textContent = item.dataset.tag + ' — ' + item.dataset.label;
      count.textContent = `${current + 1} / ${items.length}`;
    };
    items.forEach((item, index) => item.addEventListener('click', () => {
      render(index);
      dialog.showModal();
      document.body.classList.add('photo-open');
    }));
    document.getElementById('lb-close').addEventListener('click', () => dialog.close());
    document.getElementById('lb-prev').addEventListener('click', () => render(current - 1));
    document.getElementById('lb-next').addEventListener('click', () => render(current + 1));
    dialog.addEventListener('keydown', event => {
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        render(current + (event.key === 'ArrowLeft' ? -1 : 1));
      }
    });
    dialog.addEventListener('click', event => {
      const rect = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
    });
    dialog.addEventListener('close', () => document.body.classList.remove('photo-open'));
  }

  const video = document.getElementById('background-video');
  const control = document.getElementById('video-control');
  if (!video || !control) return;

  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const portrait = matchMedia('(max-aspect-ratio: 4/3)');
  const saveData = navigator.connection?.saveData === true;
  let userPaused = false;
  let requestedMotion = false;
  let hasFailed = false;
  const allowed = () => !userPaused && (requestedMotion || (!reducedMotion.matches && !saveData));
  const sync = () => {
    const paused = video.paused;
    control.querySelector('[data-video-icon]').textContent = paused ? '▶' : 'Ⅱ';
    control.querySelector('[data-video-label]').textContent = paused ? 'Play background' : 'Pause background';
    control.setAttribute('aria-label', paused ? 'Play background video' : 'Pause background video');
  };
  const play = () => {
    if (!hasFailed && !document.hidden) video.play().catch(sync);
  };
  const loadVideo = () => {
    if (hasFailed) return;
    const source = `/assets/media/roselegacy-mainvideo-${portrait.matches ? 'movil' : 'desktop'}.mp4`;
    if (video.getAttribute('src') === source) {
      if (allowed()) play();
      return;
    }
    const time = video.currentTime || 0;
    video.classList.remove('ready');
    video.onloadedmetadata = () => {
      if (Number.isFinite(video.duration)) video.currentTime = Math.min(time, Math.max(0, video.duration - .1));
      if (allowed()) play();
    };
    video.src = source;
    video.load();
  };
  control.hidden = false;
  control.addEventListener('click', () => {
    if (video.paused) {
      requestedMotion = true;
      userPaused = false;
      if (video.getAttribute('src')) play();
      else loadVideo();
    } else {
      userPaused = true;
      video.pause();
    }
  });
  video.addEventListener('playing', () => { video.classList.add('ready'); sync(); });
  video.addEventListener('pause', sync);
  video.addEventListener('error', () => {
    hasFailed = true;
    video.classList.remove('ready');
    control.hidden = true;
  });
  portrait.addEventListener('change', () => {
    if (video.getAttribute('src')) loadVideo();
  });
  reducedMotion.addEventListener('change', event => {
    if (event.matches) {
      requestedMotion = false;
      userPaused = true;
      video.pause();
    }
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) video.pause();
    else if (video.getAttribute('src') && allowed()) play();
  });
  // The responsive poster paints first. Reduced-motion/data-saving visitors
  // download no background video unless they explicitly press Play.
  const start = () => { if (allowed()) loadVideo(); };
  if (document.readyState === 'complete') start();
  else window.addEventListener('load', start, {once: true});
})();
