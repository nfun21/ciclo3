$('#piloto').on('input', function() {//check that input is being updated
    if ((this.value).length > 3) {///CHECK THAT INPUT CONTAINS 4 characters OR MORE.
      ///send ajax query
      var nombre=[];
      var idUser=[];
      var consulta;
  
      $(function() 
      {
          consulta = document.querySelector('#piloto').value;
              $.ajax(
                  {
                    url: requestUrl+consulta,//python route to process the request
                  }).done(function (data){//data is the results the request obtained
                      console.log(data);
                        //separate the name into a list so it can be searched from auto complete
                          for ( i=0; i<data.length; i++ ) {
                              nombre.push(data[i]['nombre'] + ' | ' + data[i]['id']);
                              idUser.push(data[i]['id']);
                          }
                      console.log(nombre),
                      $('#piloto').autocomplete(
                          {
                            source: nombre,
                            minLength: 4,
                            select: function( event, ui ) {
                              console.log(ui.item['value']);
                              var val = ui.item['value'];
                              var index = $.inArray( val, nombre );
                              $('input#idPiloto').val(idUser[index]);
                            }
                          }
                      );
                  }
                  );
              
      }
      );
    }
    
  });

  ///copiloto
  $('#copiloto').on('input', function() {//check that input is being updated
    if ((this.value).length > 3) {///CHECK THAT INPUT CONTAINS 4 characters OR MORE.
      ///send ajax query
      var nombre=[];
      var idUser=[];
      var consulta;
  
      $(function() 
      {
          consulta = document.querySelector('#copiloto').value;
              $.ajax(
                  {
                    url: requestUrl+consulta,//python route to process the request
                  }).done(function (data){//data is the results the request obtained
                      console.log(data);
                        //separate the name into a list so it can be searched from auto complete
                          for ( i=0; i<data.length; i++ ) {
                              nombre.push(data[i]['nombre'] + ' | ' + data[i]['id']);
                              idUser.push(data[i]['id']);
                          }
                      console.log(nombre),
                      $('#copiloto').autocomplete(
                          {
                            source: nombre,
                            minLength: 4,
                            select: function( event, ui ) {
                              console.log(ui.item['value']);
                              var val = ui.item['value'];
                              var index = $.inArray( val, nombre );
                              $('input#idcoPiloto').val(idUser[index]);
                            }
                          }
                      );
                  }
                  );
              
      }
      );
    }
    
  });

   