import { Link } from 'react-router-dom';
import type { Product } from '@cannibisters/shared';
import { formatRand } from '@/lib/format';
import { useCart } from '@/lib/cart';
import { useToast } from '@/lib/toast';
import { Icon } from './Icon';
import { StrainBadge } from './StrainBadge';

const BADGE_LABEL: Record<string, string> = { new: 'New', special: 'Special', 'app-only': 'App only', limited: 'Limited', 'living-soil': 'Living soil', sotw: 'Of the week', 'low-stock': 'Few left' };

export function ProductCard({ product, width, quickAdd = true }: { product: Product; width?: number | string; quickAdd?: boolean }) {
  const cart = useCart();
  const toast = useToast();
  const badge = product.badges?.find((b) => b !== 'new') ?? product.badges?.[0];
  return (
    <div className="pcard" style={width ? { width } : undefined}>
      <Link to={`/shop/p/${product.handle}`} className="frame frame--square">
        <img src={product.image} alt={product.title} loading="lazy" />
        {badge && <span className={`badge ${badge === 'app-only' ? 'badge--orange' : 'badge--gold'}`} style={{ position: 'absolute', top: 10, left: 10, background: badge === 'app-only' ? undefined : 'var(--card)' }}>{BADGE_LABEL[badge]}</span>}
        {quickAdd && product.available && (
          <button
            type="button"
            aria-label={`Add ${product.title}`}
            onClick={(e) => { e.preventDefault(); cart.add(product); toast.show(`${product.title} added`); }}
            style={{ position: 'absolute', right: 10, bottom: 10, width: 36, height: 36, borderRadius: 999, background: 'var(--nav)', color: 'var(--nav-ink)', display: 'grid', placeItems: 'center', boxShadow: 'var(--shadow)' }}
          >
            <Icon name="plus" size={18} />
          </button>
        )}
      </Link>
      <div className="stack gap-1">
        <StrainBadge type={product.strainType} />
        <Link to={`/shop/p/${product.handle}`} className="pcard-title clamp-2">{product.title}</Link>
        <div className="row between">
          <span className="pcard-price num">{formatRand(product.price)}{product.category === 'flower' && <span className="small mute" style={{ fontFamily: 'var(--font-body)', letterSpacing: 0 }}> /g</span>}</span>
          {!product.available && <span className="tiny mute">Sold out</span>}
        </div>
      </div>
    </div>
  );
}
