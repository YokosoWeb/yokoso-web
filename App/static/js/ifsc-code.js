$("#service").change(function() {

    if ($("#service").val() == 'IFSC Code') {
        document.getElementById("statesss").style.display = "block";
        document.getElementById("citiess").style.display = "block";
        document.getElementById("branchess").style.display = "block";
        document.getElementById("ifsc_code_form").style.display = "block";
        document.getElementById("enter-ifsc-code").style.display = "block";
    } else {
        document.getElementById("statesss").style.display = "none";
        document.getElementById("citiess").style.display = "none";
        document.getElementById("branchess").style.display = "none";
        document.getElementById("ifsc_code_form").style.display = "none";
        document.getElementById("enter-ifsc-code").style.display = "none";

    }

});


$("#service").change(function() {

    $("#State_Name").removeAttr('disabled');
    $("#City_Name").removeAttr('disabled');
    $("#Branch_Name").removeAttr('disabled');
    const selectedService = $(this).val(); // get the selected ServiceHTML input
    if ($("#service").val() == '' || $("#service").val() == 'Grievance') {

        $.ajax({ // initialize an AJAX request
            url: 'grievance/', // set the url of the request
            data: {
                'service': selectedService // add the country id to the GET parameters
            },

            success: function(data) { // `data` is the return of the `load_cities` view function
                let html_data = '<option value="">Select Bank</option>';
                data.forEach(function(grievance) {
                    html_data += `<option value="${grievance.id}">${grievance.Bank}</option>`

                });
                $("#BankName").html(html_data);
                $("#State_Name").attr('disabled', 'disabled');
                $("#City_Name").attr('disabled', 'disabled');
                $("#Branch_Name").attr('disabled', 'disabled');

                return;
            }

        });

    } else {
        $.ajax({ // initialize an AJAX request
            url: 'bankname/', // set the url of the request
            data: {
                'service': selectedService // add the country id to the GET parameters
            },

            success: function(data) { // `data` is the return of the `load_cities` view function
                let html_data = '<option value="">Select Bank</option>';
                data.forEach(function(IfscData) {
                    html_data += `<option value="${IfscData.BANK}">${IfscData.BANK}</option>`
                });

                $("#BankName").html(html_data);

            }

        });

    }

});



// function mychange() {
//     alert("onchangeiii");
// }

// function yesnoCheck(that) {
//     alert("hiii")
//     if (that.value == "Grievance") {
//         alert("check");
//         document.getElementById("statesss").style.display = "block";
//     } else {
//         document.getElementById("statesss").style.display = "none";
//     }
// }

$("#BankName").change(function() {
    document.getElementById('error').innerHTML = " ";
    const selectedBank = $(this).val(); // get the selected ServiceHTML input

    $.ajax({ // initialize an AJAX request
        url: 'statename/', // set the url of the request
        data: {
            'bank': selectedBank
                // add the country id to the GET parameters
        },

        success: function(data) { // `data` is the return of the `load_cities` view function
                let html_data = '<option value="">Select State</option>';
                data.forEach(function(IfscData) {
                    html_data += `<option value="${IfscData.STATE}">${IfscData.STATE}</option>`
                });

                $("#State_Name").html(html_data);
                // replace the contents of the city input with the data that came from the server

            } // replace the contents of the city input with the data that came from the server  

    });

});

$("#State_Name").change(function() {

    document.getElementById('error').innerHTML = " ";
    var bank = $('#BankName :selected').val();

    const selectedState = $(this).val();


    $.ajax({ // initialize an AJAX request
        url: 'cityname/', // set the url of the request
        data: {

            'state': selectedState,
            'bank': bank // add the country id to the GET parameters
        },
        success: function(data) { // `data` is the return of the `load_cities` view function
                let html_data = '<option value="">Select District</option>';
                data.forEach(function(IfscData) {
                    html_data += `<option value="${IfscData.DISTRICT}">${IfscData.DISTRICT}</option>`
                });

                $("#City_Name").html(html_data);
                // replace the contents of the city input with the data that came from the server

            } // replace the contents of the city input with the data that came from the server  

    });

});

$("#City_Name").change(function() {


    document.getElementById('error').innerHTML = " ";
    var bank = $('#BankName :selected').val();
    var state = $('#State_Name :selected').val();
    const selectedCity = $(this).val();


    $.ajax({ // initialize an AJAX request
        url: 'branchname/', // set the url of the request
        data: {

            'city': selectedCity,
            'bank': bank,
            'state': state // add the country id to the GET parameters
        },
        success: function(data) { // `data` is the return of the `load_cities` view function
                let html_data = '<option value="">Select Branch</option>';
                data.forEach(function(IfscData) {
                    html_data += `<option value="${IfscData.id}">${IfscData.ADDRESS}</option>`
                });

                $("#Branch_Name").html(html_data);
                // replace the contents of the city input with the data that came from the server

            } // replace the contents of the city input with the data that came from the server  

    });

});

function myFunction() {
    document.getElementById('error').innerHTML = " ";
    var bank = $('#BankName :selected').val();
    var branch = $('#Branch_Name :selected').val();



    if ($("#Branch_Name").val()) {
        $.ajax({
            url: 'ifscfilter/',
            data: {
                'branch': branch,
            },
            success: function(data) {

                $('#ifsc-code-display').html(jQuery(data).find('#ifsc-code-display').html()); // replace the contents of the city input with the data that came from the server

            }
        });
    } else if ($('#BankName').val()) {
        $.ajax({
            url: 'grievancefilter/',
            data: {
                'bank': bank,
            },
            success: function(data) {
                $('#ifsc-code-display').html(jQuery(data).find('#ifsc-code-display').html()); // replace the contents of the city input with the data that came from the server

            }
        });

    } else {
        document.getElementById('error').innerHTML = "Please select all the Fields.";
    }
}



$(function() {
    $('#ifsc_no_exact').keyup(function() {

        $(this).val($(this).val().toUpperCase());
    });
});




function clickFunction() {
    document.getElementById('errorrs').innerHTML = " ";
    document.getElementById('errormsg').innerHTML = " ";

    var ifsc_no = $('#ifsc_no_exact').val()

    if ($("#ifsc_no_exact").val()) {
        $.ajax({ // initialize an AJAX request
            url: ifsc_no, // set the url of the request
            success: function(data) { // `data` is the return of the `load_cities` view function

                $('#ifsc-code-display').html(jQuery(data).find('#ifsc-code-display').html());
                if ($('#ifsc-code-display').html().length < 50) {
                    document.getElementById('errorrs').innerHTML = "Please Enter Valid IFSC CODE.";
                }
            }

        });
    } else {

        document.getElementById('errormsg').innerHTML = " Enter IFSC CODE.";
        return false;
    }
}