import React from 'react';
import './App.css';
import UserHeader from './Components/UserHeader';
import Event from './Components/Event';
import Footer from './Components/Footer';

function App() {
    return (
        <div className="app">
            <UserHeader />
            <Event title="Event 1" date="dd/mm" time="hh:mm" />
            <Event title="Event 2" date="dd/mm" time="hh:mm" />
            <Footer />
        </div>
    );
}

export default App;