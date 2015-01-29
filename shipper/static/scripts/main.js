$( '.btn-dismiss' ).click(function () {
	$(this).closest('[role="dialog"]').remove();
});

$( '.btn-clear' ).click(function () {
	$('#ship-form')[0].reset();
});

$('table tr').click(function(){
    $(this).find('input[type=radio]').prop('checked', true);
});