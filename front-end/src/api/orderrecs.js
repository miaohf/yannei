import request from '@/utils/request'

export function updateOrderrec(id, data) {
  return request({
    url: `/orderrecs/${id}`,
    method: 'put',
    data,
  })
}
