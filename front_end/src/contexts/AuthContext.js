// AuthContext.js
import React, {
  createContext,
  useContext,
  useRef,
  useState,
  useEffect,
} from "react";
import GptAgent from "../utilities/gpt_agent.js"; // 引入 GptUser 类

export const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const existingToken = localStorage.getItem("userToken");
  const existingUsername = localStorage.getItem("username");
  const [isAuthenticated, setIsAuthenticated] = useState(!!existingToken);

  const gpt_agent = useRef(
    new GptAgent(existingToken, existingUsername, setIsAuthenticated)
  ).current;

  useEffect(() => {
    if (existingToken) {
      gpt_agent.validateToken();
    }
  }, [existingToken, gpt_agent]);

  return (
    <AuthContext.Provider value={{ gpt_agent, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};
