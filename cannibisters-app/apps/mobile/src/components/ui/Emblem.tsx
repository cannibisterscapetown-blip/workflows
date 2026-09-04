/** The Cannibisters gold leaf mark (simplified from the logo's ornate leaf). */
export function Emblem({ size = 40, color = 'currentColor', opacity = 1, className }: { size?: number; color?: string; opacity?: number; className?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 100 100" className={className} style={{ opacity }} aria-hidden="true">
      <g fill={color} transform="translate(50 54)">
        <ellipse rx="5" ry="27" transform="translate(0 -20)" />
        <ellipse rx="5" ry="24" transform="rotate(-36) translate(0 -18)" />
        <ellipse rx="5" ry="24" transform="rotate(36) translate(0 -18)" />
        <ellipse rx="4.2" ry="19" transform="rotate(-74) translate(0 -13)" />
        <ellipse rx="4.2" ry="19" transform="rotate(74) translate(0 -13)" />
        <ellipse rx="3.4" ry="12" transform="rotate(-110) translate(0 -7)" />
        <ellipse rx="3.4" ry="12" transform="rotate(110) translate(0 -7)" />
        <rect x="-1.3" y="6" width="2.6" height="26" rx="1.3" />
        <path d="M-14 26c-6 0-9 5-4 8 3 2 6-1 6-4M14 26c6 0 9 5 4 8-3 2-6-1-6-4" fill="none" stroke={color} strokeWidth="2.2" strokeLinecap="round" />
      </g>
    </svg>
  );
}

export function Wordmark({ size = 14, color = 'currentColor' }: { size?: number; color?: string }) {
  return (
    <span style={{ fontFamily: 'var(--font-display)', fontSize: size * 1.6, letterSpacing: '.18em', color, lineHeight: 1 }}>CANNIBISTERS</span>
  );
}
