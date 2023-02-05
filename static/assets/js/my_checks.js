
// const letters = /^[A-Za-z]+$/;
// const letters_no_space = /^[a-zA-Z()]*$/
// const letters_no_space2 = /^[a-zA-Z() ]+$/
// const regex_email_ = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;

function check_11_length(item){

    item.keypress(function(event){
        if ($(this).val().length === 11){
            $(this).removeClass('is-invalid')
            $(this).addClass('is-valid')
        }else{
            $(this).removeClass('is-valid')
            $(this).addClass('is-invalid')
        }
    });
}

function check_name_length(item, val){

    item.keypress(function(event){

        if ($(this).val().length > val){
            $(this).removeClass('is-invalid')
            $(this).addClass('is-valid')
        }else{
            $(this).removeClass('is-valid')
            $(this).addClass('is-invalid')
        }

    });
}

function check_email(item){
    if (/^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/.test(item.val()))
    {
        $(this).removeClass('is-invalid')
        $(this).addClass('is-valid')

    }else{
        $(this).addClass('is-invalid')
    }
}

function isAlphaOrParen(str) {
    return /^[a-zA-Z() ]+$/.test(str);
}

function change_color_to_orange(val) {
        val.removeClass('bg-green')
        val.addClass('bg-orange')

    }

    function change_color_to_green(val) {
        val.removeClass('bg-orange')
        val.addClass('bg-green')
    }



// if($(this).val().match(letters_no_space2)){
//           $(this).removeClass('is-invalid')
//           $(this).addClass('is-valid')
//      }else {
//          $(this).removeClass('is-valid')
//          $(this).addClass('is-invalid')
//           return
//      }