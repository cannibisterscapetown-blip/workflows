import type { SVGProps } from 'react';

const P: Record<string, string> = {
  home: 'M3 11.5 12 4l9 7.5M5 10v10h5v-6h4v6h5V10',
  shop: 'M4 8h16l-1 12H5L4 8Zm4 0V6a4 4 0 0 1 8 0v2',
  qr: 'M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h2v2h-2zM18 14h2v2h-2zM14 18h2v2h-2zM18 18h2v2h-2zM6.5 6.5h1v1h-1zM16.5 6.5h1v1h-1zM6.5 16.5h1v1h-1z',
  moments: 'M4 7h3l2-2h6l2 2h3v12H4V7Zm8 3.5a3 3 0 1 0 0 6 3 3 0 0 0 0-6Z',
  concierge: 'M4 6h16v10H9l-5 4V6Zm4 4h8M8 13h5',
  back: 'M15 5l-7 7 7 7',
  chevron: 'M9 5l7 7-7 7',
  down: 'M5 9l7 7 7-7',
  cart: 'M3 4h2l2.5 11h11L21 7H6.5M9 20a1 1 0 1 0 0-2 1 1 0 0 0 0 2Zm9 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z',
  search: 'M11 4a7 7 0 1 0 0 14 7 7 0 0 0 0-14Zm9 16-4-4',
  heart: 'M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10Z',
  comment: 'M4 5h16v11h-8l-4 3v-3H4V5Z',
  plus: 'M12 5v14M5 12h14',
  minus: 'M5 12h14',
  close: 'M6 6l12 12M18 6 6 18',
  check: 'M5 12l5 5 9-11',
  star: 'M12 3l2.8 6 6.2.7-4.6 4.3 1.3 6.3L12 17l-5.7 3.3 1.3-6.3L3 9.7 9.2 9 12 3Z',
  spark: 'M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6',
  clock: 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Zm0-13v5l3 2',
  pin: 'M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11Zm0-9a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z',
  share: 'M12 3v12M8 7l4-4 4 4M5 13v7h14v-7',
  flag: 'M5 21V4h11l-1.5 3.5L16 11H5',
  camera: 'M4 8h3l2-3h6l2 3h3v11H4V8Zm8 2.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7Z',
  gift: 'M3 9h18v4H3zM5 13v8h14v-8M12 9v12M12 9c-2-4-6-3-6-1s3 1 6 1Zm0 0c2-4 6-3 6-1s-3 1-6 1Z',
  dice: 'M4 4h16v16H4zM8 8h.01M16 8h.01M12 12h.01M8 16h.01M16 16h.01',
  arrow: 'M4 12h16m-6-6 6 6-6 6',
  user: 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm-8 9a8 8 0 0 1 16 0',
  settings: 'M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm7-3 2 1.2-2 3.4-2.2-.6a7 7 0 0 1-1.8 1l-.4 2.3h-4l-.4-2.3a7 7 0 0 1-1.8-1l-2.2.6-2-3.4L5 12l-2-1.2 2-3.4 2.2.6a7 7 0 0 1 1.8-1L9.4 4.7h4l.4 2.3a7 7 0 0 1 1.8 1l2.2-.6 2 3.4L19 12Z',
  info: 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Zm0-10v5m0-8h.01',
  external: 'M14 4h6v6M20 4l-9 9M18 13v7H4V6h7',
  sun: 'M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10Zm0-15v2m0 16v2M2 12h2m16 0h2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4',
  moon: 'M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5Z',
  whatsapp: 'M4 20l1.3-3.8A8 8 0 1 1 8 18.8L4 20Zm5.5-10.5c.3 2 2 3.7 4 4l1-1-1.7-1-.8.5c-.6-.4-1.1-.9-1.5-1.5l.5-.8-1-1.7-.5.5Z',
  leaf: 'M12 21c0-6 2-11 8-16-6 1-11 5-11 12 0 1.5.3 2.8 1 4h2ZM12 21c0-6-2-11-8-16 6 1 11 5 11 12',
  owl: 'M12 4c4 0 7 3 7 7v9l-3-2-4 2-4-2-3 2v-9c0-4 3-7 7-7Zm-3 7a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm6 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm-3 1 1.5 2h-3L12 12Z',
  trophy: 'M8 4h8v5a4 4 0 0 1-8 0V4Zm-4 1h4v3a3 3 0 0 1-3-3Zm16 0h-4v3a3 3 0 0 0 3-3ZM12 13v4m-4 4h8',
  bag: 'M6 8h12l1 12H5L6 8Zm3 0V6a3 3 0 0 1 6 0v2',
  truck: 'M3 6h11v10H3zM14 9h4l3 3v4h-7M7 19a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm11 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z',
  logout: 'M10 4H5v16h5M14 8l4 4-4 4M18 12H9',
  bell: 'M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15L6 16Zm4 4a2 2 0 0 0 4 0',
  send: 'M4 12 20 4l-4 16-4-7-8-1Z',
  image: 'M4 5h16v14H4zM8 11a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm-4 8 5-5 3 3 3-4 5 6',
  eye: 'M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Zm10 3a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z',
  refresh: 'M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5',
  calendar: 'M4 6h16v14H4zM4 10h16M8 3v4m8-4v4',
  doctor: 'M9 3v5a3 3 0 0 0 6 0V3M12 11v4m0 0a3 3 0 1 0 0 6 3 3 0 0 0 0-6Z',
  ticket: 'M4 8a2 2 0 0 0 2-2h12a2 2 0 0 0 2 2v2a2 2 0 0 0 0 4v2a2 2 0 0 0-2 2H6a2 2 0 0 0-2-2v-2a2 2 0 0 0 0-4V8Zm6-2v12',
};

export type IconName = keyof typeof P;

export function Icon({ name, size = 22, filled = false, ...rest }: { name: IconName; size?: number; filled?: boolean } & SVGProps<SVGSVGElement>) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill={filled ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" {...rest}>
      <path d={P[name]} />
    </svg>
  );
}
