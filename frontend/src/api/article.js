import request from '../utils/request'


export function getList(params) {
    return request({
        url: 'http://192.168.19.128:8000/article/?format=json',
        method: 'get',
        params
    })

}

// export function getContent(title){
//     return request({
//         url:'http://192.168.19.128:8000/'
//     })
// }