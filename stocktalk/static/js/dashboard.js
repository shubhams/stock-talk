$('.js-data-example-ajax').select2({
    minimumInputLength: 3,
    placeholder: 'Type a symbol',
    allowClear: true,
    ajax: {
        url: '/search',
        delay: 250,
        data: function (params) {
            return {
                sym: params.term
            };
        },
        cache: true
    }
});

function submitSymbol(csrfToken) {
    var val = $('.js-data-example-ajax').val();
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("save-response").innerHTML = this.responseText;
        }
    };
    xhttp.open("POST", "/save", true);
    xhttp.setRequestHeader("X-CSRFToken", csrfToken);
    var postData = new FormData();
    postData.append('sym', val);
    xhttp.send(postData);
}