import { Link } from 'react-router-dom';
import { Icon } from './Icon';

export function SectionHeader({ eyebrow, title, sub, to, action = 'See all' }: { eyebrow?: string; title: string; sub?: string; to?: string; action?: string }) {
  return (
    <div className="row between" style={{ alignItems: 'flex-end', marginBottom: 12 }}>
      <div className="stack gap-1">
        {eyebrow && <span className="eyebrow">{eyebrow}</span>}
        <h2 className="display display-md">{title}</h2>
        {sub && <p className="small mute">{sub}</p>}
      </div>
      {to && <Link to={to} className="row gap-1 small" style={{ color: 'var(--gold-2)', fontWeight: 700 }}>{action}<Icon name="chevron" size={16} /></Link>}
    </div>
  );
}
