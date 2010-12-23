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
		$(this).next().toggle(400);
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

	$('.word_reference_trigger').click(function() {
	    if ($('#word_reference_container').html() == '') {
            $('#word_reference_container').html('<iframe width="320" height="600" src="http://mini.wordreference.com/mini/index.aspx?dict=fren&w=' + $('#main_headword_input').val() + '&u=1" name="WRmini"></iframe>');
            $('.word_reference_trigger').html('<span class="web_link">Supprimer WordReference</span>');
        } else {
            $('#word_reference_container').html('');
            $('.word_reference_trigger').html('<span class="web_link">Activer WordReference</span>');
        }
    });

    // Clear out the default text in the search bar when it's focused
    $('input.search_bar_word').focus(function() {
        if ($(this).val() == "Recherche d'un mot") {
            $(this).val('');
       }
    });

});

