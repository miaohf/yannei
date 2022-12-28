import axios from 'axios'
import store from '@/store'
import { getToken } from '@/utils/auth'

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // .env
  timeout: 6000, // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent
    // config.headers.Authorization = basicAuth

    if (store.getters.token) {
      // let each request carry token
      config.headers.Authorization = 'Bearer ' + getToken()
    }
    return config
  },
  error => {
    // do something with request error
    // console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  response => {
    if (response.status in [200, 201]) {
    } else {
      return response
    }
  },
  error => {
    if (
      error.response.status === 401 ||
      error.response.status === 403 ||
      error.response.status === 405 ||
      error.response.status === 50008
    ) {
      // to re-login
      this.$confirm('您的登录凭证已经过期，请重新登录', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(() => {
        store.dispatch('user/resetToken').then(() => {
          location.reload()
        })
      })
    } else {
      return Promise.reject(error)
    }
  }
)

export default service
