import "./topbar.css"
import React, {useEffect, useState} from 'react'
import {Link} from 'react-router-dom'
import httpClient from "../../httpClient";


export default function TopBar(){
    const [user,setUser] = useState( '')

    const logoutUser = async()=>{
        await httpClient.post("//127.0.0.1:5000/logout");
        window.location.href="/home";
    };
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
        <div className ="top">
            <div className="topLeft">
                <i className="topIcon fab fa-facebook"></i>
                <i className="topIcon fab fa-instagram"></i>
                <i className="topIcon fab fa-pinterest"></i>

            </div>


            <div className="topCenter">
                <ul className="topList">

                    <li className="topListItem">
                        <Link to ="/home" className="a">HOME</Link>
                    </li>

                    {user.email==null? (<li className="topListItem" >

                            <Link to ="/login" className="a">LOGIN</Link>
                        </li>)
                    :(<p></p>)}
                    {user.email != null ? (<li className="topListItem">
                        <Link to ="/post" className="a">POST</Link>

                    </li>):(<li className="topListItem" >

                        <Link to ="/register" className="a">SIGNUP</Link>
                    </li>)}
                    {user.email != null ? (<li className="topListItem">
                        <Link to ="/myposts" className="a">LIKED POSTS</Link>

                    </li>):(<li className="topListItem" >

                        <Link to ="/register" className="a">SIGNUP</Link>
                    </li>)}


                    <li className="topListItem" >
                        <Link to ="/about" className="a">
                              ABOUT
                        </Link>
                    </li>


                </ul>

            </div>
            <div className="topRight">
                {user.email != null?
                    (
                        <Link to ="/profile" className="a"><i className="topSearchIcon far fa-user-circle">
                        </i> </Link>
                    ):
                    (<i></i>)}


                {user.email!=null?(                <i className="topSearchIcon fas fa-sign-out-alt" onClick={logoutUser}></i>
                ):(<p></p>)}
            </div>

        </div>
    )
}
