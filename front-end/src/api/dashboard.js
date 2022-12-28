import request from '@/utils/request'

export function fetchDashboardData() {
  return request({
    url: '/dashboard',
    method: 'get'
  })
}

export function fetchBasicinfo(id) {
  return request({
    url: '/basicinfo',
    method: 'post'
  })
}
