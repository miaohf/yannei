import request from '@/utils/request'

export function fetchUsers(query) {
  return request({
    url: '/users',
    method: 'get',
    params: query
  })
}

export function fetchUser(id) {
  return request({
    url: `/users/${id}`,
    method: 'get'
  })
}

export function createUser(data) {
  return request({
    url: '/users',
    method: 'post',
    data
  })
}

export function updateUser(id, data) {
  return request({
    url: `/users/${id}`,
    method: 'put',
    data
  })
}

export function deleteUser(id) {
  return request({
    url: `/users/${id}`,
    method: 'delete'
  })
}
