$(document).ready(function (){
    setInterval(function(){
        $.ajax({
            type: 'GET',
            url: getCartItems_url,
            success: function (response) {
                if (last_update !== response['new_update']) {
                    last_update = response['new_update'];

                    $(".item-remove-all").remove();
                    let prodcts_count = response['products'].length;

                    if (prodcts_count !== 0) {
                        $(".header-container").append(
                            "<a href=\"\" class=\"item-remove-all\">" +
                            "<button class=\"items-remove-all btn-remove\">Remove all</button>" +
                            "</a>"
                        );

                        $(".cart-container").empty().append("<hr class=\"cart-item-separator\">");
                        for (let i in response['products']) {
                            let image;
                            if (response['products'][i]['product__image'].length > 0){
                                image = "src=\"" + response['products'][i]['product__image'] + "\" ";
                            } else {
                                image = image = "src=\"static/images/defaul_image.png\"";
                            }

                            let temp =
                                "<div class=\"cart-item\"><div class=item-image>" +
                                "<img " +
                                image +
                                "alt=\"" + response['products'][i]['product__name'] + "\" " +
                                "loading=\"lazy\" " +
                                "width=\"80\" " +
                                "height=\"100\"/>" +
                                "</div>" +
                                "<div class=\"item-about\">" +
                                "<div class=\"item-title\">" +
                                "<p class=\"item-about-inner\">" + response['products'][i]['product__name'] + "</p>" +
                                "</div>" +
                                "<div class=\"item-subtitle\">" +
                                "<p class=\"item-about-inner\">" +
                                response['products'][i]['product__weight'] + ".0 " + response['products'][i]['product__unit__name'] +
                                "</p>" +
                                "</div>" +
                                "</div>" +
                                "<div class=\"item-counter\">" +
                                "<div class=\"item-counter-container\">" +
                                "<a href=\"\" name=\"product_" + response['products'][i]['pk'] + "\" class=\"item-counter-plus\">" +
                                "<button class=\"item-counter-btn item-counter-btn-animation\">+</button>" +
                                "</a>" +
                                "<div class=\"item-counter-count\">" + response['products'][i]['product_count'] + ".0</div>" +
                                "<a href=\"\" name=\"product_" + response['products'][i]['pk'] + "\" class=\"item-counter-minus\">" +
                                "<button class=\"item-counter-btn item-counter-btn-animation\">-</button>" +
                                "</a>" +
                                "</div>" +
                                "</div>" +
                                "<div class=\"item-price\">";
                            if (response['currency'][1] === true) {
                                temp = temp +
                                    "<div class=\"item-amount\">" + response['products'][i]['total_price'] + ".0" + response['currency'][0] + "</div>" +
                                    "<a href=\"\" name=\"product_" + response['products'][i]['pk'] + "\" class=\"item-remove\">" +
                                    "<button class=\"btn-remove\">Remove</button>" +
                                    "</a>" +
                                    "</div>" +
                                    "</div>" +
                                    "<hr class=\"cart-item-separator\">";
                            } else {
                                temp = temp +
                                    "<div class=\"item-amount\">" + response['currency'][0] + response['products'][i]['total_price'] + ".0" + "</div>" +
                                    "<a href=\"\" name=\"product_" + response['products'][i]['pk'] + "\" class=\"item-remove\">" +
                                    "<button class=\"btn-remove\">Remove</button>" +
                                    "</a>" +
                                    "</div>" +
                                    "</div>" +
                                    "<hr class=\"cart-item-separator\">";

                            }
                            $(".cart-container").append(temp);
                        }
                    } else {
                        $(".cart-container").empty().append("<hr class=\"cart-item-separator\">");
                    }
                    if (prodcts_count == 1){
                        item_s = 'item';
                    } else if (prodcts_count == 0 || prodcts_count > 1){
                        item_s = 'items';
                    }
                    
                    $(".subtotal-items").empty().append("<p>" + response['products'].length + " "+item_s+"</p>");

                    if (response['currency'][1] === true) {
                        $(".total-amount-inner").empty().append(response['total_price'] + ".0" + response['currency'][0]);
                    } else {
                        $(".total-amount-inner").empty().append(response['currency'][0] + response['total_price'] + ".0");
                    }
                }
            },
            error: function (response){
                console.log('Error: gestCartItems')
            }
        });
    },1000);
});