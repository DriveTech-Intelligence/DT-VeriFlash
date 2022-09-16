import React, { useContext } from "react";
import { Route, Routes } from "react-router-dom";
import FlashStats from "../Components/FlashStats/flashStats";
import Login from "../Components/Login/login";
import AuthContext from "../Context/AuthProvider";

function AppRouter() {
  const { auth } = useContext(AuthContext);
  return (
    <Routes>
      {auth?.username && auth?.accessToken && (
        <Route path="flash-stats" element={<FlashStats />} />
      )}
      <Route path="*" element={<Login />} />
    </Routes>
  );
}

export default AppRouter;
