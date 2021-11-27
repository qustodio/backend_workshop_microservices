import { Route, Routes } from "react-router-dom";
import Authors from "./views/Authors";
import Books from "./views/Books";
import Book from "./views/Book";
import Home from "./views/Home";
import Login from "./views/Login";

function Router() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/books" element={<Books />} />
      <Route path="/book/:id" element={<Book />} />
      <Route path="/authors" element={<Authors />} />
      <Route path="/login" element={<Login /> } />
    </Routes>
  )
}

export default Router;
