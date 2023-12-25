import React from "react";
import { createRoot } from "react-dom/client"; // 引入createRoot
import { AuthProvider } from "./contexts/AuthContext";
import App from "./App";

const container = document.getElementById("root");
const root = createRoot(container); // 使用createRoot创建根

root.render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>
);
