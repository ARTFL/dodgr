var currentHeadword;

$(document).ready(function() {

    // Toggle the visibility of the dictionary for each section after the
    // header is clicked.
	$('.block_header').click(function() {
        triangle = $(this).children('.triangle');

        if ($(this).next().is(":visible")) {
            triangle.html('▶');
        } else {
            triangle.html('▽');
        }
		$(this).next().toggle();
		return false;
	});

	// Change the headword into a form on mouseover
    $('#main_headword_container').mouseover(function() {
        currentHeadword = $('#main_headword_input').val();
        $('#main_headword_input').css('border', '1px solid #000');
        $('#main_headword_input').focus();
    });
    $('#main_headword_container').mouseout(function() {
        $('#main_headword_input').css('border', '1px solid #fff');
        $('#main_headword_input').blur();
        $('#main_headword_input').val(currentHeadword);
    });

});

