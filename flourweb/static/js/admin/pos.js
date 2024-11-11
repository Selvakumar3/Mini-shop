var Rowcount = 0
$(document).ready(function () {

    if (itemdetail_data != '') {
        data_bindingitemtable()

        // Parse the date
        let date = new Date(get_pos_date);
        let day = String(date.getDate()).padStart(2, '0');
        let month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-indexed
        let year = date.getFullYear();

        let formattedDate = `${day}-${month}-${year}`;
        $('#txtInvoiceDate').val(formattedDate);
        $('#txtInvoiceDate').addClass('input-readonly');
        $('#txtInvoiceDate').attr('readonly', true);

    } else {
        // DatePicker
        var today = new Date();
        $('#txtInvoiceDate', '#datepicker-popup').datepicker({
            format: 'dd/mm/yyyy',
            startDate: '+0d',
            autoclose: true
        }).datepicker('setDate', today);
    }

    $('#ddlCategory').select2({
        minimumResultsForSearch: 0 // Ensures the search box is always visible
    });
    $('#ddlBillType').select2({
        minimumResultsForSearch: 0 // Ensures the search box is always visible
    });

    $('#ddlCategory').change(function () {
        const selectedOption = $(this).find('option:selected');
        const imageSrc = selectedOption.data('img');
        const baseUrl = api_img_url; // Change this to your actual base URL
        if (imageSrc) {
            $('#previewimage').attr('src', baseUrl + imageSrc);
        } else {
            $('#previewimage').attr('src', '/static/images/no-img-avatar.png');
        }
    });

    $('#txtActualWeight').on('input', function () {

        let actualWeight = parseFloat($(this).val());
        if (!isNaN(actualWeight)) {
            let halfWeight = actualWeight / 2;
            $('#txtAverageWeight').val(halfWeight.toFixed(2));
            $('#txtPrice').val((halfWeight * pos_amt).toFixed(2));
        } else {
            $('#txtAverageWeight').val(0);
            $('#txtPrice').val(0);
        }
    });
});

function data_bindingitemtable() {

    $('#btnSubmit').html('Update')
    var String_json = decodeHtmlEntities(itemdetail_data)
    if (String_json && String_json.trim() !== '') {
        var itemdetaillist = $.parseJSON(String_json);
        $.each(itemdetaillist, function (idx, val) {
            categoryId = val.category,
            categoryName = val.category_name,
            actWeight = val.actual_wgt,
            avgWeight = val.avg_wgt,
            totalAmount = val.total_amount
            updateitemtable(0,categoryId, categoryName, actWeight, avgWeight, totalAmount)
        })
    } else {
        console.error("Invalid JSON: ", String_json);
    }
}


// Once Add button click data added in table ::
function itemaddbutton() {
    if ($('#ddlCategory').val() == '0') {
        showMsg('Please select category')
        return false
    }
    var fieldsToCheck = $('#txtActualWeight,#txtAverageWeight,#txtPrice');
    var blankFieldIDs = fieldsToCheck.filter(function () {
        return $(this).val() === '';
    }).map(function () {
        return this.id;
    }).get();
    if (blankFieldIDs.length != 0) {
        $.each(blankFieldIDs, function (idx, val) {
            if ($('#' + val).parent().find("span.errormsg").length == 0) {
                $('#' + val).parent().append("<span class='errormsg fs-14' style='color':red>" + validate_emptyfield + "</span>");
            }
        })
        showMsg(mutlitable_blankerror + blankFieldIDs.join(", "));
        return false
    }
    var categoryId = $('#ddlCategory').val()
    var categoryName = $('#ddlCategory option:selected').attr('categoryName')
    var actWeight = $('#txtActualWeight').val()
    var avgWeight = $('#txtAverageWeight').val()
    var totalAmount = $('#txtPrice').val()
    var method = $('#additembtn').attr('row')
    updateitemtable(method, categoryId, categoryName, actWeight, avgWeight, totalAmount)
}

// Data added on table
function updateitemtable(method, categoryId, categoryName, actWeight, avgWeight, totalAmount) {
    if ($('#emptyitemrow').length != 0) {
        $('#emptyitemrow').remove()
    }
    if (method == 0) {
        Rowcount++
        var bindingtext = ``
        bindingtext += `<tr id="itemrowid_${Rowcount}" rowid="${Rowcount}" categoryId="${categoryId}" categoryName="${categoryName}" actWeight="${actWeight}" 
                        avgWeight="${avgWeight}" totalAmount="${totalAmount}">`

        bindingtext += itemtablecontent(Rowcount, categoryName, actWeight, avgWeight, totalAmount)

        bindingtext += `</tr>`
        $('#itemtablebody').append(bindingtext)
    } else {
        var rowid = $('#itemrowid_' + method)
        rowid.attr('categoryId', categoryId)
        rowid.attr('categoryName', categoryName)
        rowid.attr('actWeight', actWeight)
        rowid.attr('avgWeight', avgWeight)
        rowid.attr('totalAmount', totalAmount)
        rowid.html(itemtablecontent(method, categoryName, actWeight, avgWeight, totalAmount))
    }
    $('#ddlCategory').val('0').trigger('change')
    $('#txtActualWeight').val('')
    $('#txtAverageWeight').val('')
    $('#txtPrice').val('')
    $('#additembtn').attr('row', '0')
    $('#additembtn').removeClass('btn-warning')
    $('#additembtn').addClass('btn-primary')
    $('.errormsg').html('')
    setitemtablesno()
}

function itemtablecontent(Rowcount, categoryName, actWeight, avgWeight, totalAmount) {
    var bindingcontent = ''
    bindingcontent += `<td class="align-middle text-center" id="snoid_${Rowcount}"></td>
    <td class="align-middle text-center">${categoryName}</td>
    <td class="align-middle text-center">${actWeight} kg</td>
    <td class="align-middle text-center">${avgWeight} kg</td>
    <td class="align-middle text-center">${totalAmount}</td>
    <td class="align-middle add-remove text-end ">
    <a href="javascript:void(0);"class="btn btn-success btn-rounded btn-icon" onclick="edititemrow(${Rowcount})" title="Edit" ><i class="ti-pencil-alt" style="font-size: 20px;"></i></a>
    <a href="javascript:void(0);" class="btn btn-danger btn-rounded btn-icon" onclick="deleteitemrow(${Rowcount})" title="Delete"><i class="ti-trash"></i></a>
    </td>`
    return bindingcontent
}

function setitemtablesno() {
    if ($("[id^='itemrowid_']").length == 0) {
        $('#itemtablebody').html(`<tr id="emptyitemrow">
                                        <td colspan="6" class="text-center p-2">no item here</td>
                                    </tr>`)
    }

    var TotAmt = 0

    $("[id^='snoid_']").each(function (idx, val) {
        $(this).html(idx + 1)
    })
    $("[id^='itemrowid_']").each(function (idx, val) {
        TotAmt = TotAmt + parseFloat($(this).attr('totalAmount'))
    })

    $('#TotAmt').html(parseFloat(TotAmt).toFixed(2))
    $('#subtotamt').html(parseFloat(TotAmt).toFixed(2))
    $('#subTotal').val(parseFloat(TotAmt).toFixed(2))
    calculationnetamt()
}

function calculationnetamt() {
    var TotAmt = $('#subtotamt').text() != '' ? parseFloat($('#subtotamt').html()).toFixed(2) : 0;
    var roundoffamt = Math.round(parseFloat(TotAmt).toFixed(2)) - parseFloat(TotAmt).toFixed(2)
    $('#roundoffamt').html(parseFloat(roundoffamt).toFixed(2))
    var netamount = (Math.round(parseFloat(TotAmt).toFixed(2)))
    $('#netamt').html(parseFloat(netamount).toFixed(2))
    $('#roundOff').val(parseFloat(roundoffamt).toFixed(2))
    $('#netAmount').val(parseFloat(netamount).toFixed(2))
}

function deleteitemrow(rowid) {
    $('#itemrowid_' + rowid).remove()
    setitemtablesno()
}

function edititemrow(rowid) {
    $('#additembtn').attr('row', rowid);
    $('#additembtn').removeClass('btn-primary').addClass('btn-warning');

    var row = $('#itemrowid_' + rowid);
    var categoryId = row.attr('categoryId');

    $('#ddlCategory').val(categoryId).trigger('change');
    $('#txtActualWeight').val(row.attr('actWeight'));
    $('#txtAverageWeight').val(row.attr('avgWeight'));
    $('#totalAmount').val(row.attr('totalAmount'));

}

function submitform() {

    if ($("[id^='itemrowid_']").length == 0) {
        // showmsg(validate_itemadd)
        showMsg('add something')
        return false
    }
    else if (check_validate_forms('#frmPOS') == false) {
        return false
    }
    else {
        pushitemdetail()
        $('#frmPOS').submit()
    }

}
function pushitemdetail() {
    var itemdetaillist = []
    $("[id^='itemrowid_']").each(function (idx, val) {
        var rowid = $(this)
        itemdetaillist.push({
            'categoryId': rowid.attr('categoryId'),
            'categoryName': rowid.attr('categoryName'),
            'actWeight': rowid.attr('actWeight'),
            'avgWeight': rowid.attr('avgWeight'),
            'totalAmount': rowid.attr('totalAmount')
        })
    })
    $('#itemdetail').val(JSON.stringify(itemdetaillist))
}