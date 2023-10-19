import { defaultUserState } from "../context/AuthContext";

export const putIntoLocalStorage = (data) => {
  localStorage.setItem("slashuser", JSON.stringify(data));
};

export const getFromLocalStorage = (setUserData) => {
  if (localStorage.getItem("slashuser") !== null) {
    const slashuser = JSON.parse(localStorage.getItem("slashuser"));
    setUserData({
      isLoggedIn: true,
      username: slashuser.username,
      email: slashuser.email,
      user_id: slashuser.user_id,
    });
  }
};

export const logout = (setUserData) => {
  localStorage.removeItem("slashuser");
  setUserData(defaultUserState);
};