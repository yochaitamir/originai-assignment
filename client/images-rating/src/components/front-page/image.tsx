    import React,{useState} from 'react'
    import  "./style.css"


    const Image=(props)=>{
        const {i,item} =props

        const [likes,setLikes]=useState(item.likes)
        const [dislikes,setDisLikes]=useState(item.dislikes)

        const handleLikeButton=(item)=>{
            setLikes(likes+1)
            fetch(`http://localhost:5001/like/${item.image_id}`)
                .then(response => response.json())
                .then(data => console.log(data));
                }

        const handleDislikeButton=(item)=>{
            setDisLikes(dislikes+1)
            fetch(`http://localhost:5001/dislike/${item.image_id}`)
                .then(response => response.json())
                .then(data => console.log(data));
                }
         return <div className="conatinerWrraper">
                    <img key={i} className="pic"  src={item.image_url} loading="lazy"/>
                    <img key={i} className="dislike" onClick={()=>handleDislikeButton(item)} src={"/dislike.png"}/>
                    <span className="dislikeRatings">{dislikes}</span>
                    <span className="likeRatings" >{likes}</span>
                    <img key={i} className="like" onClick={()=>handleLikeButton(item)} src={"/like.png"}/>
                 </div>
                }

    export default Image