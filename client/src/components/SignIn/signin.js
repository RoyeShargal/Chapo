import { useState } from 'react';
import "../SignUp/signup.css"
import httpClient from "../../httpClient"

const Signin = (props) => {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const logInUser = async () => {
        console.log(email, password);
         try {
            const resp = await httpClient.post("//127.0.0.1:5000/login", {
                email,
                password
            });
            console.log(resp.data)
             window.alert('Welcome Back!')

             window.location.href = "/home";

         } catch(error) {
                alert("INVALID!");

        }
    };

    return (
        <div className='signup'>
            <span className="signupTitle">LOGIN</span>

            <form className="signinForm" >
                <input type='text'
                       placeholder='Email'
                       onChange={(e)=>setEmail(e.target.value)}
                       value={email}
                       className='signupInput'/>

                       <br/>
                <input type='password'
                       placeholder='Password'
                       onChange={(e)=>setPassword(e.target.value)}
                       value={password}
                       className='signupInput'/>

            </form>
            <button type="button" className="signupButton" onClick={() => logInUser()}>LOGIN</button>


        </div>
    )

}


export default Signin;
