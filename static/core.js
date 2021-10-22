$('#piloto').on('input', function() {//check that input is being updated
    if ((this.value).length >= 2) {///CHECK THAT INPUT CONTAINS 4 characters OR MORE.
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
                            nombre.push(data[i]['nombres'] +' '+ data[i]['apellidos'] + ' | ' + data[i]['idUser']);
                            idUser.push(data[i]['idUser']);
                          }
                      console.log(nombre),
                      $('#piloto').autocomplete(
                          {
                            source: nombre,
                            minLength: 2,
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
    if ((this.value).length >= 2) {///CHECK THAT INPUT CONTAINS 4 characters OR MORE.
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
                  }).done(function (copilotos){//data is the results the request obtained
                      console.log(copilotos);
                        //separate the name into a list so it can be searched from auto complete
                          for ( i=0; i<copilotos.length; i++ ) {
                              nombre.push(copilotos[i]['nombres'] + ' ' +copilotos[i]['apellidos'] + ' | ' + copilotos[i]['idUser']);
                              idUser.push(copilotos[i]['idUser']);
                          }
                      console.log(nombre),
                      $('#copiloto').autocomplete(
                          {
                            source: nombre,
                            minLength: 2,
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


