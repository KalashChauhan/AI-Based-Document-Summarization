import React from 'react';
import {BrowserRouter,Routes,Route} from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Summarize from './pages/Summarize';
import History from './pages/History';
import './style.css';
export default function App(){
    return <BrowserRouter>
    <Navbar/>
    <Routes>
        <Route path="/" element={<Home/>}/>
        <Route path="/summarize" element={<Summarize/>}/>
        <Route path="/history" element={<History/>}/>
    </Routes></BrowserRouter>}
