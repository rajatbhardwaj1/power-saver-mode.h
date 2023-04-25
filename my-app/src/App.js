import './App.css';
import Login from "./pages/login/login"
import CreateAccount from './pages/create_account/create_account';
import Groups from './pages/groups/groups';
import Chats from './pages/chats/chats';
import ChatBox from './pages/chat/chat';

import {  Route, Routes } from "react-router-dom";

function App() {
  return (
    <Routes>
        <Route path="/login" element={<Login />}/>
        <Route path="/create-account" element={<CreateAccount />}/>
        <Route path="/groups" element={<Groups />}/>
        <Route path="/chats" element={<Chats />}/>
        <Route path="/chat" element={<ChatBox />}/>
    </Routes>
  );
}

export default App;
