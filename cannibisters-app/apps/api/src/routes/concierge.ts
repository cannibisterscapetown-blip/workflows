import { Hono } from 'hono';
import type { Vars } from '../app';

/** concierge routes: implemented by the feature build (see docs/cannibisters-app/03-architecture.md). */
export const concierge = new Hono<{ Variables: Vars }>();
concierge.get('/', (c) => c.json({ message: 'concierge: not implemented yet' }, 501));
