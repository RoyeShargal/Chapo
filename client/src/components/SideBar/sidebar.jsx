import "./sidebar.css"
import React from "react";

export default function SideBar(){
    return(
        <div className="sidebar">
            <div className="sidebarItem">
                <span className="sidebarTitle">WHY US</span>
                <p className={"sidebarContent"}> we believe in education. But sometimes, it's getting done wrong. We are here to fix it.
                Or if to say it properly, we are here to help you out.</p>
                <p className={"sidebarContent"}> </p>

            </div>



            <div className="sidebarItem">
                <span className="sidebarTitle">SUBJECTS</span>
                <ul className="sidebarList">
                    <li className="sidebarListItem">MATH</li>
                    <li className="sidebarListItem">PHYSICS</li>
                    <li className="sidebarListItem">ENGLISH</li>
                    <li className="sidebarListItem">HISTORY</li>
                    <li className="sidebarListItem">COMPUTING</li>
                    <li className="sidebarListItem">ART</li>
                </ul>
            </div>


            <div className="sidebarItem">
                <span className="sidebarTitle">CONNECT</span>
                <div className="sidebarSocial">
                    <i className="sidebarIcon fab fa-facebook"></i>
                    <i className="sidebarIcon fab fa-instagram"></i>
                    <i className="sidebarIcon fab fa-pinterest"></i>
                </div>
            </div>
        </div>
    )
}