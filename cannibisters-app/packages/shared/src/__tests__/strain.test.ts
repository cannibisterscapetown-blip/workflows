import { describe, it, expect } from 'vitest';
import { deriveStrainType } from '../strain';

describe('deriveStrainType', () => {
  it('prefers explicit dominance tags', () => {
    expect(deriveStrainType(['Hybrid', 'Sativa', 'Sativa-Dominant'])).toBe('sativa');
    expect(deriveStrainType(['Indica', 'Indica-Dominant', 'Flower'])).toBe('indica');
  });
  it('treats balanced and 50/50 as hybrid', () => {
    expect(deriveStrainType(['Balanced', 'Flower'])).toBe('hybrid');
    expect(deriveStrainType(['Flower'], '50/50 Hybrid')).toBe('hybrid');
  });
  it('treats indica + sativa together as hybrid', () => {
    expect(deriveStrainType(['Indica', 'Sativa'])).toBe('hybrid');
  });
  it('uses the single type tag', () => {
    expect(deriveStrainType(['Sativa', 'Flower'])).toBe('sativa');
    expect(deriveStrainType(['indica'])).toBe('indica');
  });
  it('falls back to the profile text', () => {
    expect(deriveStrainType(['Flower'], '90/10 Sativa-dominant')).toBe('sativa');
    expect(deriveStrainType(['Vapes'], 'Sativa')).toBe('sativa');
  });
  it('returns undefined for non-strain products', () => {
    expect(deriveStrainType(['Accessories'])).toBeUndefined();
  });
});
