import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import { startErrorReports } from "./errorReports.js";
import "./styles.css";

// Before the first render, so an error while the page starts up is recorded too (HIR-259).
startErrorReports();

createRoot(document.getElementById("root")).render(<React.StrictMode><App /></React.StrictMode>);
