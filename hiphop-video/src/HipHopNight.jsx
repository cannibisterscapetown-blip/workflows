import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  staticFile,
  Sequence,
} from 'remotion';

// ─── Brand colours ────────────────────────────────────────────────────────────
const GOLD   = '#C9A84C';
const GREEN  = '#39FF14';   // matches the store neon
const BLACK  = '#080808';
const WHITE  = '#FFFFFF';

// ─── Easing helper ────────────────────────────────────────────────────────────
const clamp = (v, lo = 0, hi = 1) => Math.min(hi, Math.max(lo, v));

// ─── Single full-bleed photo with Ken-Burns + slide-in ───────────────────────
function PhotoSlide({ src, direction = 'left', startFrame, endFrame }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localFrame = frame - startFrame;
  const duration   = endFrame - startFrame;

  // Fade in / fade out
  const opacity = interpolate(
    localFrame,
    [0, 12, duration - 14, duration],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  // Slide in from left or right
  const slideSpring = spring({ frame: localFrame, fps, config: { damping: 20, stiffness: 90 } });
  const slideX = interpolate(slideSpring, [0, 1], [direction === 'left' ? -80 : 80, 0]);

  // Subtle Ken-Burns drift
  const kbX = interpolate(localFrame, [0, duration], [0, direction === 'left' ? -18 : 18], {
    extrapolateRight: 'clamp',
  });
  const kbScale = interpolate(localFrame, [0, duration], [1.06, 1.0], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ opacity, overflow: 'hidden' }}>
      <Img
        src={staticFile(src)}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          objectPosition: 'center',
          transform: `translateX(${slideX + kbX}px) scale(${kbScale})`,
        }}
      />
      {/* Dark vignette so text pops */}
      <AbsoluteFill
        style={{
          background:
            'linear-gradient(180deg, rgba(8,8,8,0.45) 0%, rgba(8,8,8,0.15) 40%, rgba(8,8,8,0.75) 80%, rgba(8,8,8,0.95) 100%)',
        }}
      />
    </AbsoluteFill>
  );
}

// ─── Animated green scan-line (hip-hop TV glitch feel) ───────────────────────
function ScanLine() {
  const frame = useCurrentFrame();
  const y = ((frame * 4) % 1100) - 10;
  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        top: y,
        height: 2,
        background: `linear-gradient(90deg, transparent, ${GREEN}66, transparent)`,
        pointerEvents: 'none',
      }}
    />
  );
}

// ─── Gold + Green corner brackets ────────────────────────────────────────────
function CornerBrackets({ startFrame }) {
  const frame = useCurrentFrame();
  const progress = interpolate(frame - startFrame, [0, 30], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const size = 48;
  const thickness = 3;
  const offset = 24;

  const corners = [
    { top: offset, left: offset, borderTop: thickness, borderLeft: thickness, borderRadius: '4px 0 0 0' },
    { top: offset, right: offset, borderTop: thickness, borderRight: thickness, borderRadius: '0 4px 0 0' },
    { bottom: offset, left: offset, borderBottom: thickness, borderLeft: thickness, borderRadius: '0 0 0 4px' },
    { bottom: offset, right: offset, borderBottom: thickness, borderRight: thickness, borderRadius: '0 0 4px 0' },
  ];

  return (
    <>
      {corners.map((style, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            width: size * progress,
            height: size * progress,
            borderStyle: 'solid',
            borderColor: GOLD,
            borderWidth: 0,
            opacity: progress,
            ...style,
          }}
        />
      ))}
    </>
  );
}

// ─── Logo ─────────────────────────────────────────────────────────────────────
function Logo({ startFrame }) {
  const frame = useCurrentFrame();
  const progress = spring({
    frame: frame - startFrame,
    fps: 30,
    config: { damping: 18, stiffness: 100 },
  });
  const y  = interpolate(progress, [0, 1], [-24, 0]);
  const op = interpolate(frame - startFrame, [0, 18], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <div
      style={{
        position: 'absolute',
        top: 52,
        left: 0,
        right: 0,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        transform: `translateY(${y}px)`,
        opacity: op,
      }}
    >
      <Img
        src={staticFile('canni-logo.png')}
        style={{ width: 100, height: 'auto', filter: 'brightness(0) invert(1)' }}
      />
      <p style={{
        fontFamily: "'Arial Black', Arial, sans-serif",
        fontSize: 10,
        fontWeight: 400,
        letterSpacing: 7,
        color: GOLD,
        textTransform: 'uppercase',
        margin: '5px 0 0',
      }}>
        Herbal Apothecary
      </p>
    </div>
  );
}

// ─── "HIP HOP NIGHT" title block ─────────────────────────────────────────────
function Title({ startFrame }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const wordProgress = (delay) => spring({
    frame: frame - startFrame - delay,
    fps,
    config: { damping: 14, stiffness: 120 },
  });

  const hipP  = wordProgress(0);
  const hopP  = wordProgress(8);
  const nightP = wordProgress(16);

  const wordStyle = (progress, color = WHITE) => ({
    display: 'block',
    fontFamily: "'Arial Black', 'Impact', Arial, sans-serif",
    fontSize: 94,
    fontWeight: 900,
    color,
    textTransform: 'uppercase',
    lineHeight: 0.88,
    letterSpacing: -3,
    margin: 0,
    transform: `translateX(${interpolate(progress, [0, 1], [-60, 0])}px)`,
    opacity: clamp(progress * 3),
  });

  return (
    <div style={{
      position: 'absolute',
      bottom: 210,
      left: 0,
      right: 0,
      padding: '0 48px',
    }}>
      {/* Green accent line */}
      <div style={{
        width: interpolate(frame - startFrame, [0, 20], [0, 72], { extrapolateRight: 'clamp' }),
        height: 3,
        background: GREEN,
        marginBottom: 16,
        boxShadow: `0 0 12px ${GREEN}`,
      }} />

      <span style={wordStyle(hipP)}>Hip</span>
      <span style={wordStyle(hopP)}>Hop</span>
      <span style={wordStyle(nightP, GOLD)}>Night</span>
    </div>
  );
}

// ─── Subtitle line ────────────────────────────────────────────────────────────
function Subtitle({ startFrame }) {
  const frame = useCurrentFrame();
  const op = interpolate(frame - startFrame, [0, 22], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const y = interpolate(frame - startFrame, [0, 22], [14, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{
      position: 'absolute',
      bottom: 170,
      left: 0,
      right: 0,
      padding: '0 48px',
      opacity: op,
      transform: `translateY(${y}px)`,
    }}>
      <p style={{
        fontFamily: "'Arial', sans-serif",
        fontSize: 15,
        fontWeight: 400,
        letterSpacing: 5,
        color: WHITE,
        textTransform: 'uppercase',
        margin: 0,
        opacity: 0.8,
      }}>
        Live music · Premium cannabis · Good vibes
      </p>
    </div>
  );
}

// ─── Bottom CTA bar ───────────────────────────────────────────────────────────
function CtaBar({ startFrame }) {
  const frame = useCurrentFrame();
  const progress = spring({
    frame: frame - startFrame,
    fps: 30,
    config: { damping: 18, stiffness: 100 },
  });
  const y  = interpolate(progress, [0, 1], [80, 0]);
  const op = clamp(progress * 2);

  return (
    <div style={{
      position: 'absolute',
      bottom: 0,
      left: 0,
      right: 0,
      height: 76,
      background: `linear-gradient(90deg, ${BLACK} 0%, #1a1a1a 50%, ${BLACK} 100%)`,
      borderTop: `2px solid ${GOLD}`,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 48px',
      transform: `translateY(${y}px)`,
      opacity: op,
    }}>
      <p style={{
        fontFamily: "'Arial Black', Arial, sans-serif",
        fontSize: 13,
        fontWeight: 700,
        letterSpacing: 6,
        color: GOLD,
        textTransform: 'uppercase',
        margin: 0,
      }}>
        cannibisters.co.za
      </p>
      <p style={{
        fontFamily: "'Arial', sans-serif",
        fontSize: 12,
        fontWeight: 400,
        letterSpacing: 4,
        color: WHITE,
        textTransform: 'uppercase',
        margin: 0,
        opacity: 0.7,
      }}>
        @cannibisters
      </p>
    </div>
  );
}

// ─── Floating gold particles ──────────────────────────────────────────────────
function Particles() {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      {Array.from({ length: 18 }, (_, i) => {
        const seed  = i * 137.508;
        const x     = ((seed * 23) % 980) + 10;
        const baseY = ((seed * 41) % 900) + 50;
        const speed = 0.3 + (i % 5) * 0.12;
        const y     = baseY - ((frame * speed) % 1080);
        const size  = 1.5 + (i % 4) * 0.8;
        const delay = (i * 17) % 60;
        const op    = interpolate((frame + delay) % 90, [0, 20, 70, 90], [0, 0.9, 0.9, 0], {
          extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
        });

        return (
          <div key={i} style={{
            position: 'absolute',
            left: x,
            top: y,
            width: size,
            height: size,
            borderRadius: '50%',
            background: i % 3 === 0 ? GREEN : GOLD,
            opacity: op * 0.6,
            boxShadow: `0 0 ${size * 3}px ${i % 3 === 0 ? GREEN : GOLD}`,
          }} />
        );
      })}
    </AbsoluteFill>
  );
}

// ─── Photo slideshow — 4 shots, each ~60 frames (2s), overlapping ─────────────
const SLIDES = [
  { src: 'artist1.jpg', direction: 'left',  start: 0,   end: 90  },
  { src: 'artist2.jpg', direction: 'right', start: 75,  end: 160 },
  { src: 'artist3.jpg', direction: 'left',  start: 145, end: 230 },
  { src: 'artist4.jpg', direction: 'right', start: 215, end: 300 },
];

// ─── Main composition ─────────────────────────────────────────────────────────
export const HipHopNight = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ background: BLACK, overflow: 'hidden' }}>
      {/* Sliding photos */}
      {SLIDES.map((slide) => (
        <Sequence key={slide.src} from={slide.start} durationInFrames={slide.end - slide.start + 20}>
          <PhotoSlide {...slide} />
        </Sequence>
      ))}

      {/* Overlaid effects */}
      <ScanLine />
      <Particles />
      <CornerBrackets startFrame={10} />

      {/* Text layers */}
      <Logo startFrame={8} />
      <Title startFrame={30} />
      <Subtitle startFrame={70} />
      <CtaBar startFrame={85} />
    </AbsoluteFill>
  );
};
