import { Composition } from 'remotion';
import { HipHopNight } from './HipHopNight';
import { ArtistLineup } from './ArtistLineup';

export const RemotionRoot = () => {
  return (
    <>
      {/* 1:1 square — Instagram feed */}
      <Composition
        id="HipHopNight"
        component={HipHopNight}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1080}
      />
      {/* 9:16 — Stories / Reels */}
      <Composition
        id="HipHopNightStories"
        component={HipHopNight}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1920}
      />
      {/* 9:16 Reels — Artist Lineup reveal (13 s) */}
      <Composition
        id="ArtistLineup"
        component={ArtistLineup}
        durationInFrames={390}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
