function sip() {
    // var url = 'sipans/';
    var amount = $('#amount').val();
    var rate = $('#rate').val();
    var time_period = $('#time_period').val();
    // alert('inside sip()')
    $.ajax({
        url: 'sipans/',
        data: {
            'amount': amount,
            'rate': rate,
            'time_period': time_period,
        },
        success: function(data) {
            // var test_json = document.getElementById("test_json");
            // document.getElementById("test_json").innerHTML = data.amount + "  " + ", Marturity Amount " + data.maturity
            //     + "  " + data.rate + " " + data.time_period;
            document.getElementById("invest1").innerHTML = "Rs. " + data.invested_amount;
            document.getElementById("matty").innerHTML = "Rs. " + data.maturity;
        },
    });
}