import { NavLink } from 'react-router-dom';
import { Icon, type IconName } from './Icon';

const TABS: { to: string; label: string; icon: IconName; entry?: boolean }[] = [
  { to: '/', label: 'Home', icon: 'home' },
  { to: '/shop', label: 'Shop', icon: 'shop' },
  { to: '/entry', label: 'Entry', icon: 'qr', entry: true },
  { to: '/moments', label: 'Moments', icon: 'moments' },
  { to: '/concierge', label: 'Concierge', icon: 'concierge' },
];

export function TabBar() {
  return (
    <nav className="tabbar" aria-label="Primary">
      {TABS.map((t) => (
        <NavLink key={t.to} to={t.to} end={t.to === '/'} className={({ isActive }) => `tab ${t.entry ? 'tab--entry' : ''} ${isActive ? 'tab--active' : ''}`}>
          {t.entry ? <span className="tab-orb"><Icon name={t.icon} /></span> : <Icon name={t.icon} />}
          <span>{t.label}</span>
        </NavLink>
      ))}
    </nav>
  );
}
