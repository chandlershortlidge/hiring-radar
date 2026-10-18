// The "what does this mean for me" profile. Lives only in this browser (localStorage);
// the server never sees it. Shape: { role, seniority, german (bool: professional German),
// degree ('' | bachelor | master | phd), skills: [skill_id] }.
import { useCallback, useEffect, useState } from "react";

const KEY = "hiring-radar.profile.v1";
export const EMPTY = { role: "AI engineer", seniority: "", german: false, degree: "", skills: [] };

function load() {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return null;
    const p = JSON.parse(raw);
    return { ...EMPTY, ...p, skills: Array.isArray(p.skills) ? p.skills : [] };
  } catch { return null; }
}

export function useProfile() {
  const [profile, setProfile] = useState(() => load());
  const save = useCallback((p) => {
    setProfile(p);
    try { if (p) localStorage.setItem(KEY, JSON.stringify(p)); else localStorage.removeItem(KEY); } catch {}
  }, []);
  useEffect(() => {
    const onStorage = (e) => { if (e.key === KEY) setProfile(load()); };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);
  return [profile, save];
}

// Deterministic coverage: how many of a job's required skills the profile has.
export function coverage(profile, skills) {
  const req = skills.filter((s) => s.requirement === "required").map((s) => s.skill_id);
  if (!profile || !req.length) return null;
  const have = new Set(profile.skills);
  const covered = req.filter((id) => have.has(id));
  return { covered: covered.length, total: req.length, missing: req.filter((id) => !have.has(id)) };
}
