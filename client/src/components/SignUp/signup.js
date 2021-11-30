import { useState } from 'react';
import APIService from "../APIService";
import "./signup.css"

const Signup = (props) => {
    const [fullName, setFullname] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const insertUser = () => {
        APIService.InsertUser({fullName, email, password})
            .then((response) => props.insertedUser(response))
            .catch(error => console.log('er ror', error))
    }

    const handleSubmit = (event) => {

            event.preventDefault()
            console.log()
            insertUser()
            window.alert('Successful!')
            window.open("/home", "Successfully added!");
            setFullname('')
            setEmail('')
            setPassword('')
            console.log("User Added, Success")


    }

    return (
        <div className='signup'>
            <span className="signupTitle">GLAD YOU'RE WITH US!</span>

            <form onSubmit={handleSubmit} className="signupForm">
                <input type='text'
                       required
                       placeholder='Full Name'
                       onChange={(e) => {setFullname(e.target.value); }}
                       value={fullName}
                       className='signupInput'/>

                <input type='text' required minLength={5} maxLength={30}
                       placeholder='Email'
                       pattern = "^+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"
                       onChange={(e)=>setEmail(e.target.value)}
                       value={email}
                       className='signupInput'/>

                <input type='password'
                       required
                       minLength={8}
                       maxLength={20}
                       placeholder='Password'
                       onChange={(e)=>setPassword(e.target.value)}
                       value={password}
                       className='signupInput'/>

                <button
                        className='signupButton'
                        > SignUp
                </button>
            </form>

        </div>
    )

}


export default Signup;
