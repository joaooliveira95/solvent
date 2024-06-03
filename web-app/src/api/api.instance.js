import axios from 'axios'

export const API_INSTANCE = axios.create({
    baseURL: import.meta.env.REACT_APP_API,
})

// export const API_INSTANCE = setupCache(
//     axios.create({
//         baseURL: process.env.REACT_APP_API,
//     }),
//     {
//         methods: ['get', 'post'],
//         generateKey: (request) => `${request.method}: ${request.url}`,
//         debug: console.log,
//     }
// )

// TRANSLATION API
// export const translationApiInstance = setupCache(
//     axios.create({
//         baseURL: process.env.REACT_APP_TRANSLATION_API,
//     })
// )

export const addAuthorization = (token) => {
    API_INSTANCE.interceptors.request.use((config) => {
        if (config && config.headers) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    })
}

API_INSTANCE.defaults.headers.common = {
    'Cache-control': 'no-cache',
    Pragma: 'no-cache',
    Expires: '0',
}
