import request from '@/utils/request'

export function fetchVisits(query) {
  return request({
    url: '/visits',
    method: 'get',
    params: query,
  })
}

export function fetchVisit(id) {
  return request({
    url: `/visits/${id}`,
    method: 'get',
  })
}

export function createVisit(data) {
  return request({
    url: '/visits',
    method: 'post',
    data,
  })
}

export function updateVisit(id, data) {
  return request({
    url: `/visits/${id}`,
    method: 'put',
    data,
  })
}

export function deleteVisit(id) {
  return request({
    url: `/visits/${id}`,
    method: 'delete',
  })
}

export function confirmToAudit(data) {
  return request({
    url: '/visits',
    method: 'post',
    data,
  })
}
