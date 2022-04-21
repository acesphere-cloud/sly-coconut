odoo.define('website_sale_whatsapp_checkout', function (require) {
    'use strict';
    $(function () {
        $("input[type=radio]").change(function () {
            if (this.id == 'self_pick') {
                $("#check_address").addClass('d-none')
                $("#self_check_out").removeClass('d-none')
                $("#method_type").val('self_pick')
                $("#checkout_form").attr('target', '_new')

            }
            else if (this.id == 'home_delivery') {
                $("#check_address").removeClass('d-none')
                $("#self_check_out").addClass('d-none')
                $("#method_type").val('home_delivery')
                $("#checkout_form").attr('target', '_self')
            }
        });
        $("#address_checked").click(function () {
            setTimeout(location.reload.bind(location), 10000);
        });
        var millisecondsToWait = 10000;
        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
        $("#self_check_out").click(function () {
            sleep(millisecondsToWait).then(() => {
                window.location.href = '/shop/cart'
            })
        });
    });
});