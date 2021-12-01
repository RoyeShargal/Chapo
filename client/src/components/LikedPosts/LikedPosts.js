import React,{useState, useEffect} from "react"
import httpClient from "../../httpClient";
import Post from "../Post/Post"
export default function LikedPosts(){
    const [posts,setPosts] = useState([])
    useEffect( () => {
        (async () => {
            try{
                const listOfPosts = await httpClient.get("//127.0.0.1:5000/specificposts"
                )
                setPosts(listOfPosts.data)
            }
            catch(e){
                console.log("no posts")
            }
        })();
    },[])

    return(
        <div >
           <div className={"padd"}>
                    {posts.map((post) => {
                        return(
                            <div key="{item} ">
                                <Post aSinglePost={post}/>
                            </div>
                        )
                    })}        </div>





        </div>


    )
}
