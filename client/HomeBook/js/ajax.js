function get(url, data, thenf, catchf) {
    cAjax.get(url, data,
              function(res){
                  thenf(JSON.parse(res))
              },function(res){
                  catchf(JSON.parse(res));
              }
          );
}


function post(url, data, thenf, catchf) {
    cAjax.post(url, data,
        function(res){
            thenf(JSON.parse(res))
        },function(res){
            catchf(JSON.parse(res));
        }
    );
}
