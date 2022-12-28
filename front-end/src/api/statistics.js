import request from '@/utils/request'

export function fetchStatistics() {
  return request({
    url: '/statistics',
    method: 'get',
  })
}

export function fetchProject() {
  return request({
    url: '/projectinfo',
    method: 'get',
  })
}


