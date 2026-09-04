import type { ConciergeQuickAction, ConciergeMessage } from '../types';

export const CONCIERGE_ACTIONS: ConciergeQuickAction[] = [
  { key: 'recommend', title: 'Recommend me something', hint: 'Tell us the evening you have in mind.' },
  { key: 'reserve', title: 'Reserve a seat', hint: 'Lounge, Serenity Room or the terrace.' },
  { key: 'preorder', title: 'Pre-order for collection', hint: 'Ready at the counter when you arrive.' },
  { key: 'consult', title: 'Book a consultation', hint: 'Dr Andre Sorger, in-house practitioner.' },
  { key: 'delivery', title: 'Delivery help', hint: 'Slots, cut-off times and where your order is.' },
  { key: 'human', title: 'Talk to the team', hint: 'Continue on WhatsApp with a person.' },
];

export const CONCIERGE_WELCOME: ConciergeMessage = {
  id: 'w0',
  from: 'concierge',
  text: 'Welcome to the Concierge. Tell us what you are after and we will take it from there.',
  at: '2026-09-03T18:00:00+02:00',
  quickReplies: ['Something for a slow evening', 'A table for four on Sunday', 'What is new this week'],
};
