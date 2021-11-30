import "./profile.css"
import React, {useEffect, useState} from "react";
import httpClient from "../../httpClient";
import {Link} from "react-router-dom";
export default function Profile(){
    const [user,setUser] = useState( '')
    useEffect(()=>{
        (async () => {
            try {
                const resp = await httpClient.get("//127.0.0.1:5000/@me");
                setUser(resp.data);
            }
            catch (e){
                console.log("Not Authenticated.")
            }
        })();
    },[])

    return(

        <div className="card">
                <h1 className="title">Hello, {user.fullName}</h1>
                <p className="subtitle">Email: {user.email}</p>
                <p className="subtitle">Joined at {user.date}</p>

            <Link to ="/changepassword" className="a">
            <button className={"button"}>Change Password ?</button>
            </Link>
            </div>

    )
}