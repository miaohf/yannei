import request from '@/utils/request'

export function fetchOrders(query) {
  return request({
    url: '/orders',
    method: 'get',
    params: query,
  })
}

export function fetchOrder(id) {
  return request({
    url: `/orders/${id}`,
    method: 'get',
  })
}

export function updateOrder(id, data) {
  return request({
    url: `/orders/${id}`,
    method: 'put',
    data,
  })
}
