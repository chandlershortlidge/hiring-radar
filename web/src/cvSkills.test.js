import { describe, expect, it } from "vitest";
import { MIN_PHRASE, matchCvSkills, occursAsWord, phrasesFor } from "./cvSkills.js";

// A slice of the real taxonomy (v5 ids, displays and aliases), including every entry whose
// name is short or case-sensitive enough to be a hazard.
const TAX = [
  { id: "python", display: "Python", aliases: [] },
  { id: "pytorch", display: "PyTorch", aliases: ["torch"] },
  { id: "rag", display: "RAG", aliases: ["retrieval-augmented generation"] },
  { id: "react", display: "React", aliases: [] },
  { id: "react-agent-pattern", display: "ReAct", aliases: [] },
  { id: "go", display: "Go", aliases: ["golang"] },
  { id: "r-lang", display: "R", aliases: [] },
  { id: "csharp", display: "C#", aliases: [] },
  { id: "cpp", display: "C++", aliases: [] },
  { id: "javascript", display: "JavaScript", aliases: ["js"] },
  { id: "aws", display: "AWS", aliases: [] },
  { id: "triton-inference-server", display: "Triton Inference Server", aliases: ["NVIDIA Triton"] },
];

const ids = (text) => matchCvSkills(text, TAX).ids;

describe("matchCvSkills", () => {
  it("matches a display name and an alias, and reports which phrase hit", () => {
    const { ids, found } = matchCvSkills("Built pipelines in Python with torch.", TAX);
    expect(ids).toEqual(["python", "pytorch"]);
    expect(found.find((f) => f.id === "pytorch").phrase).toBe("torch");
    expect(found.find((f) => f.id === "python").phrase).toBe("Python");
  });

  it("is case-insensitive for ordinary skills", () => {
    expect(ids("PYTHON, python, Python")).toContain("python");
    expect(ids("aws lambda")).toContain("aws");
  });

  it("returns ids sorted and each skill at most once", () => {
    const got = ids("Python Python python and AWS and RAG");
    expect(got).toEqual(["aws", "python", "rag"]);
  });

  it("returns nothing for an empty or non-string CV", () => {
    expect(ids("")).toEqual([]);
    expect(matchCvSkills(undefined, TAX).ids).toEqual([]);
    expect(matchCvSkills("Python", undefined).ids).toEqual([]);
  });

  describe("word boundaries", () => {
    it("does not match inside a longer word", () => {
      expect(ids("ragged edges and a goner")).toEqual([]);
      expect(ids("I was going to the shop")).not.toContain("go");
      expect(ids("Pythonista")).toEqual([]);
    });

    it("matches next to punctuation and across lines", () => {
      expect(ids("Skills: Python, AWS.\n- RAG\n")).toEqual(["aws", "python", "rag"]);
      expect(ids("(Python)")).toContain("python");
    });

    it("matches a phrase ending in punctuation even when a digit follows", () => {
      // "C++" ends in '+', so no right-hand boundary is required.
      expect(ids("Wrote C++11 for three years")).toContain("cpp");
      expect(ids("C++ and Python")).toContain("cpp");
    });

    it("matches a multi-word phrase", () => {
      expect(ids("served models on NVIDIA Triton in prod")).toContain("triton-inference-server");
      expect(ids("built retrieval-augmented generation over our docs")).toContain("rag");
    });

    it("matches a multi-word phrase a PDF wrapped across lines", () => {
      // How pdf.js hands back a wrapped line: the break lands mid-phrase.
      expect(ids("served models on NVIDIA\nTriton in prod")).toContain("triton-inference-server");
      expect(ids("NVIDIA   Triton")).toContain("triton-inference-server");
      expect(ids("retrieval-augmented\n   generation")).toContain("rag");
    });
  });

  describe("ReAct vs React (case carries meaning)", () => {
    it("tells the framework from the agent pattern", () => {
      expect(ids("Front end in React with hooks")).toEqual(["react"]);
      expect(ids("Agents using the ReAct loop")).toEqual(["react-agent-pattern"]);
    });

    it("does not let a lowercase mention claim either", () => {
      expect(ids("we react to incidents quickly")).toEqual([]);
    });

    it("can match both when the CV names both", () => {
      expect(ids("React front end; ReAct agents")).toEqual(["react", "react-agent-pattern"]);
    });
  });

  describe("phrases too short to be trusted", () => {
    it("never matches a bare R or C#", () => {
      expect(ids("R&D lead. Modelling in R. Also C#.")).toEqual([]);
    });

    it("never matches a bare Go, but does match golang", () => {
      expect(ids("Go-live owner; go to market")).not.toContain("go");
      expect(ids("Services in golang")).toContain("go");
    });

    it("still matches a 3-character name", () => {
      expect(ids("Owned the RAG stack")).toContain("rag");
      expect(ids("Owned the AWS bill")).toContain("aws");
    });

    it("drops the 2-character 'js' alias, but JavaScript itself still matches", () => {
      expect(ids("Wrote plain js")).toEqual([]);
      expect(ids("Wrote plain JavaScript")).toContain("javascript");
    });

    it("drops short phrases from a skill's phrase list", () => {
      expect(phrasesFor({ display: "C#", aliases: [] })).toEqual([]);
      expect(phrasesFor({ display: "Go", aliases: ["golang"] })).toEqual(["golang"]);
      expect(MIN_PHRASE).toBe(3);
    });
  });

  it("reads a realistic CV without inventing skills", () => {
    const cv = `
      Jane Doe — Machine Learning Engineer, Berlin

      EXPERIENCE
      Acme GmbH (2023–2026). Shipped a retrieval-augmented generation assistant used by
      40,000 customers. Served fine-tuned models on NVIDIA Triton behind AWS. Training
      code in Python and PyTorch. Went to market with a React dashboard.

      EDUCATION
      MSc Computer Science. Thesis on reinforcement learning.
    `;
    expect(ids(cv)).toEqual([
      "aws", "python", "pytorch", "rag", "react", "triton-inference-server",
    ]);
  });
});

describe("occursAsWord", () => {
  it("requires a boundary on sides where the phrase edge is alphanumeric", () => {
    expect(occursAsWord("a go b", "go")).toBe(true);
    expect(occursAsWord("ago b", "go")).toBe(false);
    expect(occursAsWord("a going", "go")).toBe(false);
    expect(occursAsWord("c++11", "c++")).toBe(true);
    expect(occursAsWord("", "go")).toBe(false);
    expect(occursAsWord("go", "")).toBe(false);
  });

  it("keeps scanning past a rejected occurrence", () => {
    // first "go" is inside "ago", the second stands alone
    expect(occursAsWord("ago, then go", "go")).toBe(true);
  });

  it("treats accented letters as word characters", () => {
    expect(occursAsWord("begrüßen", "grü")).toBe(false);
  });
});
