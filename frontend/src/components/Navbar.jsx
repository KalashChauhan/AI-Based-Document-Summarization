import React from 'react';
import {Link} from 'react-router-dom'; 
export default function Navbar(){
    return <nav>
        <Link className="brand" to="/">AI-Based Document Summarizer</Link>
        <span/>
        <Link to="/summarize">Summarize</Link>
        <Link to="/history">History</Link>
    </nav>
}
