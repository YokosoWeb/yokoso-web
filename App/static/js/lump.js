function lump() {
    var amount = $('#amount').val();
    var rate = $('#rate').val();
    var time_period = $('#time_period').val();

    $.ajax({
        url: 'lumpans/',
        data: {
            'amount': amount,
            'rate': rate,
            'time_period': time_period,
        },
        success: function (data) {
            document.getElementById("invest1").innerHTML = "Rs. " + data.invested_amount;
            document.getElementById("matty").innerHTML = "Rs. " + data.maturity;
        },
    });
}