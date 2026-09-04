import type { StrainType } from './types';

const INDICA = /\bindica\b/i;
const SATIVA = /\bsativa\b/i;
const HYBRID = /\bhybrid\b/i;
const DOMINANT = /(indica|sativa)[\s-]*dominant/i;

/**
 * Derive the strain type Cannibisters shows on a product from its Shopify tags
 * and (optionally) the `my_fields.profile` metafield.
 *
 * Rules, in order:
 *  1. An explicit "Indica-Dominant" / "Sativa-Dominant" tag or profile wins.
 *  2. A "Balanced" or "50/50" tag or profile means hybrid.
 *  3. If both Indica and Sativa tags are present the product is a hybrid.
 *  4. Otherwise the single Indica / Sativa / Hybrid tag decides.
 *  5. Fall back to the profile text, then undefined (not a strain product).
 */
export function deriveStrainType(tags: readonly string[], profile?: string | null): StrainType | undefined {
  const all = [...tags, profile ?? ''].filter(Boolean);
  for (const t of all) {
    const m = t.match(DOMINANT);
    if (m) return m[1]!.toLowerCase() as StrainType;
  }
  const joined = all.join(' ');
  if (/\bbalanced\b|50\s*\/\s*50/i.test(joined)) return 'hybrid';
  const hasIndica = tags.some((t) => INDICA.test(t));
  const hasSativa = tags.some((t) => SATIVA.test(t));
  const hasHybrid = tags.some((t) => HYBRID.test(t));
  if (hasIndica && hasSativa) return 'hybrid';
  if (hasHybrid) return 'hybrid';
  if (hasIndica) return 'indica';
  if (hasSativa) return 'sativa';
  if (profile) {
    if (HYBRID.test(profile)) return 'hybrid';
    if (INDICA.test(profile)) return 'indica';
    if (SATIVA.test(profile)) return 'sativa';
  }
  return undefined;
}

export const STRAIN_LABEL: Record<StrainType, string> = {
  indica: 'Indica',
  sativa: 'Sativa',
  hybrid: 'Hybrid',
};

/** One-line member-facing hint per type, in brand voice. */
export const STRAIN_HINT: Record<StrainType, string> = {
  indica: 'Settles the body. Evenings, slow music, early nights.',
  sativa: 'Lifts the mind. Daytime, creative work, good company.',
  hybrid: 'Balanced. A little of both, whichever way the day leans.',
};
