// What the browser remembers between visits: the market you were last looking at, and the
// three you looked at most recently (HIR-188). A returning visitor lands on their last
// city instead of the home grid, and the picker opens with a "Recent" group at the top.
//
// Stored in localStorage, never sent anywhere — same care as the profile: a browser with
// storage switched off, or a quota error, must not take the page down, so every read and
// write is wrapped and failure means "nothing remembered".
const LAST = "hr.last";
const RECENT = "hr.recentPlaces";
const RECENT_MAX = 3;

const read = (key, fallback) => {
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch { return fallback; }
};
const write = (key, value) => { try { window.localStorage.setItem(key, JSON.stringify(value)); } catch { /* storage off or full */ } };

// The last market as {place, family} slugs, or null when nothing is remembered.
export function readLast() {
  const v = read(LAST, null);
  return v && typeof v.place === "string" ? { place: v.place, family: typeof v.family === "string" ? v.family : null } : null;
}
export const writeLast = (place, family) => write(LAST, { place, family: family || null });

// Recent place slugs, newest first, at most three distinct.
export const readRecent = () => (Array.isArray(read(RECENT, [])) ? read(RECENT, []).filter((s) => typeof s === "string") : []);
export function pushRecent(place) {
  const next = [place, ...readRecent().filter((s) => s !== place)].slice(0, RECENT_MAX);
  write(RECENT, next);
  return next;
}
