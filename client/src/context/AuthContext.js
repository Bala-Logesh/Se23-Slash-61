import { createContext, useEffect, useState } from "react";
import { getFromLocalStorage } from "../utils/helper";

export const AuthContext = createContext();

export const defaultUserState = {
  isLoggedIn: false,
  username: "",
  email: "",
  user_id: 0
};

export const AuthContextProvider = ({ children }) => {
  const [userData, setUserData] = useState(defaultUserState);

  useEffect(() => {
    getFromLocalStorage(setUserData);
  }, []);

  return <AuthContext.Provider value={{ userData, setUserData }}>{children}</AuthContext.Provider>;
};
