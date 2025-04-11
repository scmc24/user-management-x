import axios from "axios";

export const getAllUsers = async () => {
    const res = await axios.get(`/users/`).catch((err)=> console.log(err));
  
    if(res.status !== 200){
     return console.log("Unable to fetch users");
    }
 
    const data = res.data.data;
    return data;    
}
export const getUser = async () => {
    let userId = parseInt(localStorage.getItem('userId'));

    const res = await axios.get(`/users/${userId}/`).catch((err)=> console.log(err));
  
    if(res.status !== 200){
     return console.log("Unable to fetch user");
    }
 
    const data = res.data.data;
    return data;
}




export const login = async (data) => {
    const res = await axios.post(`/login/`,{
        email: data.email,
        password: data.password
    }).catch((err)=> console.log(err));

    if(res.status !== 200 && res.status !== 201 ){
        return console.log(`Unable to authenticate ${res.status}`);
    }

    const resData = await res.data.data;
    return resData;
}

export const logout = async () => {
    const res = await axios.post(`/users/logout`).catch((err)=> console.log(err));

    if(res.status !== 200 && res.status !== 201 ){
        return console.log(`Unable to logout ${res.status}`);
    }

    const resData = await res.data.data;
    return resData;
}

export const register = async (data) => {
    const res = await axios.post(`/signup/`,{
        username: data.username,
        email: data.email,
        password: data.password

    }).catch((err)=> console.log(err));

    if(res.status !== 200 && res.status !== 201 ){
        return console.log(`Unable to authenticate ${res.status}`);
    }

    const resData = await res.data.data;
    return resData;
}



