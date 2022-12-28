import request from '@/utils/request'

export function fetchProvincesList() {
  return request({
    url: '/selections/provinces',
    method: 'get',
  })
}

export function fetchCitesListbyProvinceID(provinceId) {
  return request({
    url: `/selections/cities/${provinceId}`,
    method: 'get',
  })
}

export function fetchCustomersList() {
  return request({
    url: '/selections/customers',
    method: 'get',
  })
}

export function fetchContactorsListbyCustomerId(customerId) {
  return request({
    url: `/selections/contactors/${customerId}`,
    method: 'get',
  })
}

export function fetchAddressesListbyCustomerId(customerId) {
  return request({
    url: `/selections/addresses/${customerId}`,
    method: 'get',
  })
}

export function fetchVisittypesList() {
  return request({
    url: '/selections/visittypes',
    method: 'get',
  })
}
