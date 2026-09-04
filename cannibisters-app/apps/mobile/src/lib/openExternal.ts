/** Open a URL outside the app shell (system browser / in-app browser under Capacitor). */
export function openExternal(url: string) {
  window.open(url, '_blank', 'noopener,noreferrer');
}
