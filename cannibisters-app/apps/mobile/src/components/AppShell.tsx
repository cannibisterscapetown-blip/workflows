import { Outlet, useMatches } from 'react-router-dom';
import { TabBar } from './ui/TabBar';
import NightOwlTakeover from '@/features/nightowl/NightOwlTakeover';

/** Layout for signed-in routes: content + tab bar + Night Owl takeover overlay. */
export default function AppShell() {
  const matches = useMatches();
  const hideTab = matches.some((m) => (m.handle as { hideTab?: boolean } | undefined)?.hideTab);
  return (
    <>
      <Outlet />
      {!hideTab && <TabBar />}
      <NightOwlTakeover />
    </>
  );
}
