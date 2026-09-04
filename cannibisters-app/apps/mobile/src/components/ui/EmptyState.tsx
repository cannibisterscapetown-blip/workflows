import type { ReactNode } from 'react';
import { Emblem } from './Emblem';

export function EmptyState({ title, body, action }: { title: string; body?: string; action?: ReactNode }) {
  return (
    <div className="stack center gap-3" style={{ padding: '48px 20px', textAlign: 'center' }}>
      <Emblem size={44} color="var(--gold)" opacity={0.6} />
      <h3 className="display display-md">{title}</h3>
      {body && <p className="body mute" style={{ maxWidth: 300 }}>{body}</p>}
      {action}
    </div>
  );
}
