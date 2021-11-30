import React,{useState, useEffect} from "react"
import httpClient from "../httpClient";
import Post from "./Post/Post";
import data from "bootstrap/js/src/dom/data";
import './home.css'
import * as http from "http";
export default function Home(){
    const [posts,setPosts] = useState([])
    const [tags,setTags] = useState('')
    const [postsTags,setPostsTags] = useState ([])
    useEffect( () => {
        (async () => {
            try{
                const listOfPosts = await httpClient.get("//127.0.0.1:5000/posts"

                )
                setPosts(listOfPosts.data)
            }
            catch(e){
                console.log("no posts")
            }
        })();
    },[])
    const getPosts =async  () =>
    {
        const postsByTags = await httpClient.post("//127.0.0.1:5000/postsbytags",{
            tags
        })
        setPostsTags(postsByTags.data)
    }

    // const mid = Math.ceil(posts.length/2);

    // const firstHalf = posts.slice().splice(0,mid);
    // const secondHalf = posts.slice().splice(-mid);
    // const [searchQuery, setSearchQuery] = useState(query || '');

    return(
<div >
        <form className={"formSearch"}>
            <input type='text'
                   placeholder='Search by Tags'
                   onChange={(e)=>{setTags(e.target.value); getPosts().then(r => null)}}
                   value={tags}
                   className='searchInput'/>

            <br/>
            {/*<button type="button" className="searcHereButton" onClick={() => getPosts()}>Search</button>*/}

        </form>
    {tags.length == 0 ? (<div className={"padd"}>
            {posts.map((post) => {
                return(
                    <div key="{item} ">
                        <Post  aSinglePost={post}/>
                    </div>
                )
            })}        </div>)
        :(<div className={"padd"}>
            {postsTags.map((post) => {
                return(
                    <div key="{item} ">
                        <Post  aSinglePost={post}/>
                    </div>
                )
            })}        </div>)}




</div>


    )
}
