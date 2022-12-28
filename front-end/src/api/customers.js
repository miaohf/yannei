import request from '@/utils/request'

export function fetchCustomers(query) {
  return request({
    url: '/customers',
    method: 'get',
    params: query,
  })
}

export function fetchCustomer(id) {
  return request({
    url: `/customers/${id}`,
    method: 'get',
  })
}

export function createCustomer(data) {
  return request({
    url: '/customers',
    method: 'post',
    data,
  })
}

export function updateCustomer(id, data) {
  return request({
    url: `/customers/${id}`,
    method: 'put',
    data,
  })
}

export function addContactorOrAddressByCustomer(id, data) {
  return request({
    url: `/customers/${id}`,
    method: 'post',
    data,
  })
}

export function deleteCustomer(id) {
  return request({
    url: `/customers/${id}`,
    method: 'delete',
  })
}

export function fetchCustomersList() {
  return request({
    url: '/customerslist',
    method: 'get',
  })
}
