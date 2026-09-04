import { Hono } from 'hono';
import type { Vars } from '../app';

/** loyalty routes: implemented by the feature build (see docs/cannibisters-app/03-architecture.md). */
export const loyalty = new Hono<{ Variables: Vars }>();
loyalty.get('/', (c) => c.json({ message: 'loyalty: not implemented yet' }, 501));
