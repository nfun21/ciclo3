$('#ciudad').on('input', function() {//check that input is being updated
  if ((this.value).length >= 2) {///CHECK THAT INPUT CONTAINS 4 characters OR MORE.
    ///send ajax query
    var resultados=[];
    var ciudad;

    $(function() 
    {
        ciudad = document.querySelector('#ciudad').value;
        tipoVuelo = document.querySelector('#tipoVuelo').value;
            $.ajax(
                {
                  url: requestUrl+'?ciudad='+ciudad+'&tipoVuelo='+tipoVuelo,//python route to process the request
                }).done(function (data){//data is the results the request obtained
                   
                      //separate the name into a list so it can be searched from auto complete
                        for ( i=0; i<data.length; i++ ) {
                          resultados.push(data[i]['vuelo']);
                          
                        }
                    
                    $('#ciudad').autocomplete(
                        {
                          source: resultados,
                          minLength: 2,
                         
                        }
                    );
                }
                );
            
    }
    );
  }
  
});

// document.getElementById("tipoVuelo").onchange = function(e) {
//   if (this[this.selectedIndex].value == "Entrante") {
//     document.getElementsByName('ciudadorigen')[0].placeholder='Dinos de qué ciudad quieres regresar⬅️';
//     document.getElementById("ciudad").focus()
//   }else{
//     document.getElementsByName('ciudadorigen')[0].placeholder='Dinos a qué ciudad quieres ir➡️';
//     document.getElementById("ciudad").focus()
//   }
  
// };

document.getElementById("tipoVuelo").onchange = function(e) {
  
    document.getElementById("ciudad").focus();

}