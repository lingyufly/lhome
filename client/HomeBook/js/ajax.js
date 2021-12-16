function get(url, data, thenf, catchf) {
    cAjax.get(url, data,
              function(res){
                  thenf(JSON.parse(res))
              }
          );
}


function post(url, data, thenf) {
    cAjax.post(url, data,
        function(res){
            thenf(JSON.parse(res))
        }
    );
}

function put(url, data, thenf) {
    cAjax.put(url, data,
        function(res){
            thenf(JSON.parse(res))
        }
    );
}


function uploadFile(url, file, data, thenf) {
    cAjax.uploadFile(url, file, data,
        function(res){
            thenf(JSON.parse(res))
        }
    );
}
