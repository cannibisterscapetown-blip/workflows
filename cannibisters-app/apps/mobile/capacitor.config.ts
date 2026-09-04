import type { CapacitorConfig } from '@capacitor/cli';

// Native shells for iOS and Android wrap the built web app in dist/.
// Run `pnpm build && pnpm cap:sync` after changes; `pnpm cap:ios` / `pnpm cap:android` once.
const config: CapacitorConfig = {
  appId: 'com.cannibisters.club',
  appName: 'Cannibisters',
  webDir: 'dist',
  backgroundColor: '#05060c',
  ios: { contentInset: 'always', scheme: 'Cannibisters' },
  android: { allowMixedContent: false },
  server: { androidScheme: 'https' },
};

export default config;
