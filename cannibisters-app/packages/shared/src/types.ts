// Shared domain types for the Cannibisters members app (mobile + BFF).

export type StrainType = 'indica' | 'sativa' | 'hybrid';
export type ProductCategory = 'flower' | 'joint' | 'extract' | 'edible' | 'accessory' | 'membership';
export type ProductBadge = 'new' | 'special' | 'app-only' | 'limited' | 'living-soil' | 'sotw' | 'low-stock';

export interface Product {
  id: string;            // Shopify product gid
  variantId: string;     // default variant gid (used for cart lines)
  handle: string;
  title: string;
  category: ProductCategory;
  price: number;         // ZAR
  compareAtPrice?: number;
  image: string;
  tags: string[];
  description: string;
  strainType?: StrainType;
  profile?: string;      // e.g. "70/30 Indica-Dominant Hybrid"
  lineage?: string;
  flavours?: string;
  effects?: string[];
  thc?: string;
  usedFor?: string;
  available: boolean;
  inventory?: number;
  badges?: ProductBadge[];
}

export interface Collection {
  handle: string;
  title: string;
  image?: string;
  blurb?: string;
  /** Simple client-side rule for mock mode; live mode resolves via Shopify. */
  rule?: { tag?: string; category?: ProductCategory; handles?: string[]; badge?: ProductBadge };
}

export type TierKey = 'silver' | 'gold' | 'platinum' | 'diamond';
export type MembershipStatus = 'active' | 'expired' | 'none';

export interface Member {
  id: string;            // Shopify customer gid
  firstName: string;
  lastName: string;
  email: string;
  memberNumber: number;
  memberSince: string;   // ISO date
  tier: TierKey;
  membership: { status: MembershipStatus; plan: string; expiresAt?: string };
}

export interface PointEvent {
  id: string;
  date: string;          // ISO
  label: string;
  delta: number;
  kind: 'earn' | 'redeem' | 'bonus' | 'expire' | 'game';
}

export interface Reward {
  id: string;
  title: string;
  description: string;
  cost: number;          // points
  kind: 'discount' | 'product' | 'voucher' | 'experience';
  valueRand?: number;
  image?: string;
  appOnly?: boolean;
}

export interface LoyaltySummary {
  points: number;
  pointsValueRand: number;
  tier: TierKey;
  multiplier: number;
  tierProgress: { spend180d: number; nextTier?: TierKey; amountToNext?: number; pct: number };
  expiringSoon?: { points: number; on: string };
  history: PointEvent[];
  rewards: Reward[];
  playWallet: number;    // Cannisino play balance (separate from real points)
  referralCode: string;
}

export interface RedeemResult {
  ok: boolean;
  code?: string;         // discount code to apply at checkout / show in store
  message: string;
  newBalance: number;
}

export interface MomentComment {
  id: string;
  authorName: string;
  text: string;
  createdAt: string;
}

export interface Moment {
  id: string;
  authorName: string;
  authorInitials: string;
  createdAt: string;
  image: string;
  caption: string;
  product?: { handle: string; title: string };
  strainType?: StrainType;
  likes: number;
  likedByMe: boolean;
  comments: MomentComment[];
  location?: string;     // e.g. "The Serenity Room"
  mine?: boolean;
}

export interface NewMomentInput {
  image: string;         // data URL or uploaded asset URL
  caption: string;
  productHandle?: string;
  strainType?: StrainType;
  location?: string;
}

export type SpecialKind = 'app-only' | 'night-owl' | 'monthly' | 'bundle' | 'tier';

export interface Special {
  id: string;
  kind: SpecialKind;
  title: string;
  subtitle: string;
  description: string;
  code?: string;         // discount code applied at checkout
  productHandle?: string;
  collectionHandle?: string;
  image?: string;
  savings?: string;      // "15% off", "Save R80"
  endsAt?: string;
  nudge?: string;        // subtle upsell line
}

export type CannisinoGameKey = 'predictions' | 'claw' | 'mines' | 'wheel';

export interface CannisinoGame {
  key: CannisinoGameKey;
  title: string;
  tagline: string;
  native: boolean;       // rendered in-app (wheel) vs embedded lounge
  minStake?: number;
}

export interface CannisinoSession {
  embedUrl: string;      // https://cannisino.vercel.app/casino?embed_token=...
  playWallet: number;
  expiresAt: string;
}

export interface WheelPrize {
  label: string;
  kind: 'points' | 'discount' | 'product';
  value?: number;
}

export interface ConciergeQuickAction {
  key: 'recommend' | 'reserve' | 'preorder' | 'consult' | 'delivery' | 'human';
  title: string;
  hint: string;
}

export interface ConciergeMessage {
  id: string;
  from: 'member' | 'concierge';
  text: string;
  at: string;
  quickReplies?: string[];
  productHandles?: string[];   // concierge can attach product cards
}

export interface Order {
  id: string;
  name: string;          // "#12345"
  date: string;
  status: 'processing' | 'out-for-delivery' | 'delivered' | 'collected' | 'cancelled';
  total: number;
  items: { title: string; qty: number }[];
  pointsEarned?: number;
}

export interface EntryPass {
  token: string;         // signed payload encoded in the QR
  memberNumber: number;
  name: string;
  tier: TierKey;
  membershipStatus: MembershipStatus;
  issuedAt: string;
  expiresAt: string;     // short-lived; client refreshes before expiry
}

export interface NightOwlStatus {
  active: boolean;
  startHour: number;
  endHour: number;
  timeZone: string;
  discountCode: string;
  discountPct: number;
  nextChangeAt: string;  // ISO of next flip
}

export interface CartLineInput { variantId: string; quantity: number }
export interface CheckoutHandoff { checkoutUrl: string; requiresMembership: boolean; dayPassVariantId: string }
