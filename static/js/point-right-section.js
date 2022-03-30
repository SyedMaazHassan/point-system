var BUSINESS_ID = null;
var is_value = false;
var BUSINESS_TOTAL = null;

setTimeout(() => {
    $("#dashboard-link").removeClass("active");
}, 100);

function get_customer_list(business_id) {
    $("#points_to_be_given").val("");
    $("#at-most-fb").removeClass("text-danger");

    BUSINESS_ID = business_id;
    // MARK AS SELECTED
    $(".business_containers").removeClass("selected-business");
    $(`#business_container_${business_id}`).addClass("selected-business");

    $.ajax({
        url: GET_CUSTOMER_LIST_URL,
        type: "GET",
        data: `business_id=${business_id}`,
        success: (response)=>{
            // SET value in holder
            console.log(response);
            if (response) {          
                BUSINESS_TOTAL = response.total;

                if (BUSINESS_TOTAL > 0) {
                    $("#send-section").show();
                }else{
                    $("#send-section").hide();
                }


                $("#image_holder").attr("src", "media/"+response.image);
                $("#title_holder").text(response.business_name);
                $("#total_holder").text(response.total);
                $("#point-needed").text(response.total);
                $("#table_body").children().remove();
                for (let i = 0; i < response.customer_list.length; i++) {
                    let customer = response.customer_list[i];
                    $("#table_body").append(`
                        <tr>
                            <td class="px-3">${ customer.name }</td>
                            <td>${ customer.total_points_owe }</td>
                        </tr>
                    
                    `);
                }

                if (response.customer_list.length == 0) {
                    $("#table_body").append(`
                        <tr>
                            <td class="px-3 pt-3" colspan="2">
                                <div class="alert text-center alert-warning" role="alert">
                                    No customer yet!
                                </div>    
                            </td>
                        </tr>
                    
                    `);
                }

                // show right panel
                $("#right-panel").show();

                // make left panel small
                $("#left-panel").removeClass("col-sm-12");
                $("#left-panel").addClass("col-sm-8");

                // Scroll up
                $('html, body').animate({
                    scrollTop: $('#business-section').offset().top
                }, 200);
            }else{
                BUSINESS_TOTAL = null;
            }
        }
    })
}

function close_right_panel() {
    $(".business_containers").removeClass("selected-business");
    $("#left-panel").addClass("col-sm-12");
    $("#left-panel").removeClass("col-sm-8");
    $("#right-panel").hide();
}

function send_points() {
    if (is_value) {
        $("#success-msg").hide();
        $("#error-msg").hide();
        $("#loading-spinner").show();
        let value = $("#points_to_be_given").val();
        $.ajax({
            url: SEND_POINT_URL,
            type: "GET",
            data: {
                'business_id': BUSINESS_ID,
                'value': value
            },
            success: (response)=>{
                $("#loading-spinner").hide();
                if (response.status == true) {
                    $("#success-msg").show();
                    $("#error-msg").hide();
                    $("#error-2-msg").hide();
                    $("#points_to_be_given").val("");
                    $(".admin_total_balance").text(response.admin_account_info.total_balance); 
                    get_customer_list(BUSINESS_ID);
                }else{
                    $("#success-msg").hide();
                    $("#error-msg").show();
                }
                console.log(response);
            }
        })
    }
}


$("#points_to_be_given").on("input", function () {
    let value = this.value;
    let admin_account_balance = '{{ admin_account_info.total_balance }}';
    if (value && value > 0) {
        if (parseFloat(value) <= parseFloat(admin_account_balance)) {
            
            if (BUSINESS_TOTAL && (parseFloat(value) <= parseFloat(BUSINESS_TOTAL))) {
                is_value = true;
                $("#error-2-msg").hide();
                $("#at-most-fb").removeClass("text-danger");
                return;   
            }else{
                $("#error-2-msg").show();
            }
               
        }else{
            $("#at-most-fb").addClass("text-danger");
        }
    }
    is_value = false;
});



if (default_business) {
    get_customer_list(default_business);
}

