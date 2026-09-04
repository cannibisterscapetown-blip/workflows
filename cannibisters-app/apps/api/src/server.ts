import { serve } from '@hono/node-server';
import { createApp } from './app';
import { env, isMock } from './env';

serve({ fetch: createApp().fetch, port: env.port }, (info) => {
  console.log(`Cannibisters BFF listening on http://localhost:${info.port} (${isMock ? 'mock' : 'live'} mode)`);
});
