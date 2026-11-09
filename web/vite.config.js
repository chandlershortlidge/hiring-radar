import { defineConfig } from "vite";
import { configDefaults } from "vitest/config";
import react from "@vitejs/plugin-react";

// Dev: `npm run dev` proxies /api to the FastAPI server on :8000.
// Build: `npm run build` writes web/dist, which `python -m app serve` mounts at /.
// Test: vitest runs the unit tests only; e2e/ holds
// the PR before/after screenshots (HIR-231), run by `npm run shots`.
export default defineConfig({
  plugins: [react()],
  server: { proxy: { "/api": "http://127.0.0.1:8000" } },
  build: { outDir: "dist", emptyOutDir: true },
  test: { exclude: [...configDefaults.exclude, "e2e/**", "shots-out/**"] },
});
