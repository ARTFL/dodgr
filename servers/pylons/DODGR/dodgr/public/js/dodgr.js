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
		$(this).next().slideToggle(400);
		return false;
	});
    
    $("#toggle_nyms").click(function() {
        var str = $("#toggle_nyms").text()
        
        if (str == 'Voir le reste des synonymes') {
            var newstr = 'Cacher';
        } else {
            var newstr = 'Voir le reste des synonymes';
        }
        $("#toggle_nyms").text(newstr);
        $("#remainder").slideToggle(200);
        $("#ellipsis").toggle(200);
        return false;
    });
    
    $("#toggle_anto").click(function() {
        var str = $("#toggle_anto").text()
        
        if (str == 'Voir le reste des antonymes') {
            var newstr = 'Cacher';
        } else {
            var newstr = 'Voir le reste des antonymes';
        }
        $("#toggle_anto").text(newstr);
        $("#remainder_anto").slideToggle(200);
        $("#ellipsis_anto").toggle(200);
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

function expand(truncated, rest) {
                $("#" + truncated).toggle();
                $("#" + rest).toggle();
                return false;
}

