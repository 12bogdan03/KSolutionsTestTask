$(document).ready(function(){
    var form = $('form[name="Pay"]');
    var usd = '840';
    var eur = '978';

    var selected = usd;
    $('#currency').on('change', function (e) {
        selected = this.value;
        if (selected === usd) {
            form.attr('action', 'https://tip.pay-trio.com/en/');
        }
    });

    function process_form() {
        var data = {
            amount: $('#amount').val(),
            currency: $('#currency').val(),
            description: $('#description').val()
        };

        if (selected === eur) {
            data['payway'] = 'payeer_eur';
        }

        $.ajax({
            url : '/ajax-data',
            type : 'post',
            data : data,
            success : function(result) {
                $('input[name="sign"]').val(result.sign);
                $('input[name="shop_invoice_id"]').val(result.shop_invoice_id);
            },
            complete: function() {
                if (selected === usd) {
                    form.off('submit');
                    form.submit();
                } else if (selected === eur) {
                    invoice();
                }
            }
        });
    }

    function invoice() {
        $.ajax({
            url : '/ajax-invoice',
            type : 'post',
            data : form.serialize(),
            success : function(result) {
                if (result.status === 'ok') {
                    form.html(result.new_form_html);
                    form.attr('method', result.method);
                    form.attr('action', result.action);
                    form.off('submit');
                    form.submit();
                }
            }
        });
    }

    form.submit(function(e) {
        e.preventDefault();
        e.returnValue = false;
        process_form();
    });

    // Input validation
    $("#amount").keyup(function() {
        if (!$.isNumeric($(this).val())) {
            $("#amount-errors").text('Please, enter valid amount.');
            $("input[type=submit]").css('cursor', 'not-allowed');
            $("input[type=submit]").prop('disabled', true);
        } else {
            $("#amount-errors").empty();
            $("input[type=submit]").css('cursor', 'pointer');
            $("input[type=submit]").prop('disabled', false);
        }
    });
    $("#description").keyup(function() {
        if ($(this).val().length > 300) {
            $("#description-errors").text('Enter less than 300 characters.');
            $("input[type=submit]").css('cursor', 'not-allowed');
            $("input[type=submit]").prop('disabled', true);
        } else if ($(this).val().length < 1) {
            $("#description-errors").text('Enter more than 1 character.');
            $("input[type=submit]").css('cursor', 'not-allowed');
            $("input[type=submit]").prop('disabled', true);
        } else {
            $("#description-errors").empty();
            $("input[type=submit]").css('cursor', 'pointer');
            $("input[type=submit]").prop('disabled', false);
        }
    });
});