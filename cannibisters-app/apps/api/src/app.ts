import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { env, isMock } from './env';
import { verifySession, type SessionPayload } from './lib/session';
import { auth } from './routes/auth';
import { catalog } from './routes/catalog';
import { entry } from './routes/entry';
import { misc } from './routes/misc';
import { loyalty } from './routes/loyalty';
import { moments } from './routes/moments';
import { cannisino } from './routes/cannisino';
import { concierge } from './routes/concierge';

export type Vars = { session: SessionPayload };
export type App = Hono<{ Variables: Vars }>;

export function createApp(): App {
  const app = new Hono<{ Variables: Vars }>();
  app.use('*', logger());
  app.use('/api/*', cors({ origin: env.corsOrigin, allowHeaders: ['Authorization', 'Content-Type'] }));

  app.get('/api/health', (c) => c.json({ ok: true, mode: isMock ? 'mock' : 'live' }));

  // Public
  app.route('/api/auth', auth);
  app.route('/api', misc.public);

  // Member-only
  app.use('/api/*', async (c, next) => {
    if (c.req.path.startsWith('/api/auth/') || c.req.path === '/api/health' || c.req.path === '/api/nightowl/status') return next();
    const h = c.req.header('Authorization');
    const token = h?.startsWith('Bearer ') ? h.slice(7) : '';
    const session = isMock && token.startsWith('mock.')
      ? { customerId: 'gid://shopify/Customer/6100000000001', customerAccessToken: 'mock', email: 'demo@cannibisters.com', exp: Number.MAX_SAFE_INTEGER }
      : verifySession(token);
    if (!session) return c.json({ message: 'Sign in to continue.' }, 401);
    c.set('session', session);
    return next();
  });
  app.route('/api/catalog', catalog);
  app.route('/api/entry', entry);
  app.route('/api', misc.member);
  app.route('/api/loyalty', loyalty);
  app.route('/api/moments', moments);
  app.route('/api/cannisino', cannisino);
  app.route('/api/concierge', concierge);

  app.notFound((c) => c.json({ message: 'Not found' }, 404));
  app.onError((err, c) => { console.error(err); return c.json({ message: err.message || 'Something went wrong' }, 500); });
  return app;
}
