import request from '../utils/request'

export function getList(params) {
    return request({
        url: 'http://139.196.142.70:8000/profile/?format=json',
        method: 'get',
        params
    })
}
