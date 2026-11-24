import { createFanPlayback, type FanAction, type FanPlaybackOptions } from './fan-playback';
import { fanDefaults } from './fan-layout';

export interface FanGalleryItem {
  src: string;
  alt: string;
  href?: string;
}

export const fanMotionDefaults = {
  entrance: 'stack' as const,
  radius: 18,
  speed: 0.7,
  stagger: 0.09,
  bounce: 0.35,
  hoverSpeed: 0.28,
};

export interface FanVanillaOptions extends Partial<FanPlaybackOptions> {
  showTitle?: boolean;
  title?: string;
  subtitle?: string;
  ariaLabel?: string;
  onLayout?: (info: any) => void;
}

export function initFanGallery(root: HTMLElement, items: FanGalleryItem[], userOptions: FanVanillaOptions = {}) {
  const mergedOptions: FanPlaybackOptions = {
    cardWidth: userOptions.cardWidth ?? fanDefaults.cardWidth,
    aspectRatio: userOptions.aspectRatio ?? fanDefaults.aspectRatio,
    spacing: userOptions.spacing ?? fanDefaults.spacing,
    curve: userOptions.curve ?? fanDefaults.curve,
    tilt: userOptions.tilt ?? fanDefaults.tilt,
    lift: userOptions.lift ?? fanDefaults.lift,
    spread: userOptions.spread ?? fanDefaults.spread,
    stackFrom: userOptions.stackFrom ?? fanDefaults.stackFrom,
    radius: userOptions.radius ?? fanMotionDefaults.radius,
    speed: userOptions.speed ?? fanMotionDefaults.speed,
    stagger: userOptions.stagger ?? fanMotionDefaults.stagger,
    bounce: userOptions.bounce ?? fanMotionDefaults.bounce,
    hoverSpeed: userOptions.hoverSpeed ?? fanMotionDefaults.hoverSpeed,
    trigger: userOptions.trigger ?? 'scroll',
    viewportStart: userOptions.viewportStart ?? 75,
    viewportStartUp: userOptions.viewportStartUp,
    once: userOptions.once ?? true,
  };

  root.className = 'fan-gallery' + (root.className ? ' ' + root.className : '');
  root.setAttribute('aria-label', userOptions.ariaLabel || 'Fan gallery');

  let headingHtml = '';
  if (userOptions.showTitle && (userOptions.title || userOptions.subtitle)) {
    headingHtml = `<header class="fan-gallery-heading">
      ${userOptions.title ? `<h2>${userOptions.title}</h2>` : ''}
      ${userOptions.subtitle ? `<p>${userOptions.subtitle}</p>` : ''}
    </header>`;
  }

  const cardsHtml = items
    .map((item, i) => {
      const img = `<img src="${item.src}" alt="${item.alt || `Image ${i + 1}`}" draggable="false" loading="lazy" decoding="async" />`;
      if (item.href) {
        return `<a class="fan-gallery-card" href="${item.href}" aria-label="${item.alt || `Image ${i + 1}`}">${img}</a>`;
      }
      return `<button class="fan-gallery-card" type="button" aria-label="${item.alt || `Image ${i + 1}`}">${img}</button>`;
    })
    .join('');

  root.innerHTML = `${headingHtml}<div class="fan-gallery-stage">${cardsHtml}</div>`;

  const stage = root.querySelector<HTMLDivElement>('.fan-gallery-stage')!;
  const cardElements = Array.from(root.querySelectorAll<HTMLButtonElement | HTMLAnchorElement>('.fan-gallery-card'));

  const pending = { current: null as FanAction | null };
  const controller = createFanPlayback(root, stage, cardElements, mergedOptions, pending, userOptions.onLayout);

  stage.addEventListener('pointermove', (event) => {
    if (event.pointerType === 'touch') return;
    controller.point(event.clientX, event.clientY);
  });

  stage.addEventListener('pointerleave', () => {
    const focused = cardElements.findIndex((node) => node === document.activeElement);
    controller.activate(focused);
  });

  stage.addEventListener('blur', (event) => {
    const related = event.relatedTarget as Node | null;
    if (!stage.contains(related)) {
      controller.activate(-1);
    }
  }, true);

  cardElements.forEach((card, i) => {
    card.addEventListener('focus', () => controller.activate(i));
    card.addEventListener('click', () => controller.activate(i));
    card.addEventListener('keydown', (event) => {
      let next = -1;
      if (event.key === 'ArrowRight') next = (i + 1) % items.length;
      else if (event.key === 'ArrowLeft') next = (i - 1 + items.length) % items.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = items.length - 1;

      if (next >= 0) {
        event.preventDefault();
        cardElements[next]?.focus({ preventScroll: true });
      }
      if (event.key === 'Escape') {
        controller.activate(-1);
        card.blur();
      }
    });
  });

  return controller;
}

if (typeof window !== 'undefined') {
  (window as any).initFanGallery = initFanGallery;
}
