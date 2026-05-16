import axios from 'axios'
const login=axios.create({
    baseURL:'http://localhost:8000/funciones/login'
})
const register=axios.create({
    baseURL:'http://localhost:8000/funciones/register'
})

export const Login=(e)=>login.post('/', e)
export const Registe=(e)=>register.post('/', e)