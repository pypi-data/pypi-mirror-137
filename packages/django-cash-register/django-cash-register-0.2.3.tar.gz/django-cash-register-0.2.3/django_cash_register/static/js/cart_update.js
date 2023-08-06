$(document).on('click', '.item-remove-all', function (){
    $.ajax({
        type: 'POST',
        url: cartBtns_url,
        data: {
            'cart_number': cart_number,
            'operation': 'item_remove_all',
            'csrfmiddlewaretoken': csrf_token
        },
        dataType: 'json',
        error: function (){
            console.log('Error: item-remove-all')
        }
    });
});

$(document).on('click', '.item-counter-plus', function (){
    $.ajax({
        type: 'POST',
        url: cartBtns_url,
        data: {
            'product_id': $(this).attr('name'),
            'operation': 'item_counter_plus',
            'csrfmiddlewaretoken': csrf_token
        },
        dataType: 'json',
        error: function (){
            console.log('Error: item-counter-plus')
        }
    });
});

$(document).on('click', '.item-counter-minus', function (){
    $.ajax({
        type: 'POST',
        url: cartBtns_url,
        data: {
            'product_id': $(this).attr('name'),
            'operation': 'item_counter_minus',
            'csrfmiddlewaretoken': csrf_token
        },
        dataType: 'json',
        error: function (){
            console.log('Error: item-counter-minus')
        }
    });
});

$(document).on('click', '.item-remove', function (){
    $.ajax({
        type: 'POST',
        url: cartBtns_url,
        data: {
            'product_id': $(this).attr('name'),
            'operation': 'item_remove',
            'csrfmiddlewaretoken': csrf_token
        },
        dataType: 'json',
        error: function (){
            console.log('Error: item-remove')
        }
    });
});

$(document).on('click', '.sell', function (){
    $.ajax({
        type: 'POST',
        url: cartBtns_url,
        data: {
            'cart_number': cart_number,
            'operation': 'sell',
            'csrfmiddlewaretoken': csrf_token
        },
        dataType: 'json',
        error: function (){
            console.log('Error: sell')
        }
    });
});