function eliminar_tarea(key){
	$.ajax({
		url: '/ajax/delete/'+key,
		dataType: 'json',
		cache: false,
		success: function(data){
			if(data.eliminado == true){
				alert("Eliminado!")
				window.location.reload()
			}else
				alert(":O, no lo eliminó")
		}
	})
}