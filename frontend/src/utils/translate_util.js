export async function translateByYoudao(enText){
    youdaoEngine='http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i='
    return fetch(youdaoEngine+enText,{mode:'no-cors'}).then(resp=>{return resp.json().translateResult[0][0].tgt})
}
