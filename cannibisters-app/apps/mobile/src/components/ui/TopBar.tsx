import type { ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { Icon } from './Icon';

export function TopBar({ title, back, right, children }: { title?: string; back?: boolean | string; right?: ReactNode; children?: ReactNode }) {
  const nav = useNavigate();
  return (
    <header className="topbar">
      {back && (
        <button type="button" className="btn btn--ghost btn--icon" aria-label="Back" onClick={() => (typeof back === 'string' ? nav(back) : nav(-1))} style={{ marginLeft: -8 }}>
          <Icon name="back" />
        </button>
      )}
      {title ? <h1 className="topbar-title">{title}</h1> : <div className="grow">{children}</div>}
      {right}
    </header>
  );
}
