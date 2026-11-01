import { describe, expect, it } from "vitest";
import { MIN_PHRASE, flatten, matchCvSkills, occursAsWord, phrasesFor } from "./cvSkills.js";

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

describe("hyphens and slashes are word separators (HIR-100)", () => {
  // Its own slice: these entries are multi-word or punctuated, which is what the rule is
  // about, and adding them to TAX would change every exact-array expectation above.
  const COMPOUNDS = [
    ...TAX,
    { id: "prompt-engineering", display: "prompt engineering", aliases: [] },
    { id: "docker", display: "Docker", aliases: ["container technologies"] },
    { id: "machine-learning", display: "machine learning", aliases: [] },
    { id: "kubernetes", display: "Kubernetes", aliases: ["deployment patterns"] },
    { id: "agent-frameworks", display: "agent frameworks", aliases: ["orchestration frameworks"] },
    { id: "sqlite", display: "SQLite", aliases: [] },
    { id: "postgres", display: "Postgres", aliases: ["PostgreSQL"] },
    { id: "tool-calling", display: "tool calling", aliases: ["function calling"] },
    { id: "dotnet", display: ".NET", aliases: [] },
    { id: "nodejs", display: "Node.js", aliases: [] },
    { id: "tool-call-hyphen", display: "tool-call", aliases: [] },
    { id: "cicd", display: "CI/CD", aliases: [] },
  ];
  const ids = (text) => matchCvSkills(text, COMPOUNDS).ids;

  it("matches a hyphenated compound against the spaced phrase", () => {
    expect(ids("Erfahrung mit Prompt-Engineering")).toContain("prompt-engineering");
    expect(ids("Container-Technologien wie Docker")).toContain("docker");
    expect(ids("Deployment-Patterns in der Cloud")).toContain("kubernetes");
    expect(ids("Kenntnisse in Machine-Learning-Konzepten")).toContain("machine-learning");
    expect(ids("Orchestrierungs-Frameworks")).not.toContain("agent-frameworks");
    expect(ids("Orchestration-Frameworks kennen")).toContain("agent-frameworks");
  });

  it("matches both sides of a slashed pair", () => {
    const got = ids("Datenbanken: SQLite/Postgres");
    expect(got).toContain("sqlite");
    expect(got).toContain("postgres");
  });

  it("matches a phrase split by a slash in the text", () => {
    const got = ids("tool/function calling with the API");
    expect(got).toContain("tool-calling");
  });

  it("matches a hyphenated phrase against spaced text, and the reverse", () => {
    // phrase "tool-call" against spaced text
    expect(ids("we do a tool call per step")).toContain("tool-call-hyphen");
    // phrase "CI/CD" against spaced and hyphenated text
    expect(ids("owned CI CD pipelines")).toContain("cicd");
    expect(ids("owned CI-CD pipelines")).toContain("cicd");
    expect(ids("owned CI/CD pipelines")).toContain("cicd");
  });

  it("reports the taxonomy's own spelling, not the flattened one", () => {
    const { found } = matchCvSkills("Erfahrung mit Prompt-Engineering", COMPOUNDS);
    expect(found.find((f) => f.id === "prompt-engineering").phrase).toBe("prompt engineering");
  });

  it("leaves dots alone, so .NET and Node.js still match as one token", () => {
    expect(ids("backend in .NET and Node.js")).toEqual(
      expect.arrayContaining(["dotnet", "nodejs"]),
    );
    // and a dot is still not a separator: "NET" alone must not claim ".NET"
    expect(ids("NET revenue grew")).not.toContain("dotnet");
    expect(ids("node js scripts")).not.toContain("nodejs");
  });

  it("keeps every rule the fix had to leave alone", () => {
    expect(ids("Wrote C++11 for three years")).toContain("cpp");
    expect(ids("Front end in React with hooks")).toContain("react");
    expect(ids("Front end in React with hooks")).not.toContain("react-agent-pattern");
    expect(ids("Agents using the ReAct loop")).toContain("react-agent-pattern");
    expect(ids("Go-live owner; go to market")).not.toContain("go");
    expect(ids("Wrote plain js")).not.toContain("javascript");
    expect(ids("R&D lead. Modelling in R.")).not.toContain("r-lang");
  });

  it("flattens separators but not other punctuation", () => {
    expect(flatten("Machine-Learning/Konzepten")).toBe("Machine Learning Konzepten");
    expect(flatten("Node.js")).toBe("Node.js");
    expect(flatten("C++")).toBe("C++");
    expect(flatten("  a - b  ")).toBe("a b");
    expect(flatten(undefined)).toBe("");
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
