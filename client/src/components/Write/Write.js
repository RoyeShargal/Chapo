import "./write.css"
import {useEffect, useState} from 'react';
import APIService from "../APIService";
import httpClient from "../../httpClient";
import React from "react";
const Write = (props) => {

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

    const [user,setUser] = useState( '')
    const [title, setTitle] = useState('')
     const [content, setContent] = useState('')
    const [userid,setUserid] = useState('')
    const [tags,setTags] = useState('')
    const insertPost = () => {
        APIService.InsertPost({title,content,userid,tags })
            .then((response) => props.insertedPost(response))
            .catch(error => console.log('error', error))
    }

    const handleSubmit= (event) =>{

        event.preventDefault()
        insertPost()
        window.alert('Posted!')
        window.open("/home", "Posted!");
        // setImg('')
        setTitle('')
        setContent('')
        setTags('')


    }
    return (
        <div className="write">

            <form className="writeForm" onSubmit={handleSubmit} >
                <p className="writeFormGroup writeInputTitle">CREATE:</p>

                <div className="writeFormGroup">
                    <textarea type="text" required minLength={4} maxLength={50}
                           placeholder="Title"
                           id="textInput"
                           value={title}
                           className="writeInput titleBOX"
                           onChange={(e)=>setTitle(e.target.value)}

                           autoFocus={true}/>

                </div>

                <div className="writeFormGroup ">
                    <textarea className="writeInput content " type="text" required minLength={5} maxLength={300}
                           placeholder="What's this about ?"
                           onChange={(e)=>{setContent(e.target.value);setUserid(user.id)}}
                           value={content}
                    />

                </div>
                <div className={"writeFormGroup"}>
                    <input
                        type="text" required maxLength={12}
                        onChange={(e)=>{setTags(e.target.value)}}
                        placeholder="Tags"
                        value={tags}
                        className={"writeInput titleBOX"}
                    />
                </div>



                <div className="writeFormGroup">

                    <button className="writeSubmit btn-success"
                            >POST</button>
                </div>
            </form>
        </div>
    )
}
export default Write;