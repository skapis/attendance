$(document).ready(function(){

    var today = new Date()
    var months = ['Leden', 'Únor', 'Březen', 'Duben', 'Květen', 'Červen', 'Červenec', 'Srpen', 'Září', 'Říjen', 'Listopad', 'Prosinec']

    $('[name="month"]')
    .append($('<option>', {
        value: today.getMonth() +1,
        text:  months[today.getMonth()]
    }))
    .append($('<option>', {
        value: today.getMonth(),
        text:  months[today.getMonth() -1]
    }))
;

    const searchParams = new URLSearchParams(window.location.search)
    if (searchParams.has('month')){
        $('[name="month"]').val(searchParams.get('month'))
        $('[name="year"]').val(searchParams.get('year'))
    } else {
        $('[name="month"]').val(today.getMonth()+1)
        $('[name="year"]').val(today.getFullYear())
    }


    $('[name="year"]')
        .append($('<option>', {
            value: today.getFullYear(),
            text:  today.getFullYear()
        }))
        .append($('<option>', {
            value: today.getFullYear() - 1,
            text:  today.getFullYear() - 1
        }))
    ;

    $('.bi-x').each(function(){
        $(this).on('click', () => {
            var bix = $('.bi-x').index(this)
            var msg = $('.bi-x')
            $(msg[bix]).parent().remove()
        })
    })

    $('#showBtn').click(function(){
        var month = $('[name="month"]').val()
        var year = $('[name="year"]').val()
        window.location.href = window.location.pathname + '?year=' + year + '&month=' + month
    })


})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
        }
    }
    return cookieValue;
}


function getMessage(text, type, action){
    var message = 
        '<div class="messages">' +
            '<div class="row mx-0 align-items-center ' + action + ' alert alert-sm rounded-sm alert-'+ type +'">' +
                '<div>' + text + '</div>'+
                '<a class="bi bi-x ml-auto"></a>' + 
            '</div>'
        '</div>';
    
    return message
}