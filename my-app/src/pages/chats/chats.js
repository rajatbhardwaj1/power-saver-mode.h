import React from "react";
import "./chats.css"
import groups from "./chats.json"

function Chats() {
    return (
        <div className="container">
            <div className="groups-container">
                {groups.map(group => {
                    return (
                        <div className="group-box" key={group.id}>
                            <center><div className="group-title">Title: {group.title}</div></center>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}

export default Chats;
