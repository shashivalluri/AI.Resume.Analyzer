import { FanGallery } from './fan-gallery';

// Project images tailored for AI Resume Analyzer (replaces demo paths)
export const items = [
  {
    src: '/assets/cards/ats-score.webp',
    alt: 'AI Resume Analyzer ATS Score & Compatibility Overview',
  },
  {
    src: '/assets/cards/skill-gap.webp',
    alt: 'Skill Gap Taxonomy & Requirement Matching',
  },
  {
    src: '/assets/cards/resume-preview.webp',
    alt: 'Executive Resume Structure and Section Breakdown',
  },
  {
    src: '/assets/cards/improvements.webp',
    alt: 'Actionable Bullet Point Improvements and Score Boost',
  },
  {
    src: '/assets/cards/job-recommendations.webp',
    alt: 'Target Role Recommendations and Alignment',
  },
];

export function Example() {
  return (
    <FanGallery
      items={items}
      cardWidth={162}
      aspectRatio={0.8}
      spacing={0.69}
      curve={0.14}
      tilt={14.5}
      lift={42}
      spread={0.2}
      stackFrom={'left'}
      speed={0.7}
      stagger={0.09}
      bounce={0.35}
      hoverSpeed={0.28}
      radius={18}
      entrance={'stack'}
      trigger={'scroll'}
      viewportStart={75}
      once={true}
      showTitle={false}
    />
  );
}

export default Example;
