// Datatable Functions ::
var datetable_language = {
    search: "_INPUT_", // Removes the 'Search' field label
    searchPlaceholder: "Search", // Placeholder for the search box
    sLengthMenu: "_MENU_",
    sInfo: "_START_ to _END_ of _TOTAL_",
    sInfoEmpty: "0 to 0 of 0",
    sInfoFiltered: "(filtered from _MAX_ total records)"
}
// commom
var errormsg_something = "Somthing Went Wrong"
var mutlitable_blankerror = "Please enter text in  "
var validate_futuredaterestriction = "Don't Select Future Date"
var validate_permissionrestricte = "You don't have Permission !"
// in main js
var validate_emptyfield = "This field should not be empty";
var validate_selectfield = "Please select any one value";
var validate_emailfield = "Please enter valid email";
var validate_itemselect = 'Please select Product'
var validate_billtypeselect = 'Please select Billtype'
var validate_unitselect = 'please select Unit'
var validate_itemadd = 'Please Add Product'


// SHOW MESSAGES FOR ERROR ::
function showMsg(msg, type) {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
    });

    Toast.fire({
        icon: (type == 1 ? 'success' : 'error'),
        title: `<span style='font-size: 15px; font-family: Arial, sans-serif;'>${msg}</span>`
    })
}



$(document).ready(function () {
    // Set up click event for the clear button
    $('#btnCancel').on('click', function () {
        window.location.replace(window.location.href);
    });
});




// Form Validation Functions ::
function check_validate_forms(formId) {
    let isValid = true;

    // Clear previous error messages
    $(`${formId} .error-message`).text("");

    // Validate only inputs with the data-validate attribute
    $(`${formId} [data-validate="true"]`).each(function () {
        const inputField = $(this);
        const labelText = inputField.prev('label').text().trim(); // Get label text once for reuse
        const isEmptyLabel = labelText === "" ? 'This field' : labelText;

        // Validate text inputs and textareas
        if (inputField.is("input[type='text'], textarea")) {
            if (inputField.val().trim() === "") {
                isValid = false;
                inputField.next('.error-message').text(`${isEmptyLabel} is required.`);
            }
        }

        // Validate email inputs
        if (inputField.is("input[type='email']")) {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Simple email regex
            if (inputField.val().trim() === "") {
                isValid = false;
                inputField.next('.error-message').text(`${isEmptyLabel} is required.`);
            } else if (!emailPattern.test(inputField.val().trim())) {
                isValid = false;
                inputField.next('.error-message').text(`${isEmptyLabel} is not a valid email address.`);
            }
        }

        // Validate password inputs
        if (inputField.is("input[type='password']")) {
            if (inputField.val().trim() === "") {
                isValid = false;
                inputField.next('.error-message').text(`${labelText} is required.`);
            } else if (inputField.val().length < 8) { // Minimum length condition
                isValid = false;
                inputField.next('.error-message').text(`${labelText} must be at least 8 characters long.`);
            }
        }

        // Validate file inputs
        if (inputField.is("input[type='file']")) {
            if (inputField.get(0).files.length === 0) {
                isValid = false;
                inputField.next('.error-message').text(`${labelText} is required.`);
            }
        }

        // Generic required field check
        if (inputField.val() === "" || inputField.val() === "0") {
            isValid = false;
            const errorMsg = `${labelText} is required.`;
            inputField.siblings('.error-message').text(errorMsg);
        }
    });

    return isValid; // Return true if valid, false otherwise
}



// Clear input error validation messages ::
function clearErrorMessageOnInput(formId) {
    $(`${formId} input[data-validate="true"], ${formId} textarea[data-validate="true"], ${formId} input[type="email"], ${formId} select[data-validate="true"]`).on('input change', function () {
        const errorMessageElement = $(this).next('.error-message');
        errorMessageElement.text(""); // Clear the error message

        // Specifically handle the change event for the dropdown
        $(`${formId} select[data-validate="true"]`).on('change', function () {
            const errorMessageElement = $(this).next('.error-message');
            errorMessageElement.text(""); // Clear the error message
        });
    });
}



// Function to handle file upload and validation
function handleFileUpload(id) {

    $('#' + id).click();
    if (!$('#' + id).data('change-setup')) {
        $('#' + id).data('change-setup', true);

        $('#' + id).on('change', function () {
            var file = this.files[0];
            if (!file) {
                showMsg("Please select a file.");
                return;
            }
            if (file.size > 2 * 1024 * 1024) {
                showMsg("File size must be less than 2MB.");
                return;
            }
            var img = new Image();
            var reader = new FileReader();

            reader.onload = function (e) {
                img.src = e.target.result;

                img.onload = function () {
                    if (img.width !== img.height) {
                        showMsg("Image must have a 1:1 aspect ratio.");
                        return;
                    }
                    $('#previewImage').attr('src', e.target.result);
                    $('.file-upload-info').val(file.name);
                };
            };
            reader.readAsDataURL(file);
        });
    }
}

// Datatable to Pdf ::
function ExporttabletoPdf(id, filename, colcount, btnDate = '') {
    var contentlist = [`Velan foods`]
    var titlename = filename.replaceAll('_', ' ')
    if (btnDate != '') {
        var reportdate = $('#' + btnDate).text()
        titlename = titlename + ' ( ' + reportdate + ' )'
    }
    contentlist.push(titlename)
    var reporton = 'Date : ' + moment().format('DD.MM.YYYY');
    contentlist.push(reporton)
    ExporttabletoPdfmain(id, filename, colcount, contentlist)
}

// Confirm Modal delete ::
function confirmDelete(event, titleName = null, userId = null) {
    event.preventDefault();

    // Customize the message based on the category
    const messageText = titleName ? `Want to delete the ${titleName} ?` : "Want to delete this!";

    Swal.fire({
        title: 'Are you sure?',
        text: messageText,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#4BB543',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            // Redirect based on whether userId is provided or not
            if (userId === null) {
                window.location.href = event.target.href;
            } else {
                window.location.href = userId;
            }
        }
    });
}


// Toggle Active status 
function confirmStatusChange(id, url, tblId, status, chkswitch, content) {

    Swal.fire({
        title:
            status == 1
                ? "<h6 class='text-left'>Change the status</h6>"
                : "<h6 class='text-left'>Change the status</h6>",
        text: `Are you sure? Do you want to change ${content} status?`,
        icon: status == 1 ? "warning" : "error",
        showCancelButton: true,
        confirmButtonText:
            status == 1 ? "Yes, Activate it!" : "Yes, Deactivate it!",
        customClass: {
            confirmButton: "btn btn-success me-4",
            cancelButton: "btn btn-light",
        },
        buttonsStyling: false,

    }).then(function (result) {

        if (result.value) {

            statusUpdate(id, url, status);

            Swal.fire({
                icon: "success",
                title: status == 0 ? "<h4 class='text-center'>DeActivated!</h4>" : "<h4 class='text-center'>Activated!</h4>",
                text:
                    status == 0
                        ? ""
                        : "",
                customClass: {
                    confirmButton: "btn btn-success me-4",
                },

            });

        } else {

            $("#" + chkswitch + id).prop("checked", status == 1 ? false : true);

        };
    });
};

// Toggle status update ::
function statusUpdate(id, url, status) {

    $.ajax({
        type: "GET",
        url: url,
        data: {
            'id': id,
            'sts': status
        },
        dataType: "json",
        success: function (data) {
            if (data == 200) {
                showMsg('Settings Updated Successfully', 1)
            }
            else {
                showmsg('Failed To Update Settings')
            };
            return true;
        },
    });

};

function numbervalidation(event, count = null) {
    if (event.target.value.length > count && count != null) {
        return false
    }
    var patten = /[0-9]/
    if (!patten.test(event.key)) {
        return false
    }
}

// Function to decode HTML entities
function decodeHtmlEntities(encodedString) {
    var textArea = document.createElement('textarea');
    textArea.innerHTML = encodedString;
    return textArea.value;
}

function decimalvalidation(event, maxvalue = null, count = null) {
    var patten = /[0-9.]/
    if (!patten.test(event.key)) {
        return false
    }
    if (maxvalue != null) {
        var inputvalue = (event.target.value).toString() + event.key
        var floatinput = parseFloat(inputvalue)
        var floatmaxvalue = parseFloat(maxvalue)
        if (floatmaxvalue < floatinput) {
            return false
        }
    }
    if (event.target.value.length > count && count != null) {
        return false
    }
}


