/** @jest-environment jsdom */
const fs = require('fs'), path = require('path');
const code = fs.readFileSync(path.join(__dirname, '..', 'src', 'js', 'analytics.js'), 'utf8');

function load({ dnt = false, tcf } = {}) {
  jest.resetModules();
  document.head.innerHTML = '';
  delete window.dataLayer; delete window.gtag; delete window.__tcfapi;
  Object.defineProperty(navigator, 'doNotTrack', { value: dnt ? '1' : '0', configurable: true });
  Object.defineProperty(window, 'location', { value: new URL('https://minimalist-games.com/'), configurable: true, writable: true });
  if (tcf) window.__tcfapi = tcf;
  (0, eval)(code);
}
const calls = () => (window.dataLayer || []).map(a => Array.from(a));
const consentUpdates = () => calls().filter(c => c[0] === 'consent' && c[1] === 'update');
const fakeTcf = (data) => (cmd, v, cb) => { if (cmd === 'addEventListener') cb(data, true); };

beforeEach(() => jest.useFakeTimers());
afterEach(() => jest.useRealTimers());

test('consent default is DENIED and is queued before config', () => {
  load();
  const c = calls();
  const iDef = c.findIndex(x => x[0] === 'consent' && x[1] === 'default');
  const iCfg = c.findIndex(x => x[0] === 'config');
  expect(iDef).toBeGreaterThanOrEqual(0);
  expect(iDef).toBeLessThan(iCfg);
  expect(c[iDef][2]).toMatchObject({ analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
});

test('Do Not Track: nothing is loaded', () => {
  load({ dnt: true });
  expect(window.dataLayer).toBeUndefined();
  expect(document.querySelector('script[src*="googletagmanager"]')).toBeNull();
});

test('GDPR applies and visitor has not chosen: stays denied', () => {
  load({ tcf: fakeTcf({ gdprApplies: true, eventStatus: 'cmpuishown', purpose: { consents: {} } }) });
  expect(consentUpdates()).toHaveLength(0);
});

test('GDPR applies and no message was ever shown (current production state): stays denied', () => {
  load({ tcf: fakeTcf({ gdprApplies: true, purpose: { consents: {} } }) });
  expect(consentUpdates()).toHaveLength(0);
});

test('visitor consents to purposes 1 and 7: analytics granted', () => {
  load({ tcf: fakeTcf({ gdprApplies: true, eventStatus: 'useractioncomplete', purpose: { consents: { 1: true, 7: true } } }) });
  expect(consentUpdates()).toHaveLength(1);
  expect(consentUpdates()[0][2]).toEqual({ analytics_storage: 'granted' });
});

test('visitor refuses: stays denied', () => {
  load({ tcf: fakeTcf({ gdprApplies: true, eventStatus: 'useractioncomplete', purpose: { consents: { 1: false, 7: false } } }) });
  expect(consentUpdates()).toHaveLength(0);
});

test('consent for purpose 1 only is not enough', () => {
  load({ tcf: fakeTcf({ gdprApplies: true, eventStatus: 'tcloaded', purpose: { consents: { 1: true } } }) });
  expect(consentUpdates()).toHaveLength(0);
});

test('GDPR does not apply (outside EEA/UK/CH): granted', () => {
  load({ tcf: fakeTcf({ gdprApplies: false, eventStatus: 'tcloaded', purpose: { consents: {} } }) });
  expect(consentUpdates()).toHaveLength(1);
});

test('granted only once even if the CMP fires several events', () => {
  const d = { gdprApplies: true, eventStatus: 'useractioncomplete', purpose: { consents: { 1: true, 7: true } } };
  load({ tcf: (cmd, v, cb) => { if (cmd === 'addEventListener') { cb(d, true); cb(d, true); } } });
  expect(consentUpdates()).toHaveLength(1);
});

test('CMP injected late (after 2 s) is still picked up', () => {
  load();
  jest.advanceTimersByTime(2000);
  window.__tcfapi = fakeTcf({ gdprApplies: true, eventStatus: 'useractioncomplete', purpose: { consents: { 1: true, 7: true } } });
  jest.advanceTimersByTime(500);
  expect(consentUpdates()).toHaveLength(1);
});

test('no CMP ever (ad blocker): stays denied and does not poll forever', () => {
  load();
  jest.advanceTimersByTime(60000);
  expect(consentUpdates()).toHaveLength(0);
  expect(jest.getTimerCount()).toBe(0);
});

test('mgTrack still queues events', () => {
  load();
  window.mgTrack('game_win', { game: 'sudoku' });
  expect(calls().some(c => c[0] === 'event' && c[1] === 'game_win')).toBe(true);
});
