import { describe, expect, it } from "vitest";
import { CvReadError, MAX_BYTES, MIN_CHARS, readCvFile } from "./cvText.js";

// The PDF and .docx readers need real binaries and a browser worker, so they are exercised
// by hand (see the PR). What is tested here is every guard that decides whether text is
// usable at all — the paths a person actually hits when something is wrong.

const txt = (body, name = "cv.txt") => new File([body], name, { type: "text/plain" });
const long = (word) => (word + " ").repeat(Math.ceil(MIN_CHARS / (word.length + 1)) + 5);

describe("readCvFile", () => {
  it("reads a plain-text CV", async () => {
    const body = long("Python and PyTorch and Kubernetes");
    await expect(readCvFile(txt(body))).resolves.toContain("PyTorch");
  });

  it("reads .md and .markdown too", async () => {
    const body = long("- Python");
    await expect(readCvFile(txt(body, "cv.md"))).resolves.toContain("Python");
    await expect(readCvFile(txt(body, "cv.markdown"))).resolves.toContain("Python");
  });

  it("refuses a file with almost no text, naming the scanned-CV case", async () => {
    await expect(readCvFile(txt("Jane Doe"))).rejects.toThrow(CvReadError);
    await expect(readCvFile(txt("Jane Doe"))).rejects.toThrow(/scanned or image-only/i);
  });

  it("counts only non-whitespace toward the minimum", async () => {
    await expect(readCvFile(txt(" ".repeat(MIN_CHARS * 2)))).rejects.toThrow(CvReadError);
  });

  it("refuses an unsupported extension by name", async () => {
    await expect(readCvFile(txt(long("Python"), "cv.pages"))).rejects.toThrow(/\.pages/);
  });

  it("refuses a file with no extension", async () => {
    await expect(readCvFile(txt(long("Python"), "cv"))).rejects.toThrow(CvReadError);
  });

  it("refuses a file over the size cap before reading it", async () => {
    const big = new File([new Uint8Array(MAX_BYTES + 1)], "cv.pdf");
    await expect(readCvFile(big)).rejects.toThrow(/over 10 MB/);
  });

  it("refuses nothing at all", async () => {
    await expect(readCvFile(null)).rejects.toThrow(CvReadError);
  });
});
