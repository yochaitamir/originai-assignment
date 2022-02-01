import React,{useEffect,useState} from 'react'
import  "./style.css"
import Image from "./image.tsx"

const ImagesDisplay=()=>{
    const [imagesArray,setImagesArray]=useState([])
    useEffect(() => {
      fetch("http://localhost:5001/populate")
        .then(response => response.json())
        .then(data =>{
        console.log("useeffect",data)
         setImagesArray(data)});

      },[]);
    const handleCSV = async ()=>{
        console.log("csv")
        await fetch(`http://localhost:5001/exportcsv`)
            .then(response => response.json())
            .then(data => alert(data['msg']));
        }

    const gallery = imagesArray.map((item,i)=>{
           return <Image key={i} item={item} i={i}/>
          })
    return (
            <div className="wrraper" >
                <img className="csvIcon" src={"/CSV.png"} onClick={()=>handleCSV()}/>
                {gallery}
            </div>
            )
}

export default ImagesDisplay