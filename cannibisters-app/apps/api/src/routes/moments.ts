import { Hono } from 'hono';
import type { Vars } from '../app';

/** moments routes: implemented by the feature build (see docs/cannibisters-app/03-architecture.md). */
export const moments = new Hono<{ Variables: Vars }>();
moments.get('/', (c) => c.json({ message: 'moments: not implemented yet' }, 501));
