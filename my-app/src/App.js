import './App.css';
import Login from "./pages/login/login"
import CreateAccount from './pages/create_account/create_account';


import {  Route, Routes } from "react-router-dom";

function App() {
  return (
    <Routes>
        <Route path="/login" element={<Login />}/>
        <Route path="/create-account" element={<CreateAccount />}/>
    </Routes>
  );
}

export default App;
