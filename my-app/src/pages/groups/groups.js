import React from "react";
import "./groups.css"
import groups from "./groups.json"

function Groups() {
    return (
        <div className="container">
            <div className="groups-container">
                {groups.map(group => {
                    return (
                        <div className="group-box" key={group.id}>
                            <center><div className="group-title">Title: {group.title}</div></center>
                            <center><div className="group-content">Type: {group.Type}</div></center>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}

export default Groups;
