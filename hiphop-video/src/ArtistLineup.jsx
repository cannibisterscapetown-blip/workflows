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
const GOLD  = '#C9A84C';
const GREEN = '#39FF14';
const BLACK = '#080808';
const WHITE = '#FFFFFF';

// ─── Helpers ──────────────────────────────────────────────────────────────────
const clamp = (v, lo = 0, hi = 1) => Math.min(hi, Math.max(lo, v));

// ─── Glitch displacement — quick random jitter ────────────────────────────────
function useGlitch(intensity = 1) {
  const frame = useCurrentFrame();
  // fires on specific frames to simulate a glitch beat
  const triggers = [0, 1, 2, 30, 31, 60, 61, 90, 91, 120, 121, 150, 151, 180, 181, 210, 211, 270, 271];
  const active = triggers.includes(frame % 300);
  const dx = active ? (((frame * 7919) % 11) - 5) * intensity : 0;
  const dy = active ? (((frame * 6271) % 7) - 3) * intensity : 0;
  return { dx, dy, active };
}

// ─── RGB-split overlay (glitch aesthetic) ────────────────────────────────────
function RgbSplit({ src, style }) {
  const { active, dx } = useGlitch(2);
  if (!active) return <Img src={src} style={style} />;
  return (
    <div style={{ position: 'relative', width: style.width, height: style.height, overflow: 'hidden' }}>
      <Img src={src} style={{ ...style, position: 'absolute', mixBlendMode: 'screen', filter: 'url(#red)', opacity: 0.85, transform: `translateX(${dx * 1.5}px)` }} />
      <Img src={src} style={{ ...style, position: 'absolute', mixBlendMode: 'screen', filter: 'url(#blue)', opacity: 0.85, transform: `translateX(${-dx}px)` }} />
      <Img src={src} style={{ ...style, position: 'absolute', mixBlendMode: 'normal', opacity: 0.6 }} />
    </div>
  );
}

// ─── VHS scanlines ────────────────────────────────────────────────────────────
function Scanlines() {
  return (
    <AbsoluteFill style={{ pointerEvents: 'none', zIndex: 10 }}>
      <div style={{
        width: '100%',
        height: '100%',
        backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,0,0,0.18) 3px, rgba(0,0,0,0.18) 4px)',
        mixBlendMode: 'multiply',
      }} />
    </AbsoluteFill>
  );
}

// ─── Neon border flash ────────────────────────────────────────────────────────
function NeonBorder({ color = GREEN, startFrame, durationFrames = 40 }) {
  const frame = useCurrentFrame();
  const local = frame - startFrame;
  const op = interpolate(local, [0, 5, durationFrames - 8, durationFrames], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill style={{
      border: `3px solid ${color}`,
      boxShadow: `inset 0 0 40px ${color}22, 0 0 30px ${color}55`,
      opacity: op,
      pointerEvents: 'none',
    }} />
  );
}

// ─── "CANNIBISTERS PRESENTS" intro ────────────────────────────────────────────
function Intro() {
  const frame = useCurrentFrame();

  const presentsOp = interpolate(frame, [5, 20, 50, 62], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  const titleOp = interpolate(frame, [22, 38, 50, 62], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  const { dx, dy } = useGlitch(3);

  return (
    <AbsoluteFill style={{
      background: BLACK,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      gap: 16,
      transform: `translate(${dx}px, ${dy}px)`,
    }}>
      {/* Logo */}
      <Img
        src={staticFile('canni-logo.png')}
        style={{ width: 120, filter: 'brightness(0) invert(1)', opacity: presentsOp }}
      />
      <p style={{
        fontFamily: "'Arial', sans-serif",
        fontSize: 14,
        letterSpacing: 10,
        color: GOLD,
        textTransform: 'uppercase',
        margin: 0,
        opacity: presentsOp,
      }}>
        Presents
      </p>
      <p style={{
        fontFamily: "'Arial Black', Impact, sans-serif",
        fontSize: 52,
        fontWeight: 900,
        color: WHITE,
        textTransform: 'uppercase',
        letterSpacing: -1,
        lineHeight: 1,
        margin: 0,
        opacity: titleOp,
      }}>
        The Lineup
      </p>
      {/* Neon underline */}
      <div style={{
        width: interpolate(frame, [30, 50], [0, 220], { extrapolateRight: 'clamp' }),
        height: 2,
        background: GREEN,
        boxShadow: `0 0 14px ${GREEN}`,
        opacity: titleOp,
      }} />
    </AbsoluteFill>
  );
}

// ─── Single artist reveal slide ───────────────────────────────────────────────
function ArtistSlide({ src, number, enterFrame }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const local = frame - enterFrame;

  // Punch zoom on entry
  const zoomSpring = spring({ frame: local, fps, config: { damping: 12, stiffness: 200 } });
  const scale = interpolate(zoomSpring, [0, 1], [1.18, 1.0]);

  // Fade
  const opacity = interpolate(local, [0, 8], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  // Number counter reveal
  const numOp = interpolate(local, [4, 18], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const numY  = interpolate(local, [4, 18], [30, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  // "ARTIST" label
  const labelOp = interpolate(local, [12, 26], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  // Horizontal slash line
  const slashW = interpolate(local, [8, 28], [0, 100], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  const { dx, dy } = useGlitch(1.5);

  return (
    <AbsoluteFill style={{ opacity, transform: `translate(${dx}px,${dy}px)` }}>
      {/* Full-bleed photo */}
      <Img
        src={staticFile(src)}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          objectPosition: 'center top',
          transform: `scale(${scale})`,
        }}
      />

      {/* Heavy gradient bottom */}
      <AbsoluteFill style={{
        background: 'linear-gradient(180deg, rgba(8,8,8,0.1) 0%, rgba(8,8,8,0.05) 30%, rgba(8,8,8,0.6) 60%, rgba(8,8,8,0.97) 100%)',
      }} />

      {/* Side accent bar */}
      <div style={{
        position: 'absolute',
        left: 36,
        bottom: 180,
        top: '20%',
        width: 3,
        background: `linear-gradient(180deg, transparent, ${GREEN} 40%, ${GOLD})`,
        boxShadow: `0 0 12px ${GREEN}`,
        opacity: labelOp,
      }} />

      {/* Large artist number */}
      <div style={{
        position: 'absolute',
        right: 36,
        bottom: 220,
        fontFamily: "'Arial Black', Impact, sans-serif",
        fontSize: 160,
        fontWeight: 900,
        color: WHITE,
        lineHeight: 1,
        opacity: numOp * 0.08,
        transform: `translateY(${numY}px)`,
        userSelect: 'none',
      }}>
        {number}
      </div>

      {/* Artist label + slash line */}
      <div style={{
        position: 'absolute',
        bottom: 160,
        left: 56,
        opacity: labelOp,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 10 }}>
          <div style={{
            width: `${slashW}%`,
            height: 2,
            background: GREEN,
            boxShadow: `0 0 8px ${GREEN}`,
          }} />
        </div>
        <p style={{
          fontFamily: "'Arial', sans-serif",
          fontSize: 11,
          letterSpacing: 8,
          color: GOLD,
          textTransform: 'uppercase',
          margin: '0 0 6px',
        }}>
          Artist {number}
        </p>
        <p style={{
          fontFamily: "'Arial Black', Impact, sans-serif",
          fontSize: 68,
          fontWeight: 900,
          color: WHITE,
          textTransform: 'uppercase',
          lineHeight: 0.9,
          letterSpacing: -2,
          margin: 0,
        }}>
          Performing
          <br />
          <span style={{ color: GREEN }}>Live</span>
        </p>
      </div>

      <NeonBorder color={number % 2 === 0 ? GOLD : GREEN} startFrame={enterFrame} durationFrames={45} />
    </AbsoluteFill>
  );
}

// ─── Final 2×2 grid reveal ────────────────────────────────────────────────────
function GridFinale({ startFrame }) {
  const frame = useCurrentFrame();
  const local = frame - startFrame;
  const { fps } = useVideoConfig();

  const artists = ['artist1.jpg', 'artist2.jpg', 'artist3.jpg', 'artist4.jpg'];

  const gridOp = interpolate(local, [0, 15], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  // Each quadrant slides in from its corner
  const corners = [
    { dx: -1, dy: -1 }, { dx: 1, dy: -1 },
    { dx: -1, dy:  1 }, { dx: 1, dy:  1 },
  ];

  const logoSpring = spring({ frame: local - 20, fps, config: { damping: 14, stiffness: 80 } });
  const logoScale  = interpolate(logoSpring, [0, 1], [0.5, 1.0]);
  const logoOp     = interpolate(local, [20, 38], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  // Pulsing glow on logo
  const pulse = Math.sin((local / 8) * Math.PI) * 0.5 + 0.5;

  return (
    <AbsoluteFill style={{ opacity: gridOp, background: BLACK }}>
      {/* 2×2 photo grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gridTemplateRows: '1fr 1fr',
        width: '100%',
        height: '100%',
        gap: 3,
      }}>
        {artists.map((src, i) => {
          const sp = spring({ frame: local - i * 6, fps, config: { damping: 18, stiffness: 120 } });
          const tx = interpolate(sp, [0, 1], [corners[i].dx * 60, 0]);
          const ty = interpolate(sp, [0, 1], [corners[i].dy * 60, 0]);
          return (
            <div key={src} style={{ overflow: 'hidden', position: 'relative' }}>
              <Img
                src={staticFile(src)}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover',
                  objectPosition: 'center top',
                  transform: `translate(${tx}px, ${ty}px)`,
                  filter: 'brightness(0.55) saturate(0.8)',
                }}
              />
            </div>
          );
        })}
      </div>

      {/* Dark overlay */}
      <AbsoluteFill style={{
        background: 'radial-gradient(ellipse at center, rgba(8,8,8,0.65) 0%, rgba(8,8,8,0.9) 100%)',
      }} />

      {/* Centre logo + text */}
      <AbsoluteFill style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 14,
        opacity: logoOp,
        transform: `scale(${logoScale})`,
      }}>
        <Img
          src={staticFile('canni-logo.png')}
          style={{
            width: 110,
            filter: `brightness(0) invert(1) drop-shadow(0 0 ${14 * pulse}px ${GREEN})`,
          }}
        />
        <p style={{
          fontFamily: "'Arial', sans-serif",
          fontSize: 11,
          letterSpacing: 9,
          color: GOLD,
          textTransform: 'uppercase',
          margin: 0,
        }}>
          Herbal Apothecary
        </p>
        <div style={{ width: 200, height: 1, background: `linear-gradient(90deg, transparent, ${GOLD}, transparent)` }} />
        <p style={{
          fontFamily: "'Arial Black', Impact, sans-serif",
          fontSize: 58,
          fontWeight: 900,
          color: WHITE,
          textTransform: 'uppercase',
          letterSpacing: -1,
          lineHeight: 0.9,
          textAlign: 'center',
          margin: 0,
        }}>
          Hip Hop<br />
          <span style={{ color: GREEN }}>Night</span>
        </p>
        <p style={{
          fontFamily: "'Arial', sans-serif",
          fontSize: 11,
          letterSpacing: 6,
          color: WHITE,
          opacity: 0.6,
          textTransform: 'uppercase',
          margin: 0,
        }}>
          cannibisters.co.za
        </p>
      </AbsoluteFill>

      <Scanlines />
    </AbsoluteFill>
  );
}

// ─── Timeline ─────────────────────────────────────────────────────────────────
//  0 –  65  : Intro ("Cannibisters Presents / The Lineup")
// 65 – 120  : Artist 1
//120 – 175  : Artist 2
//175 – 230  : Artist 3
//230 – 285  : Artist 4
//285 – 390  : Grid finale + logo lock-up
const TOTAL = 390; // 13 seconds @ 30fps

export const ArtistLineup = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ background: BLACK, overflow: 'hidden' }}>

      {/* Intro */}
      <Sequence from={0} durationInFrames={70}>
        <Intro />
      </Sequence>

      {/* Artist slides — each gets 55 frames with a 5-frame overlap for the glitch cut */}
      <Sequence from={60} durationInFrames={70}>
        <ArtistSlide src="artist1.jpg" number={1} enterFrame={60} />
      </Sequence>
      <Sequence from={115} durationInFrames={70}>
        <ArtistSlide src="artist2.jpg" number={2} enterFrame={115} />
      </Sequence>
      <Sequence from={170} durationInFrames={70}>
        <ArtistSlide src="artist3.jpg" number={3} enterFrame={170} />
      </Sequence>
      <Sequence from={225} durationInFrames={70}>
        <ArtistSlide src="artist4.jpg" number={4} enterFrame={225} />
      </Sequence>

      {/* Grid finale */}
      <Sequence from={285} durationInFrames={TOTAL - 285}>
        <GridFinale startFrame={285} />
      </Sequence>

      {/* Global scanlines */}
      <Scanlines />

      {/* Floating gold/green particles */}
      <AbsoluteFill style={{ pointerEvents: 'none' }}>
        {Array.from({ length: 14 }, (_, i) => {
          const seed  = i * 137.5;
          const x     = ((seed * 23) % 960) + 20;
          const baseY = ((seed * 41) % 1800) + 50;
          const speed = 0.25 + (i % 4) * 0.1;
          const y     = baseY - ((frame * speed) % 2100);
          const size  = 1.5 + (i % 3) * 0.7;
          const delay = (i * 19) % 80;
          const op    = interpolate((frame + delay) % 100, [0, 18, 80, 100], [0, 0.85, 0.85, 0], {
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
              opacity: op * 0.5,
              boxShadow: `0 0 ${size * 4}px ${i % 3 === 0 ? GREEN : GOLD}`,
            }} />
          );
        })}
      </AbsoluteFill>

    </AbsoluteFill>
  );
};
