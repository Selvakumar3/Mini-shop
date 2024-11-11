$(document).ready(function () {
    datatablebind();
});

// Datatable ::
function datatablebind() {
    $("#tblEmployeeTable").DataTable({
        responsive: true,
        autoWidth: false,
        aLengthMenu: [
            [10, 30, 50, -1],
            [10, 30, 50, "All"]
        ],
        columnDefs: [
            {
                className: "dt-body-center",
                targets: [0,1,7,8],
                orderable: false
            }
        ],
        language: {
            search: "_INPUT_", // Removes the 'Search' field label
            searchPlaceholder: "Search", // Placeholder for the search box
            sLengthMenu: "_MENU_",
            sInfo: "_START_ to _END_ of _TOTAL_",
            sInfoEmpty: "0 to 0 of 0",
            sInfoFiltered: "(filtered from _MAX_ total records)"
        },
        iDisplayLength: 10,
        processing: true,
        serverSide: true,
        ajax: {
            url: '/employee/employee-dt/',
            type: 'GET',
            data: function (data) {
                // Additional data can be sent if needed
            }
        },
        columns: [
            {
                data: null,
                width: 20,
                orderable: false,
                render: function (data, type, row, meta) {
                    return meta.row + meta.settings._iDisplayStart + 1;
                }
            },
            {
                data: null,
                class: "text-center",
                render: function (data) {
                    return data ? `<img src="${data.employee_image}" width="100" height="100">` : '-';
                }
            },
            {
                data: null,
                class: "text-left",
                render: function (data) {
                    return (data.first_name != '') ? data.first_name : '-';
                }
            },
            {
                data: null,
                class: "text-left",
                render: function (data) {
                    return (data.employee_no != '') ? data.employee_no : '-';
                }
            },
            {
                data: null,
                class: "text-left",
                render: function (data) {
                    return (data.mobile_number != '') ? data.mobile_number : '-';
                }
            },
            {
                data: null,
                class: "text-left",
                render: function (data) {
                    return (data.doj != '') ? data.doj : '-';
                }
            },
            {
                data: null,
                class: "text-left",
                render: function (data) {
                    return (data.email != '') ? data.email : '-';
                }
            },
            {
                data: null,
                class: "text-center",
                render: function (data) {
                    // Check if is_active is true or 'true' (string)
                    const isActive = data.is_active === true || data.is_active === 'true';

                    return `<div class="form-check form-switch">
                        <input type="checkbox" class="form-check-input ms-4 fs-5" id="chkEmployee${data.employee_id}" ${isActive ? 'checked' : ''} 
                        onclick="doStatus(${data.employee_id})">
                    <label class="custom-control-label pointer" title="Status" for="chkEmployee${data.employee_id}"></label></div>`;
                }
            },
            {
                data: null,
                class: "text-center",
                render: function (data) {
                    return `
                        <td class="text-center">
                            <a class="btn btn-success btn-rounded btn-icon" href="/employee/?employee_id=${data.employee_id}" title="Edit">
                                <i class="ti-pencil-alt" style="font-size: 20px;"></i>
                            </a>
                            <a class="btn btn-danger btn-rounded btn-icon" href='/employee/deleteemployee/?employee_id=${data.employee_id}' onclick="confirmDelete(event, '${data.employee_no}')">
                                <i class="ti-trash"></i>
                            </a>
                    </td>`;
                }
            }
        ],
    });

    // Append elements into the datatable plugin for spacing on top
    $('.dataTables_filter input[type="search"]').css("width", "9rem");
    $(".dataTables_filter").parent().addClass("d-flex justify-content-end");

    $(".dataTables_filter").parent().append(`
    <div class="add-group">
        <a class="btn btn-light ms-3" onClick="location.reload()">
            <img src='${window.location.origin}/static/images/icons/re-fresh.svg' alt="Refresh">
        </a>
    </div>
    <a  class="btn btn-info text-white ms-2" title="Download Excel" onclick="ExporttabletoExcell('tblEmployeeTable','Employee_List',7)"><i class="icon-download"></i> Excel</a>
    <a class="btn btn-danger text-white ms-2" onclick="ExporttabletoPdf('tblEmployeeTable','Employee_List',7)"><i  class="ti-file btn-icon-append"></i> PDF</a>
`);
}

// Binded data in edit action::
function EditRow(product_id) {

    fetch(`/product/edit-product/?product_id=${product_id}`, { method: 'GET' })
        .then(res => res.json())
        .then(data => {

            $('#txtCategoryName').val(data.product_name).focus()
            $('#txtDescription').val(data.category_desc).focus()
            $('#previewImage').attr('src', data.category_image);
            $('#hiddenEdit').val('edit');
            $('#hiddenCategoryId').val(data.categoryid);
            $('#categoryImg').removeAttr('data-validate');
            $('#btnSave').text('Update')
            $('#txtTitle').text('Edit Category')
            window.scrollTo({ top: 0, behavior: 'smooth' });

        }).catch(error => {
            console.error('Error:', error);

        });
}

// Change Category Active Status::
function doStatus(employee_id) {
    var status = $("#chkEmployee" + employee_id).is(":checked");
    confirmStatusChange(employee_id, "/employee/update-employee-status/", "", (status === true ? 1 : 0), "chkEmployee", "employee");
}
