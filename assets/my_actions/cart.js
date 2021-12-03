function cartLength(name){
    let cartData = localStorage.getItem(name);
    let jsonData = JSON.parse(cartData);
    return jsonData.length
}

function add_cart(shop_name,product_id,ourQuantity,tag) {
    if(shop_name == null || shop_name=='' || product_id==null || product_id=='' || ourQuantity==null || ourQuantity=='' || tag==null || tag==''){
        console.log("value not valid")
    }else{
        let quantity = parseInt(ourQuantity)
        let cart = localStorage.getItem(shop_name)
        if(cart==null){
            // if cart have no data
            let products = []
            let product = {'product_id':product_id,'quantity':quantity}
            products.push(product)
            localStorage.setItem(shop_name,JSON.stringify(products))
            if(tag=='one'){
                $(".cart-items").html(cartLength(shop_name))
                $(".cart-data").html("")
                cart_items(shop_name,'main-page')
                cart_added_message(product_id,quantity,cartLength(shop_name))
            }else{
                $(".cart-items").html(cartLength(shop_name))
                $(".cart-data").html("")
                cart_items(shop_name,'main-page')
                $("#quick-look").modal("hide")
                cart_added_message(product_id,quantity,cartLength(shop_name))
            }
            // console.log("first "+quantity+" Items added")
        }else{
            // given Shop-Name already exists
            let pcart = JSON.parse(cart)
            let haveAlready = pcart.find(item=>item.product_id==product_id)
            if(haveAlready){
                // given product available
                let qty = parseInt(haveAlready.quantity)+quantity
                haveAlready.quantity=qty
                pcart.map((item=>{
                    if(item.product_id==haveAlready.product_id){
                        item.quantity=haveAlready.quantity
                    }
                }))
                localStorage.setItem(shop_name,JSON.stringify(pcart))
                if(tag=='one'){
                    $(".cart-items").html(cartLength(shop_name))
                    $(".cart-data").html("")
                    cart_items(shop_name,'main-page')
                    cart_added_message(product_id,quantity,cartLength(shop_name))
                }else{
                    $(".cart-items").html(cartLength(shop_name))
                    $(".cart-data").html("")
                    cart_items(shop_name,'main-page')
                    $("#quick-look").modal("hide")
                    cart_added_message(product_id,quantity,cartLength(shop_name))
                }
            }else{
                // given product not available
                let newItem = {'product_id':product_id,'quantity':quantity}
                pcart.push(newItem)
                localStorage.setItem(shop_name,JSON.stringify(pcart))
                if(tag=='one'){
                    $(".cart-items").html(cartLength(shop_name))
                    $(".cart-data").html("")
                    $(".cart-items1").show()
                    cart_items(shop_name,'main-page')
                    cart_added_message(product_id,quantity,cartLength(shop_name))
                }else{
                    $(".cart-items").html(cartLength(shop_name))
                    $(".cart-data").html("")
                    $(".cart-items1").show()
                    cart_items(shop_name,'main-page')
                    $("#quick-look").modal("hide")
                    cart_added_message(product_id,quantity,cartLength(shop_name))
                }
            }
        }
    }
}