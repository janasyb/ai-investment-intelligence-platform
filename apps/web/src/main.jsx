import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App.jsx";
import OperationsApp from "./components/operations/OperationsApp.jsx";
import "./styles/global.css";

const root = ReactDOM.createRoot(document.getElementById("root"));

const application =
  window.location.pathname === "/operations" ? (
    <OperationsApp />
  ) : (
    <App />
  );

root.render(
  <React.StrictMode>
    {application}
  </React.StrictMode>
);