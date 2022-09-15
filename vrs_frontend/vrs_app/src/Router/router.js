import React from "react";
import { Route, Routes } from "react-router-dom";
import FlashStats from "../Components/FlashStats/flashStats";
import SignIn from "../Components/Login/login";
import RequireAuth from "../Components/RequireAuth";

function AppRouter() {
  return (
    <Routes>
      <Route index element={<SignIn />} />
      <Route element={<RequireAuth />}>
        <Route path="flash-stats" element={<FlashStats />} />
      </Route>
    </Routes>
  );
}

export default AppRouter;
