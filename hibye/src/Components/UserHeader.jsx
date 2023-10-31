import React from 'react';
import './UserHeader.css';

function UserHeader() {
    return (
        <div className="userHeader">
            <button className="userButton">USERS</button>
            <button className="editButton">Edit</button>
        </div>
    );
}

export default UserHeader;