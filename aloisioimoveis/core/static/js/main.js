new Vue({
    el: '#app'
});

$(document).ready(function() {
    let carousel = $("#myCarousel");
    carousel.swiperight(function() {
        $(this).carousel('prev');
    });
    carousel.swipeleft(function() {
        $(this).carousel('next');
    });
});
