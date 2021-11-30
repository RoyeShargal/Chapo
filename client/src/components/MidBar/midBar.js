import logo from "../../photos/Chapo-logos.jpeg"
import React,{useState, useEffect} from "react"
import "./midBar.css"
import httpClient from "../../httpClient";
export default function MidBar(){

    const [user,setUser] = useState('')

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
        <div className={"mid"}>
            {user.email != null ? (
                <span className={"item"}>
                    Welcome back {user.fullName}
                </span>
            ):(
                <span className={"item"}>
                    Welcome Champ.
                </span>
            )}

        </div>
    )

}
