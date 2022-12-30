$('.plus-cart').click(function () {
    
    let id = $(this).attr("pid").toString();
    console.log(id)

    let eml = this.parentNode.children[2];
    
    
    $.ajax(
        {
            type: "GET",
            url: "/pluscart",
            data: {
                prod_id: id
            },
            success: function (data) {
                console.log(data.quantity);
                console.log("success")
                eml.innerText = data.quantity;
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
            }
        })
});
$('.minus-cart').click(function () {
    
    let id = $(this).attr("pid").toString();
    console.log(id)

    let eml = this.parentNode.children[2];
    
    
    $.ajax(
        {
            type: "GET",
            url: "/minuscart",
            data: {
                prod_id: id
            },
            success: function (data) {
                console.log(data.quantity);
                console.log("success")
                eml.innerText = data.quantity;
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
            }
        })
});
$('.remove-cart').click(function () {
    
    let id = $(this).attr("pid").toString();
    console.log(id)

    let elm = this;
    
    
    $.ajax(
        {
            type: "GET",
            url: "/removecart",
            data: {
                prod_id: id
            },
            success: function (data) {
               
                console.log("success")
               
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
                elm.parentNode.parentNode.parentNode.parentNode.remove();
            }
        })
});