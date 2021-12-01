import "./post.css"
import React, {useEffect, useState} from "react";
import httpClient from "../../httpClient";
import {Link} from "react-router-dom";
import * as http from "http";
export default function Post({aSinglePost})
{
    const [user,setUser] = useState( '')

    const postID = aSinglePost.id

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

    let postId = aSinglePost.id
    const arrayOfTags = aSinglePost.tags.split(' ')

    const deletePost = async  () => {
        if (window.confirm("Delete?")) {
            await httpClient.post("//127.0.0.1:5000/deletepost",{
                postId
            });


        }
    }
    let userid;
    if(user != null){
     userid = user.id}
    else{
         userid=0;
    }
    const likePost = async () => {
        await httpClient.post("//127.0.0.1:5000/likeapost",{
            postId,
            userid

        })
        window.alert('Added to liked posts!')
    }

    return(
        <div className="post">
            <div>
                <span className="postTitle" >{aSinglePost.title}</span>
                <span className="postAuthor">Created by {aSinglePost.authorName}</span>
                <p className={"postContent"}>{aSinglePost.content} </p>
                {arrayOfTags.map((tag) => {
                    return(<p className={"tags"}>{tag}</p>)
                })}
                <p className={"postDate"}>{aSinglePost.date} </p>
                {user.email != null ? (
                    <i className="far fa-heart heart " onClick={likePost}></i>
                ):(<p></p>)}
                {/*{aSinglePost.authorId === user.id ? (<i className="deletebtn far fa-trash-alt " onClick={deletePost}/>)*/}
                {/*    :*/}
                {/*    (<p></p>)}*/}




            </div>
        </div>
    )
}