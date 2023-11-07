import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Auth } from "./auth/ui";

export const Router = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/sign-up" element={<Auth />} />
      </Routes>
    </BrowserRouter>
  );
};
