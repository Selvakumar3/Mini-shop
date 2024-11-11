var Rowcount = 0

$(document).ready(function () {
    if (itemdetail_data != '') {
        data_bindingitemtable()

        // Parse the date
        let date = new Date(get_purchase_date);
        let day = String(date.getDate()).padStart(2, '0');
        let month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-indexed
        let year = date.getFullYear();

        let formattedDate = `${day}-${month}-${year}`;
        $('#txtPurchaseDate').val(formattedDate);
        $('#txtPurchaseDate').addClass('input-readonly');
        $('#txtPurchaseDate').attr('readonly', true);


    } else {
        // DatePicker
        var today = new Date();
        $('#txtPurchaseDate', '#datepicker-popup').datepicker({
            format: 'dd/mm/yyyy',
            startDate: '+0d',
            autoclose: true
        }).datepicker('setDate', today);
    }

    // Select2
    $('#ddlProduct').select2({ minimumResultsForSearch: 0 });
    $('#ddlUnit').select2({ minimumResultsForSearch: 0 });
    $('#ddlBillType').select2({ minimumResultsForSearch: 0 });
    $('#ddlBatchNo').select2({ minimumResultsForSearch: 0 });

    // Once ddl change product against data binded in forms
    $('#ddlProduct').change(function (event) {
        if ($(this).val() != '0') {
            var itemid = $('#ddlProduct option:selected')
            $('#MRPAmount').val(itemid.attr('MRP'))
            $('#salesAmount').val(itemid.attr('salesAmount'))
            $('#ddlUnit').val(itemid.attr('unitId')).trigger('change')
            $('#qty').val(1)
            $('#stockDataDisplay').html('')
            calculateitemamount(event)
            var product_id = $('#ddlProduct option:selected').val();
            getBatchNo(product_id);
        } else {
            $('#MRPAmount, #salesAmount, #qty, #totalAmount').val('')
            $('#ddlBatchNo').val('0').trigger('change')
            $('#ddlUnit').val('0').trigger('change')
            $('#stockDataDisplay').html('')
        }
    })

    // Once ddl change product against data binded in forms
    $('#ddlBatchNo').change(function (event) {
        if ($(this).val() != '0') {
            var batch = $('#ddlBatchNo option:selected')
            $('#stockDataDisplay').html(batch.attr('stockQty'))

        } else {
            $('#stockDataDisplay').html('')
        }
    })


});

// CASCADE FOR Product AGAINST Batch ::
function getBatchNo(product_id) {
    return $.ajax({
        url: '/store/get-batch-no/',
        data: { 'product_id': product_id },
        dataType: 'json'
    }).done(function (data) {
        $('#ddlBatchNo').html("<option value='0'>Select Batch</option>");
        $.each(data, function (index, val) {
            $('#ddlBatchNo').append('<option prod_batch_no="' + val.batch_no + '" stockId="' + val.stock_id + '" stockQty="' + val.stock_qty + '" value="' + val.stock_id + '">' + val.batch_no + '</option>');
        });
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.error("Error fetching batch numbers: " + textStatus, errorThrown);
    });
}



// Calculate product amount 
function calculateitemamount(event) {
    var itemId = $('#ddlProduct').val();
    if (itemId == '0') {
        showMsg('Please select any one');
        $('#' + event.target.id).val('');
    } else {
        var qty = $('#qty').val();
        var salesamt = $('#salesAmount').val();

        if (qty === '' || qty === '0') {
            $('#totalAmount').val('');
            if (qty === '0') {
                showMsg('Quantity cannot be zero');
                $('#qty').val(1);
                var TotAmt = (parseFloat(salesamt) * parseFloat($('#qty').val()));
                $('#totalAmount').val(parseFloat(TotAmt).toFixed(2));
            }
        } else {
            var TotAmt = (parseFloat(salesamt) * parseFloat(qty));
            $('#totalAmount').val(parseFloat(TotAmt).toFixed(2));
        }
    }
}


// if ($('#hiddenPurchaseDet').val() != '') {
//     data_bindingitemtable()
// }

function data_bindingitemtable() {
    $('#txtPurTitle').html('Edit Purchase Invoice')
    $('#btnSubmit').html('Update')
    var String_json = decodeHtmlEntities(itemdetail_data)
    if (String_json && String_json.trim() !== '') {
        var itemdetaillist = $.parseJSON(String_json);
        $.each(itemdetaillist, function (idx, val) {
            productId = val.product,
            productName = val.product_name,
            unitId = val.unit,
            unitName = val.unit_name,
            convertionValue = val.convertion_value,
            batchNo = val.batch_no,
            MRPAmount = val.mrp_amount,
            salesAmount = val.sales_amount
            qty = val.qty,
            totalAmount = val.total_amount
            stockId = val.stock

            updateitemtable(0, productId, productName, unitId, unitName, convertionValue, batchNo, MRPAmount, salesAmount, qty, totalAmount, stockId)
        })
    } else {
        console.error("Invalid JSON: ", String_json);
    }
}


// Once Add button click data added in table ::
function itemaddbutton() {
    
    if ($('#ddlProduct').val() == '0') {
        showMsg(validate_itemselect)
        return false
    }
    var fieldsToCheck = $('#MRPAmount, #salesAmount,#qty');
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
    var productId = $('#ddlProduct').val()
    var productName = $('#ddlProduct option:selected').attr('productName')
    var unitId = $('#ddlUnit').val()
    var unitName = $('#ddlUnit option:selected').attr('unitName')
    var convertionValue = $('#ddlUnit option:selected').attr('convertionValue')
    var batchNo = $('#ddlBatchNo option:selected').attr('prod_batch_no')
    var stockId = $('#ddlBatchNo').val()
    var MRPAmount = $('#MRPAmount').val()
    var salesAmount = $('#salesAmount').val()
    var qty = $('#qty').val()
    var totalAmount = $('#totalAmount').val()
    var method = $('#additembtn').attr('row')
    updateitemtable(method, productId, productName, unitId, unitName, convertionValue, batchNo, MRPAmount, salesAmount, qty, totalAmount, stockId)

}

// Data added on table
function updateitemtable(method, productId, productName, unitId, unitName, convertionValue, batchNo, MRPAmount, salesAmount, qty, totalAmount, stockId) {

    // Check for existing rows with the same productId and stockId
    var existingRow = $('#itemtablebody tr').filter(function () {
        return $(this).attr('productId') === productId && $(this).attr('stockId') === stockId;
    });

    if (existingRow.length > 0) {
        showMsg("This product with the batch no already exists in the table.");
        return; // Exit the function if a duplicate is found
    }

    if ($('#emptyitemrow').length != 0) {
        $('#emptyitemrow').remove()
    }
    if (method == 0) {
        Rowcount++
        var bindingtext = ``
        bindingtext += `<tr id="itemrowid_${Rowcount}" rowid="${Rowcount}" productId="${productId}" productName="${productName}" batchNo="${batchNo}" 
                        unitId="${unitId}" unitName="${unitName}" convertionValue="${convertionValue} "MRPAmount="${MRPAmount}" salesAmount="${salesAmount}"  qty="${qty}" 
                        totalAmount="${totalAmount}" stockId="${stockId}">`

        bindingtext += itemtablecontent(Rowcount, productName, unitName, batchNo, MRPAmount, salesAmount, qty, totalAmount, stockId)

        bindingtext += `</tr>`
        $('#itemtablebody').append(bindingtext)
    } else {
        var rowid = $('#itemrowid_' + method)
        rowid.attr('productId', productId)
        rowid.attr('productName', productName)
        rowid.attr('unitId', unitId)
        rowid.attr('unitName', unitName)
        rowid.attr('convertionValue', convertionValue)
        rowid.attr('batchNo', batchNo)
        rowid.attr('MRPAmount', MRPAmount)
        rowid.attr('salesAmount', salesAmount)
        rowid.attr('qty', qty)
        rowid.attr('totalAmount', totalAmount)
        rowid.attr('stockId', stockId)
        rowid.html(itemtablecontent(method, productName, unitName, batchNo, MRPAmount, salesAmount, qty, totalAmount))
    }
    $('#ddlProduct').val('0').trigger('change')
    $('#ddlBatchNo').val('0').trigger('change')
    $('#additembtn').attr('row', '0')
    $('#additembtn').removeClass('btn-warning')
    $('#additembtn').addClass('btn-primary')
    $('.errormsg').html('')
    $('#stockDataDisplay').html('')
    setitemtablesno()
}

function itemtablecontent(Rowcount, productName, unitName, batchNo, MRPAmount, salesAmount, qty, totalAmount) {
    var bindingcontent = ''
    bindingcontent += `<td class="align-middle text-center" id="snoid_${Rowcount}"></td>
    <td class="align-middle text-center">${productName}</td>
    <td class="align-middle text-center">${unitName}</td>
    <td class="align-middle text-center">${batchNo}</td>
    <td class="align-middle text-center">${MRPAmount}</td>
    <td class="align-middle text-center">${salesAmount}</td>
    <td class="align-middle text-center">${qty}</td>
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
                                        <td colspan="14" class="text-center p-2">no product here</td>
                                    </tr>`)
    }

    var totqty = 0
    var TotAmt = 0

    $("[id^='snoid_']").each(function (idx, val) {
        $(this).html(idx + 1)
    })
    $("[id^='itemrowid_']").each(function (idx, val) {

        totqty = totqty + parseFloat($(this).attr('qty'))
        TotAmt = TotAmt + parseFloat($(this).attr('totalAmount'))
    })

    $('#totqty').html(parseFloat(totqty))
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
    $('#txtPurTitle').html('Edit Purchase Invoice');
    $('#additembtn').removeClass('btn-primary').addClass('btn-warning');

    var row = $('#itemrowid_' + rowid);
    var productId = row.attr('productId');

    $('#ddlProduct').val(productId).trigger('change');
    $('#ddlUnit').val(row.attr('unitId')).trigger('change');
    $('#MRPAmount').val(row.attr('MRPAmount'));
    $('#salesAmount').val(row.attr('salesAmount'));
    $('#qty').val(row.attr('qty'));
    $('#totalAmount').val(row.attr('totalAmount'));

    // Load batch numbers based on selected product
    getBatchNo(productId).then(() => {
        var stockId = row.attr('stockId');
        console.log("Setting stock ID:", stockId);

        // Set the selected batch if it exists
        if ($('#ddlBatchNo option[value="' + stockId + '"]').length) {
            $('#ddlBatchNo').val(stockId).trigger('change');
        } else {
            console.warn("Stock ID not found in dropdown options:", stockId);
            $('#ddlBatchNo').val('0').trigger('change'); // Reset if not found
        }
    });
}


function submitform() {

    if ($("[id^='itemrowid_']").length == 0) {
        // showmsg(validate_itemadd)
        showMsg('add something')
        return false
    }
    else if (check_validate_forms('#frmPurchaseInvoice') == false) {
        return false
    }
    else {
        pushitemdetail()
        $('#frmSubPurchase').submit()
    }

}


function pushitemdetail() {
    var itemdetaillist = []
    $("[id^='itemrowid_']").each(function (idx, val) {
        var rowid = $(this)
        itemdetaillist.push({
            'productId': rowid.attr('productId'),
            'productName': rowid.attr('productName'),
            'unitId': rowid.attr('unitId'),
            'unitName': rowid.attr('unitName'),
            'convertionValue': rowid.attr('convertionValue'),
            'batchNo': rowid.attr('batchNo'),
            'MRPAmount': rowid.attr('MRPAmount'),
            'salesAmount': rowid.attr('salesAmount'),
            'qty': rowid.attr('qty'),
            'totalAmount': rowid.attr('totalAmount')
        })
    })
    $('#itemdetail').val(JSON.stringify(itemdetaillist))
}


