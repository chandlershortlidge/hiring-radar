// What a "doesn't belong here" flag says about the screen it was clicked on (HIR-226).
//
// The flag has no reason picker: the view itself says what the job was supposed to be. So
// the whole state goes along, not a hand-picked list of filters. `filters` is the very
// object the job list hands to api.jobs — the one the request's address is built from — so
// a filter added to the dashboard later is recorded with no change here. The server stores
// what it is sent, untouched (app/flags.py), and flagView.test.js fails if anything the
// job-list request carries is missing from the flag.
//
// Pure: nothing is fetched or stored here, and nothing about the person is included.

// A flag from the job list. `sort` is "fit" when the list is ranked in the browser;
// `saved` is true in the Saved view, where no filter narrows the rows.
export function flagView({ filters, sort, saved = false, market = null, url = window.location.pathname }) {
  return { page: "list", url, sort, saved, market, filters: { ...filters } };
}

// A flag from a job's own page: no filter decided that the job is shown there.
export const jobPageView = (url = window.location.pathname) => ({ page: "job", url });
