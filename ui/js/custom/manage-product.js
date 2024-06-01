var productModal = $("#productModal");

// Function to populate product list
function populateProductList() {
    $.get(productListApiUrl, function (response) {
        if (response) {
            var table = '';
            $.each(response, function (index, product) {
                table += '<tr data-id="' + product.product_id + '" data-name="' + product.name + '" data-unit="' + product.uom_id + '" data-price="' + product.price_per_unit + '">' +
                    '<td>' + product.name + '</td>' +
                    '<td>' + product.uom_name + '</td>' +
                    '<td>' + product.price_per_unit + '</td>' +
                    '<td>' +
                    '<button class="btn btn-xs btn-warning edit-product">Edit</button>&nbsp;&nbsp;&nbsp;' +
                    '<button class="btn btn-xs btn-danger delete-product">Delete</button>' +
                    '</td>' +
                    '</tr>';
            });
            $("table").find('tbody').empty().html(table);
        }
    });
}

// Event handler for edit button click
$(document).on("click", ".edit-product", function (){
    var tr = $(this).closest('tr');
    var productId = tr.data('id');
    var productName = tr.data('name');
    var unitId = tr.data('unit');
    var price = tr.data('price');
    
    // Populate modal with product details
    $("#id").val(productId);
    $("#name").val(productName);
    $("#uoms").val(unitId);
    $("#price").val(price);
    
    // Change modal title
    productModal.find('.modal-title').text('Edit Product');
    
    // Show modal
    productModal.modal('show');
});

// Save Product
$("#saveProduct").on("click", function () {
    // Extract data from form
    var data = $("#productForm").serializeArray();
    var requestPayload = {
        product_id: $("#id").val(), // Include product_id for editing
        product_name: null,
        uom_id: null,
        price_per_unit: null
    };
    for (var i = 0; i < data.length; i++) {
        var element = data[i];
        switch (element.name) {
            case 'name':
                requestPayload.product_name = element.value;
                break;
            case 'uoms':
                requestPayload.uom_id = element.value;
                break;
            case 'price':
                requestPayload.price_per_unit = element.value;
                break;
        }
    }

    // Send AJAX request to save product
    callApi("POST", productSaveApiUrl, {
        'data': JSON.stringify(requestPayload)
    }).done(function (response) {
        // Product saved successfully, update product list
        populateProductList();
    }).fail(function (jqXHR, textStatus, errorThrown) {
        // Handle AJAX error
        console.error('Error saving product:', errorThrown);
    });

    // Close modal after saving
    productModal.modal('hide');
});

$(document).on("click", ".delete-product", function (){
    var tr = $(this).closest('tr');
    var data = {
        product_id : tr.data('id')
    };
    var isDelete = confirm("Are you sure to delete "+ tr.data('name') +" item?");
    if (isDelete) {
        callApi("POST", productDeleteApiUrl, data);
    }
});

// Close Button (Dismiss)
$(".modal-close").on("click", function () {
    // Check if the modal is in "Edit Product" mode
    var modalTitle = productModal.find('.modal-title').text();
    if (modalTitle === 'Edit Product') {
        // Close the modal without clearing form fields or changing the modal title
        productModal.modal('hide');
        return; // Exit the function early, as no further actions are needed
    }
    // Clear form fields and change modal title for "Add New Product" mode
    $("#name, #uoms, #price").val('');
    productModal.find('.modal-title').text('Add New Product');
});


// Event handler for when modal is shown
productModal.on('show.bs.modal', function () {
    // Load available UOM options
    $.get(uomListApiUrl, function (response) {
        if (response) {
            var options = '<option value="">--Select--</option>';
            $.each(response, function (index, uom) {
                options += '<option value="' + uom.uom_id + '">' + uom.uom_name + '</option>';
            });
            $("#uoms").empty().html(options);
        }
    });
});

// Initial load
$(function () {
    // Populate product list
    populateProductList();
});

