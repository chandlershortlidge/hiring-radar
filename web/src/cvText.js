// A chosen CV file → its plain text, in the browser. The thin I/O half of the CV pre-fill;
// the matching logic is cvSkills.js and is what the tests cover.
//
// Does: read a PDF (pdf.js), a .docx (mammoth) or a plain-text file into a string, and
// refuse a file that yields too little text to match against.
//
// Does NOT: upload anything, keep anything, or look at what the text says. The File never
// leaves the page and the string is dropped when the drawer closes
// (DECISIONS 2026-11-01, HIR-14).
//
// Invariants:
//   - A scanned PDF (images, no text layer) yields almost nothing and is rejected with a
//     message that says to paste the text instead, rather than silently matching zero skills.
//   - Errors are CvReadError with a sentence meant for the person, not a stack trace.

export const MAX_BYTES = 10 * 1024 * 1024;
export const MIN_CHARS = 200;

export class CvReadError extends Error {}

function extOf(name) {
  const m = /\.([a-z0-9]+)$/i.exec(name || "");
  return m ? m[1].toLowerCase() : "";
}

async function pdfText(file) {
  const [pdfjs, worker] = await Promise.all([
    import("pdfjs-dist"),
    import("pdfjs-dist/build/pdf.worker.min.mjs?url"),
  ]);
  pdfjs.GlobalWorkerOptions.workerSrc = worker.default;
  const data = new Uint8Array(await file.arrayBuffer());
  const doc = await pdfjs.getDocument({ data }).promise;
  const pages = [];
  for (let n = 1; n <= doc.numPages; n++) {
    const page = await doc.getPage(n);
    const content = await page.getTextContent();
    pages.push(content.items.map((i) => i.str || "").join(" "));
  }
  return pages.join("\n");
}

async function docxText(file) {
  const mammoth = await import("mammoth");
  const { value } = await mammoth.extractRawText({ arrayBuffer: await file.arrayBuffer() });
  return value || "";
}

/** Read `file` into text, or throw CvReadError with something worth showing the person. */
export async function readCvFile(file) {
  if (!file) throw new CvReadError("No file chosen.");
  if (file.size > MAX_BYTES) throw new CvReadError("That file is over 10 MB. Try a smaller one.");

  const ext = extOf(file.name);
  let text;
  try {
    if (ext === "pdf") text = await pdfText(file);
    else if (ext === "docx") text = await docxText(file);
    else if (ext === "txt" || ext === "md" || ext === "markdown") text = await file.text();
    else throw new CvReadError(`Can't read a .${ext || "?"} file. Use a PDF, a .docx or plain text.`);
  } catch (e) {
    if (e instanceof CvReadError) throw e;
    throw new CvReadError("That file could not be read. Try exporting it again, or paste the text.");
  }

  if ((text || "").trim().length < MIN_CHARS) {
    throw new CvReadError(
      "Almost no text came out — a scanned or image-only CV can't be read here. Paste the text instead."
    );
  }
  return text;
}
