import request from '@/utils/request'

export function upload(data, query) {
  return request({
    url: '/upload',
    method: 'post',
    params: query,
    data
  })
}

export function remove(query) {
  return request({
    url: '/remove',
    method: 'delete',
    params: query
  })
}
