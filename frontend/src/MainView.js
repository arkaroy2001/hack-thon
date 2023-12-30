import React, { useState,useEffect} from 'react'
import httpClient from './httpClient';
import BubbleChart from "./BubbleChart";

const MainView = () => {

    const [message,setMessage] = useState('');
    const [loading, setLoading] = useState(false);

    useEffect(()=>{
        setLoading(true);

        (async()=>{
            await httpClient.get("/api")
            .then(res=>{
                setMessage(res.data);
                setLoading(false);
            })
            .catch(err=>{
                console.log(err);
            })
        })()
    },[]);

    if(loading){
        return <p>...Loading</p>
    }

    return (
        <div>
            <BubbleChart/>
        </div>
    );
};

export default MainView;
