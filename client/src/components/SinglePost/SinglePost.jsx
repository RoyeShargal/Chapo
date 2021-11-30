
import React, {useState} from "react";
export default function SinglePost({aSinglePost})
{

    return(
        <div className="post">

            <div className="postItem">
                <span className="postTitle">{aSinglePost.title}</span>
                <span className="postDate">Created by {aSinglePost.authorName}</span>
                <p className={"postContent"}>{aSinglePost.content}</p>
                <p className={"postDate"}>{aSinglePost.date}</p>
            </div>
        </div>
    )
}