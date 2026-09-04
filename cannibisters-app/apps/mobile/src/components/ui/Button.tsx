import type { ButtonHTMLAttributes, ReactNode } from 'react';
import { Link } from 'react-router-dom';

type Variant = 'primary' | 'gold' | 'dark' | 'outline' | 'outline-gold' | 'ghost';
interface Props extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'children'> {
  variant?: Variant; size?: 'sm' | 'md' | 'lg'; block?: boolean; pill?: boolean; to?: string; href?: string; loading?: boolean; children: ReactNode; icon?: ReactNode;
}

export function Button({ variant = 'primary', size = 'md', block, pill, to, href, loading, children, icon, className = '', ...rest }: Props) {
  const cls = ['btn', `btn--${variant}`, size !== 'md' ? `btn--${size}` : '', block ? 'btn--block' : '', pill ? 'btn--pill' : '', className].filter(Boolean).join(' ');
  const inner = <>{icon}{loading ? 'One moment' : children}</>;
  if (to) return <Link to={to} className={cls}>{inner}</Link>;
  if (href) return <a href={href} target="_blank" rel="noopener noreferrer" className={cls}>{inner}</a>;
  return <button type="button" className={cls} disabled={loading || rest.disabled} {...rest}>{inner}</button>;
}
