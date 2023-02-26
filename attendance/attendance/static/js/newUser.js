$(document).ready(function(){

    var username = $('#userName') 
    username.keyup(function(){
        if(username.val() != ''){
            $.ajax({
                type: 'POST',
                url: 'check-user',
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                data: JSON.stringify({
                    'username': username.val(),
                }),
                success: function(data){
                    $('.userFeedbackArea').removeClass('d-block')
                    username.removeClass('is-invalid')
                    username.addClass('is-valid')
                    $('#submitBtn').prop('disabled', false)
                },
                error: function(xhr){
                    username.removeClass('is-valid')
                    username.addClass('is-invalid')
                    $('#submitBtn').prop('disabled', true)
                    $('.userFeedbackArea')
                        .append($('<p/>').text('Uživatel s tímto jménem již existuje'))
                        .addClass('d-block')
                }
            });
        } else {
            username.removeClass('is-valid')
        }
    });

    var password = $('[name="pass1"]')
    var confirmpass = $('[name="pass2"]')
    password.keyup(function(){
        if (CheckPassword(password.val())){
            password.removeClass('is-invalid')
            password.addClass('is-valid')
            $('.passCheckArea')
                .removeClass('d-block')
            $('.passCheckHint').show()
            $('#submitBtn').prop('disabled', false)
        } else {
            password.removeClass('is-valid')
            password.addClass('is-invalid')
            $('.passCheckHint').hide()
            $('.passCheckArea')
                .empty()
                .append($('<p/>').text('Heslo neodpovídá požadavkům. 6 znaků, číslice, velká písmena'))
                .addClass('d-block')
            $('#submitBtn').prop('disabled', true)
        }
    })
    confirmpass.keyup(function(){
        if(password.val() != confirmpass.val()){ // function for validate password
            password.removeClass('is-valid')
            password.addClass('is-invalid')
            confirmpass.removeClass('is-valid')
            confirmpass.addClass('is-invalid')
            $('.passwordCheckArea')
                .empty()
                .append($('<p/>').text('Zadaná hesla se neshodují'))
                .addClass('d-block')
            $('#submitBtn').prop('disabled', true)
        } else {
            password.removeClass('is-invalid')
            password.addClass('is-valid')
            confirmpass.removeClass('is-invalid')
            confirmpass.addClass('is-valid')
            $('.passwordCheckArea')
                .removeClass('d-block')
            $('#submitBtn').prop('disabled', false)
        }
    })

})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
        }
    }
    return cookieValue;
}


function CheckPassword(password){ 
    var passw = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/;
    if(password.match(passw)) { 
        return true;
    } else { 
    return false;
    }
}