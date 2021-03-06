//Inits for materialize elements:

$(document).ready(function() {
    $('.sidenav').sidenav();
    $('select').formSelect();

// Change Icon for categories when displaying recipes from Mongo;

$(".category_icon").each(function(index) {
    if ($(this).html() == "Breakfast") {
            $(this).replaceWith('<img class="recipecat" src="./static/images/breakfast.png"></img>');
        } else if ($(this).html() == "Lunch") {
            $(this).replaceWith('<img class="recipecat" src="./static/images/lunch.png"></img>');
        } else if ($(this).html() == "Dinner") {
            $(this).replaceWith('<img class="recipecat" src="./static/images/dinner.png"></img>');
        } else if ($(this).html() == "Brunch") {
            $(this).replaceWith('<img class="recipecat" src="./static/images/brunch.png"></img>');
        } else if ($(this).html() == "Dessert") {
            $(this).replaceWith('<img class="recipecat" src="./static/images/dessert.png"></img>');
        } else {
            $(this).replaceWith('<img class="recipecat" src="./static/images/baking.png"></img>');
        } 
});

// Masonary Init and re-sizing 

        $('.grid').masonry({
            itemSelector: '.grid-sizer',
            gutter: 10,
            columnWidth: '.grid-sizer',
            percentPosition: true
        });
});

