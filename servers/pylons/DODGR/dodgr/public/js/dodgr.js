
$(document).ready(function() {
    // setup ul.tabs to work as tabs for each div directly under div.panes
    // $("ul.tabs").tabs("div.panes > div");    

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
});

