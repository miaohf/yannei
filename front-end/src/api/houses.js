import request from '@/utils/request'

export function fetchHouses(query) {
  return request({
    url: '/houses',
    method: 'get',
    params: query,
  })
}

export function fetchHouse(id) {
  return request({
    url: `/houses/${id}`,
    method: 'get',
  })
}

export function createHouse(data) {
  return request({
    url: '/houses',
    method: 'post',
    data,
  })
}

export function updateHouse(id, data) {
  return request({
    url: `/houses/${id}`,
    method: 'put',
    data,
  })
}

export function deleteHouse(id) {
  return request({
    url: `/houses/${id}`,
    method: 'delete',
  })
}

export function fetchHousesList() {
  return request({
    url: '/houseslist',
    method: 'get',
  })
}

export function checkHouse(id) {
  return request({
    url: `/houses/${id}`,
    method: 'put',
  })
}

export function fetchHousesCount() {
  return request({
    url: '/houses/count',
    method: 'get',
  })
}

export function fetchHouseStatistics() {
  return request({
    url: '/houses/statistics',
    method: 'get',
  })
}
