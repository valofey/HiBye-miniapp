import React from 'react';
import './Event.css';

function Event({ title, date, time }) {
    return (
        <div className="event">
            <h3>{title}</h3>
            <p>{date} {time}</p>
            <button>+</button>
        </div>
    );
}

export default Event;