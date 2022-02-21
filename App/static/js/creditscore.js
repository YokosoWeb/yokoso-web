const steps = Array.from(document.querySelectorAll("form .step"));
const nextBtn = document.querySelectorAll("form .next-btn");
const prevBtn = document.querySelectorAll("form .previous-btn");


// validate






nextBtn.forEach((button) => {
    button.addEventListener("click", () => {

        function validate() {

            // Check format Email
            var filter = /^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+$/;
            // var regx = /^[A-Za-z]+/;
            // var regx_fname = /^([\w]{3,})+\s+([\w\s]{3,})+$/;
            var regx_fname = /^[a-zA-Z0-9 ]+$/;

            // var regx_pan = /^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$/;
            var regx_pan = /^([A-Za-z]){5}([0-9]){4}([A-Za-z]){1}?$/;

            var regx_phone = /^[1-9][0-9]+$/;
            // var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            // var filter = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
            // var filter = /^[a-zA-Z0-9]/;

            let isvalid = 0;
            // console.log('hi')
            if (true) {
                // Validate
                console.log(fname.value, pan.value, emp.value, phone.value, email.value, dob.value, gender.value);

                if (fname.value == '') {
                    console.log(regx_fname.test(fname.value));
                    // alert('please fill name');
                    fname_msg.innerText = "*Please fill name"
                    isvalid += 1;
                    console.log(isvalid)
                        // return false
                } else {
                    if (!regx_fname.test(fname.value)) {
                        fname_msg.innerText = "*Please fill valid name"
                        isvalid += 1;
                    } else {
                        fname_msg.innerText = ""

                    }
                }


                if (pan.value == '' || pan.value.length != 10) {

                    console.log(regx_pan.test(pan.value));
                    pan_msg.innerText = "*Please fill PAN"

                    isvalid += 1;
                    console.log(isvalid)

                } else {
                    if (!regx_pan.test(pan.value)) {
                        pan_msg.innerText = "*Please fill valid PAN"
                        isvalid += 1;
                    } else {
                        pan_msg.innerText = ""
                    }

                }

                if (emp.value == '') {
                    emp_msg.innerText = "*Please fill Employment type"

                    isvalid += 1;
                    console.log(isvalid)

                } else {
                    emp_msg.innerText = ""

                }

                if (phone.value == '' || phone.value.length != 10) {

                    console.log(regx_phone.test(phone.value));
                    phone_msg.innerText = "*Please fill Phone Number"

                    isvalid += 1;
                    console.log(isvalid)

                } else {
                    if (!regx_phone.test(phone.value)) {
                        phone_msg.innerText = "*Please fill valid Phone Number"
                        isvalid += 1;
                    } else {
                        phone_msg.innerText = ""
                    }
                }


                if (email.value == '') {

                    console.log(filter.test(email.value));
                    email_msg.innerText = "*Please fill Email Address"

                    isvalid += 1;
                    console.log(isvalid)

                } else {
                    if (!filter.test(email.value)) {
                        email_msg.innerText = "*Please fill valid Email Address"
                        isvalid += 1;
                    } else {
                        email_msg.innerText = ""

                    }

                }
                if (!dob.value) {
                    dob_msg.innerText = "*Please fill DOB"

                    isvalid += 1;
                    console.log(isvalid)

                } else {
                    dob_msg.innerText = ""

                }
                if (gender.value == "") {
                    gender_msg.innerText = "*Please select gender"

                    isvalid += 1;
                    console.log(isvalid)

                } else {
                    gender_msg.innerText = ""

                }

                if (isvalid == 0) {
                    changeStep("next");

                    data = {
                            name: fname.value,
                            pan: pan.value,
                            phone: phone.value,
                            email: email.value,
                            dob: dob.value,
                            gender: gender.value,
                        }
                        // Permit for Post Request
                    sendPost(data);

                }

            }
        }
        validate();

    });
});
prevBtn.forEach((button) => {
    button.addEventListener("click", () => {
        changeStep("prev");
    });
});


function changeStep(btn) {
    let index = 0;
    const active = document.querySelector(".active");
    index = steps.indexOf(active);
    steps[index].classList.remove("active");
    if (btn === "next") {
        index++;
    } else if (btn === "prev") {
        index--;
    }
    steps[index].classList.add("active");
}


// Form Validation
function validate1() {
    let isvalid = 0;
    if (true) {
        // Validate


        if (ms.value == '') {
            // alert('please fill name');
            ms_msg.innerText = "*Please fill Salary"
            isvalid += 1;
            console.log(isvalid)

        } else {
            ms_msg.innerText = ""

        }
        if (oe.value == '') {
            // alert('please fill name');
            oe_msg.innerText = "*Please fill monthly emi"
            isvalid += 1;
            console.log(isvalid)

        } else {
            oe_msg.innerText = ""

        }
        if (loanType.value == '') {
            // alert('please fill name');
            loanType_msg.innerText = "*Please fill Loan type"
            isvalid += 1;
            console.log(isvalid)

        } else {
            loanType_msg.innerText = ""

        }
        if (la.value == '') {
            // alert('please fill name');
            la_msg.innerText = "*Please fill Loan Amount"
            isvalid += 1;
            console.log(isvalid)

        } else {
            la_msg.innerText = ""

        }

        if (month.value == '') {
            // alert('please fill name');
            month_msg.innerText = "*Please fill tenure in months"
            isvalid += 1;
            console.log(isvalid)

        } else {
            month_msg.innerText = ""

        }
        if (bank.value == '') {
            // alert('please fill name');
            bank_msg.innerText = "*Please fill preferred bank"
            isvalid += 1;
            console.log(isvalid)

        } else {
            bank_msg.innerText = ""

        }
        if (isvalid == 0) {
            return true
        } else {
            return false
        }
    }
}

function sendPost(data) {
    console.log('POST Data', data)
        // Constructing

    let u = window.location.href.split('/')
    u[3] = "emi-enquiry"
    u = u.join('/')


    // e.preventDefault()
    // Making the AJAX Request

    $.ajax({
        url: u,
        type: "POST",
        data: data,
        beforeSend: function(xhr) {

            xhr.setRequestHeader("X-CSRFToken", $('[name=csrfmiddlewaretoken]').val());
        },
        success: function(data) {
            console.log(data);
        },
        error: function(error) {
            console.log(error);
        }
    });
}
//ritika

$('#my').click(function() {

    var url = '/emi-pro/personalDetails/';
    var name = $('#fname').val();
    var pan = $('#pan').val();
    var phone = $('#phone').val();
    var employmentType = $('#emp').val();
    var email = $('#email').val();
    var dob = $('#dob').val();
    var gender = $('#gender').val();

    $.ajax({
        url: url,
        data: {
            'name': name,
            'pan': pan,
            'phone': phone,
            'employmentType': employmentType,
            'email': email,
            'dob': dob,
            'gender': gender

        },

        success: function(data) {

            document.getElementById('id').value = data;
            alert("Wait");



        }
    });


});




$('#sub').click(function() {

    var url = '/emi-pro/submit/';
    var ide = $('#id').val();
    var la = $('#la').val();
    var bank = $('#bank').val();
    var salary = $('#ms').val();
    var emi = $('#oe').val();
    var loanType = $('#loanType').val();
    var tenure = $('#month').val();



    $.ajax({
        url: url,
        data: {
            'ide': ide,
            'la': la,
            'bank': bank,
            'salary': salary,
            'emi': emi,
            'loanType': loanType,
            'tenure': tenure,

        },

        success: function(data) {

            alert("Wait")



        }
    });

    return temp;

});