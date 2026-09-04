import { Hono } from 'hono';
import type { Vars } from '../app';

/** cannisino routes: implemented by the feature build (see docs/cannibisters-app/03-architecture.md). */
export const cannisino = new Hono<{ Variables: Vars }>();
cannisino.get('/', (c) => c.json({ message: 'cannisino: not implemented yet' }, 501));
