import {useEffect, useState} from 'react';
import APIService from "../APIService";
import "../SignUp/signup.css"
import httpClient from "../../httpClient";

const ChangePassword = (props) => {
    const [user,setUser] = useState( '')

    const [password, setPassword] = useState('')
    const [confirmpassword, setConfirmPassword] = useState('')
    const [userid,setUserid] = useState('')

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
    const changePassword = () => {
        APIService.InsertPassword({ userid,password})
            .then((response) => props.insertedUser(response))
            .catch(error => console.log('error', error))
    }

    const handleSubmit = (event) => {

        event.preventDefault()
        console.log()
        if(confirmpassword == password) {
            changePassword()
            console.log("Password Changed, Success")

        }
        else {
            window.alert("Passwords don't match!");
        }
            setPassword('')
        setConfirmPassword('')


    }

    return (
        <div className='signup'>
            <span className="signupTitle"> PASSWORD CHANGE</span>

            <form onSubmit={handleSubmit} className="signupForm">


                <input type='password'
                       required
                       minLength={8}
                       maxLength={20}
                       placeholder='Password'
                       onChange={(e)=>{setPassword(e.target.value);setUserid(user.id)}}
                       value={password}
                       className='signupInput'/>
                <input type='password'
                       required
                       minLength={8}
                       maxLength={20}
                       placeholder='Confirm Password'
                       onChange={(e)=>setConfirmPassword(e.target.value)}
                       value={confirmpassword}
                       className='signupInput'/>

                <button
                    className='signupButton'
                > Confirm
                </button>
            </form>

        </div>
    )

}


export default ChangePassword;
