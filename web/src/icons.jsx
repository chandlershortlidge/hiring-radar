const I = ({ d, size = 14, sw = 2, ...rest }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" {...rest}>
    {d.map((p, i) => <path key={i} d={p} />)}
  </svg>
);
export const Plus = (p) => <I d={["M12 5v14M5 12h14"]} {...p} />;
export const X = (p) => <I d={["M6 6l12 12M18 6L6 18"]} sw={2.4} {...p} />;
export const Down = (p) => <I d={["M6 9l6 6 6-6"]} size={16} {...p} />;
export const Up = (p) => <I d={["M6 15l6-6 6 6"]} size={16} {...p} />;
export const Search = (p) => <I d={["M18 18a7 7 0 1 0-14 0a7 7 0 0 0 14 0M20 20l-4-4"]} {...p} />;
export const Ext = (p) => <I d={["M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"]} size={13} {...p} />;
export const Repost = (p) => <I d={["M4 12a8 8 0 0 1 14-5.3L20 9M20 4v5h-5M20 12a8 8 0 0 1-14 5.3L4 15M4 20v-5h5"]} size={12} {...p} />;
export const Check = (p) => <I d={["M5 12l5 5 9-10"]} size={16} sw={2.2} {...p} />;
export const Info = (p) => <I d={["M12 21a9 9 0 1 0 0-18a9 9 0 0 0 0 18M12 8v5M12 16v.5"]} size={16} {...p} />;
export const Warn = (p) => <I d={["M12 3l10 18H2z", "M12 10v4M12 17v.5"]} size={16} {...p} />;
export const Compare = (p) => <I d={["M3 5h7v14H3zM14 5h7v14h-7z"]} sw={1.8} {...p} />;
export const Person = (p) => <I d={["M12 12a4 4 0 1 0 0-8a4 4 0 0 0 0 8M4 21a8 8 0 0 1 16 0"]} sw={1.8} {...p} />;
export const Radar = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#161616" strokeWidth="1.6" aria-hidden="true">
    <circle cx="12" cy="12" r="9" /><circle cx="12" cy="12" r="5" /><path d="M12 12 L19 6" /><circle cx="12" cy="12" r="1.2" fill="#161616" />
  </svg>
);
