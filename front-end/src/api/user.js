import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/tokens',
    method: 'post',
    headers: {
      Authorization: 'Basic ' + btoa(data.username + ':' + data.password)
    }
  })
}

// export function getInfo(token) {
export function getInfo() {
  return request({
    url: '/user/info',
    method: 'get',
    // params: { token }
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}

