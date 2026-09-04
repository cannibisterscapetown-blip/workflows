import { STRAIN_LABEL, type StrainType } from '@cannibisters/shared';

export function StrainBadge({ type, className = '' }: { type?: StrainType; className?: string }) {
  if (!type) return null;
  return <span className={`type type--${type} ${className}`}>{STRAIN_LABEL[type]}</span>;
}
