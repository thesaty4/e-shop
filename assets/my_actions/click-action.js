function change_my_profile(){
    $("#profile_pic_help_text").html("&#8593; Please select your profile from here..")
}

// AUTO LOAD ----------------------
function default_profile_data(gender,country){
    $("#reg-gender").val(gender);
    $("#reg-country").val(country)
}
// AUTO LOAD ----------------------

defaultAddress = 0
currentUser = 0
function makeDefaultAddress(addressId,user){
    defaultAddress = addressId
    currentUser = user
}

$("#default-shipping-address").on("submit",function(e){
    e.preventDefault()
    if(defaultAddress == 0 && currentUser == 0){
        $('#address-response-message').html("<span class='error blink_me'>Please select new address.</span>")
    }else{
        $('#address-response-message').html("")
        $.ajax({
            method:'post',
            url:'/dashboard/dashAddMakeDefault/',
            data:{
                'addressId':defaultAddress.trim(),
                'userId':currentUser.trim(),
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val().trim()
            },
            success:function(response){
                if(response == 'valid'){
                    if(confirm("Default Shipping address has been changed !"))
                    window.location.href='/dashboard/dashAddMakeDefault/'
                    else window.location.href='/dashboard/dashAddMakeDefault/'
                }else{
                    alert("Opps ! Somthing wen't wrong")
                }
            },error:function(response){
                // window.location.href="/dashboard/dashAddMakeDefault/"
                alert("Opps ! an error occured")
            }
        })
    }
})

function select_default_country(country){
    $("#id_country").val(country)
}
function select_default_state(state){
    $("#id_state").val(state)
}
function insert_full_address(address){
    $("#id_full_address").html(address)
}

function delete_address(id){
    if(confirm("Do you want to delete?")){
        $("#"+id).hide()
        $.ajax({
            method:'POST',
            url:"/dashboard/delete-address/",
            data:{
                'addressId':id,
                'userId':loggedUser,
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
            },
            success:function(r){console.log("Deleted")},
            error:function(r){console.log("Error")}
        })
    }
}

// CHANING DROPDOWN MENU
$("#id_category").on("change",function(e) {
    e.preventDefault()
    let category = $(this).val()
    $.ajax({
        method:'GET',
        url:'/selling_product/get-dropdown/',
        data:{'id':category,'type':'subcategory',csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()},
        success:function(response){
            $("#id_subcategory").html(response)
        }
    })

    $.ajax({
        method:'GET',
        url:'/selling_product/get-dropdown/',
        data:{'id':category,'type':'brand',csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()},
        success:function(response){
            $("#id_brand").html(response)
        }
    })
})

$('#messageExit').on('click',function(){
    $("#message").hide()
})
function messageDismiss() {
    setTimeout(function(){
        $("#message").hide()
    },3000)
}

// product image delete
function delete_my_image(params,productId) {
    if(confirm("Do you want to delete?")){
        $("#"+params).hide()
        $.ajax({
            method:'POST',
            url:'/selling_product/delete-product-images/',
            data:{
                'image-id':params,
                'product-id':productId,
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
            },
            success:function(){
                console.log("deleted")
            },error:function () {
                console.log("not deleted")
            }
        })
    }
}

// PRODUCT DELTEING PROCESS
function  delete_product(product_id) {
    if(confirm("Do you want to delete product?")){
        $("#"+product_id).hide()
        $.ajax({
            method:'POST',
            url:'/selling_product/delete-entire-product/',
            data:{
                'product-id':product_id,
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
            },
            success:function(params) {
                console.log("Product Delete")
            },error:function(params) {
                alert("Opps ! Product Deleting problem raise..")
            }
        })
    }
}

// quick view
function quick_view(shop,pid) {
    $.ajax({
        method:"GET",
        url:"/selling_product/get-one-product/",
        data:{
            'product-id':pid,
            'shop':shop,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function (data) {
            $("#id-quick-look-modal").html(data)
            $("#quick-look").modal("show")
            // console.log("data set")
        },error:function (params) {
            console.log("data seting error")
            
        }
    })
}
// cart added
function cart_added_message(pid,quantity,total_item) {
    $.ajax({
        method:"GET",
        url:"/selling_product/get-cart-product/",
        data:{
            'product-id':pid,
            'quantity':quantity,
            'total-item':total_item,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function (data) {
            $("#id-cart-modal").html(data)
            $("#add-to-cart").modal("show")
            console.log("data set")
        },error:function (params) {
            console.log("data seting error")
        }
    })
}

function increase_decrease__item(shop,product_id,quantity){
    let qty = 0.0
    let cart = localStorage.getItem(shop)
    let pcart = JSON.parse(cart)
    let haveAlready = pcart.find(item=>item.product_id==product_id)
    haveAlready.quantity=quantity
    pcart.map((item=>{
        if(item.product_id==haveAlready.product_id){
            item.quantity=haveAlready.quantity
        }
    }))
    localStorage.clear()
    localStorage.setItem(shop,JSON.stringify(pcart))
    $(".cart-data").html("")
    cart_items(shop,'main-page')
}

// PACKAGE FOR CONVERT DATA INTO COMMAN
class NumberConvertIntoComman{

    reverse(data){
        let newData=''
        for(let i=0,j=data.length-1;i<data.length;i++,j--){
            newData+=data[j]
        }
        return newData
    }

    reverse_comma_data(arg){
        let lastCommaRemovedData=''
        let reverseData=''
        if(arg[arg.length-1]==','){
            for(var j=0;j<arg.length-1;j++){
                lastCommaRemovedData+=arg[j]
            }
            reverseData = this.reverse(lastCommaRemovedData)
        }else{
            reverseData = this.reverse(arg)
        }
        return reverseData
    }
    
    sliceData(data,start,end){
        let newData=''
        for(var i=start;i<=end;i++){
            newData+=data[i]
        }
        return newData
    }

    convert_data_into_comma(arg){
        let data=arg.toString()
        let splited=data.split(".")
        data=splited[0]
        let rev_data = this.reverse(data)
        let data_length = data.length
        let counter=1
        let begining=0
        let end=0
        let position=0
        let changedData=''
        for(let i=0;i<data_length;i++){
            if(counter%3==0){
                changedData+=this.sliceData(rev_data,begining,end)
                changedData+=","
                position+=3
            }
            counter+=1
            begining=position
            end+=1
            if(counter==data_length && counter%3 != 0){
                changedData+=this.sliceData(rev_data,begining,end)
            }
        }
        return this.reverse_comma_data(changedData.toString())+"."+data[1]
    }
}


// VALUE INCREASE DECREASE

function value_minus(shop,tag,id,actualPrice){
    let val = $("#product_quantity-"+id).val()
    if(val>1){
    val = parseInt(val) - 1
    let price = parseFloat(actualPrice)*val
    obj = new NumberConvertIntoComman()
    $("#product_quantity-"+id).val(val)
    $("#cart-product-total-price-"+id).html(obj.convert_data_into_comma(price))
    increase_decrease__item(shop,id,val)
}
}
function value_plus(shop,tag,id,actualPrice){
    let val = $("#product_quantity-"+id).val()
    val = parseInt(val) + 1
    let price = parseFloat(actualPrice)*val
    obj = new NumberConvertIntoComman()
    $("#product_quantity-"+id).val(val)
    $("#cart-product-total-price-"+id).html(obj.convert_data_into_comma(price))
    increase_decrease__item(shop,id,val)
}

function cart_length(name){
    let cartData = localStorage.getItem(name);
    let jsonData = JSON.parse(cartData);
    return jsonData.length
}

// cart items setting
function get_cart_items(name){
    let cartData = localStorage.getItem(name);
    if(cartData == null || JSON.parse(cartData).length == 0){
        $(".cart-items").hide()
        $(".cart-items-data").html('<a class="mini-link btn--e-brand-b-2">No Cart Found !</a>')
        $(".cart-items-data2").hide()
    }else{
        let len = cart_length(name)
        $(".cart-items").html(len)
    }
}


function cart_items(shop_name,from) {
    let cartItem = localStorage.getItem(shop_name);
    if(cartItem != null){
        let jsonCartItem = JSON.parse(cartItem)
        jsonCartItem.map((item=>{
            $.ajax({
                method:'GET',
                url:'/selling_product/get-products/',
                data:{
                    'product-id':item.product_id,
                    'quantity':item.quantity,
                    'from':from,
                    csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
                },success:function(response){
                    if(from == 'cart-page'){
                        $(".cart-page-data").append(response)
                    }else{
                        $(".cart-data").append(response)
                    }
                },error:function(response){
                    // $(".cart-data").html(response)
                    console.log("data seting problem...")
                }
            })
        }))
    }
}

// REMOVING ITEMS FROM CART
function remove_cart_item(shop,item_id){
    console.log(shop,item_id)
    $(".cart-id-"+item_id).hide()
    let cartData = localStorage.getItem(shop)
    let jsonCartData = JSON.parse(cartData)
    let newData = []
    let counter = 0
    if(jsonCartData.find(item=>item.product_id==item_id)){
        jsonCartData.map((item=>{
            if(item.product_id!=item_id){
                newData.push(item)
                counter+=1
            }
        }))
    }
    localStorage.clear()
    localStorage.setItem(shop,JSON.stringify(newData))
    if(cart_length(shop)<1){
        $(".cart-items").hide()
        $(".cart-items-data").html('<a class="mini-link btn--e-brand-b-2">No Cart Found !</a>')
        $(".cart-items-data2").hide()
    }else{
        $(".cart-items").html(counter)
    }

}


// REMOVE ALL PRODUCT FROM CART 
function remove_all_cart(shop){
    localStorage.clear()
    window.location.href='/cart/'
}

// CHECKING DATA AVAILABLE IN THE CART ?
function is_null_cart(shop_name){
    let data = localStorage.getItem(shop_name)
    if(data == null || JSON.parse(data).length == 0){
        let emptyCart = `
        <!--====== Section 1 ======-->
        <div class="u-s-p-y-60">

            <!--====== Section Content ======-->
            <div class="section__content">
                <div class="container">
                    <div class="row">
                        <div class="col-lg-12 col-md-12 u-s-m-b-30">
                            <div class="empty">
                                <div class="empty__wrap">

                                    <span class="empty__big-text">EMPTY</span>

                                    <span class="empty__text-1">No items found on your cart.</span>

                                    <a class="empty__redirect-link btn--e-brand"
                                        href="/shop">CONTINUE SHOPPING</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!--====== End - Section Content ======-->
        </div>
        <!--====== End - Section 1 ======-->

        `;
        $("#cart-item-wrapper").html(emptyCart)
    }
}


// ADD MY WISHLIST INTO DATABASE
function add__wishlist(user_id,product_id,status){
    // console.log("i'm working")
    $.ajax({
        method:'POST',
        url:'/selling_product/add-my-wishlist/',
        data:{
            'user':user_id,
            'product':product_id,
            'status':status,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        }
        // ,success:function(res){
        //     // console.log(set)
        //     console.log(res)
        // },error:function(re){
        //     console.log(re)
        // }
    })
}

// WISHLIST ACTION
function wishlist_check__action(user_id,product_id){
    let checkbox = $("input[id='wishlist-checkbox-"+product_id+"']:checked").val()
    if(checkbox == undefined){
        // console.log("on")
        $("#wishlist-enable__disable-"+product_id).html("<i class='fas fa-heart'></i>")
        $(".wishlist-enable__disable-"+product_id).html("<i class='fas fa-heart'></i>")
        add__wishlist(user_id,product_id,true)
    }else{
        // console.log("off")
        $("#wishlist-enable__disable-"+product_id).html("<i class='far fa-heart'></i>")
        $(".wishlist-enable__disable-"+product_id).html("<i class='far fa-heart'></i>")
        add__wishlist(user_id,product_id,false)
    }
}
function dod_wishlist_check__action(user_id,product_id){
    let checkbox = $("input[id='wishlist-dod-checkbox-"+product_id+"']:checked").val()
    if(checkbox == undefined){
        // console.log("on")
        $(".wishlist-dod-enable__disable-"+product_id).html("<i class='fas fa-heart'></i>")
        add__wishlist(user_id,product_id,true)
    }else{
        // console.log("off")
        $(".wishlist-dod-enable__disable-"+product_id).html("<i class='far fa-heart'></i>")
        add__wishlist(user_id,product_id,false)
    }
}

function fp_wishlist_check__action(user_id,product_id){
    let checkbox = $("input[id='wishlist-fp-checkbox-"+product_id+"']:checked").val()
    if(checkbox == undefined){
        // console.log("on")
        $(".wishlist-fp-enable__disable-"+product_id).html("<i class='fas fa-heart'></i>")
        add__wishlist(user_id,product_id,true)
    }else{
        // console.log("off")
        $(".wishlist-fp-enable__disable-"+product_id).html("<i class='far fa-heart'></i>")
        add__wishlist(user_id,product_id,false)
    }
}

// WISH LIST CLEAR
function clear__wishlist(userid){
    $.ajax({
        method:'POST',
        url:'/selling_product/clear-my-wishlist/',
        data:{
            'user_id':userid,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(){
            window.location.href='/wishlist/'
        }
    })
}

// REMOVE WISHLIST ITEM
function remove_wishlist(wishlist_id){
    $("#id-wishlist-item-"+wishlist_id).hide()
    $.ajax({
        method:'POST',
        url:'/selling_product/remove-wishlist-item/',
        data:{
            'wishlist-id':wishlist_id,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        }
    })
}

// UNSUBSCRIBING PRODUCT
function product_subscribe__action(user_id,product_id){
    let checkbox = $("input[id='product-subscribe-checkbox-"+product_id+"']:checked").val()
    if(checkbox == undefined){
        // console.log("on")
        $("#product-subscribe-enable__disable-"+product_id).html("<i class='fas fa-envelope'></i>")
        $(".product-subscribe-enable__disable-"+product_id).html("<i class='fas fa-envelope'></i>")
        add__subscriber(user_id,product_id,true)
    }else{
        // console.log("off")
        $("#product-subscribe-enable__disable-"+product_id).html("<i class='far fa-envelope'></i>")
        $(".product-subscribe-enable__disable-"+product_id).html("<i class='far fa-envelope'></i>")
        add__subscriber(user_id,product_id,false)
    }
}
function dod_product_subscribe__action(user_id,product_id){
    let checkbox = $("input[id='product-dod-subscribe-checkbox-"+product_id+"']:checked").val()
    if(checkbox == undefined){
        // console.log("on")
        $(".product-dod-subscribe-enable__disable-"+product_id).html("<i class='fas fa-envelope'></i>")
        add__subscriber(user_id,product_id,true)
    }else{
        // console.log("off")
        $(".product-dod-subscribe-enable__disable-"+product_id).html("<i class='far fa-envelope'></i>")
        add__subscriber(user_id,product_id,false)
    }
}
function fp_product_subscribe__action(user_id,product_id){
    let checkbox = $("input[id='product-fp-subscribe-checkbox-"+product_id+"']:checked").val()
    if(checkbox == undefined){
        // console.log("on")
        $(".product-fp-subscribe-enable__disable-"+product_id).html("<i class='fas fa-envelope'></i>")
        add__subscriber(user_id,product_id,true)
    }else{
        // console.log("off")
        $(".product-fp-subscribe-enable__disable-"+product_id).html("<i class='far fa-envelope'></i>")
        add__subscriber(user_id,product_id,false)
    }
}

// TAG REMOVEING
function remove_my_tag(tag_id,tag,pid,uid){
    $("#id-tag-"+tag_id).hide()
    $.ajax({
        method:'POST',
        url:'/remove-my-tag/',
        data:{
            'tag':tag,
            'pid':pid,
            'uid':uid,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        }
    })
}

// ADD MY TAG
function add_new_tag(pid,uid){
    let new_tags = $("#add-new-tag").val().split(",")
    let tags = $("#add-new-tag").val()
    for(i=0;i<new_tags.length;i++){
        if(new_tags[i] != ''){
            let tag_html=`
                    <div class="tags input-counter">
                        <input type="text" class="input-counter__text input-counter--text-primary-style" value="`+new_tags[i]+`" style="padding-left: 20px; padding-right: 33px" style='padding-left: 15px;padding-right:15px;'>
                        
                        <a class="input-counter__plus fas fa-trash" style="color: red;" href='/productDetails/`+pid+`?#pd-tag'></a>
                       
                    </div>`
            $("#tag-wrapper").append(tag_html)
        }
    }
    $.ajax({
        method:'POST',
        url:'/add-new-tag/',
        data:{
            'uid':uid,
            'pid':pid,
            'new-tag':tags,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        }

    })
}

function auto_fill_rating_star(rate){
    if(rate==1){
        fill_rating_star('review-star-1')
    }else if(rate==2){
        fill_rating_star('review-star-2')
    }else if(rate==3){
        fill_rating_star('review-star-3')
    }else if(rate==4){
        fill_rating_star('review-star-4')
    }else if(rate==5){
        fill_rating_star('review-star-5')
    }
}
// RATING STAR 
function fill_rating_star(star_id){
    // rating = 0
    if(star_id == 'review-star-1'){ 
        $("#review-star-1").html("<i class='fas fa-star'></i>")

        $("#review-star-2").html("<i class='far fa-star'></i>")
        $("#review-star-3").html("<i class='far fa-star'></i>")
        $("#review-star-4").html("<i class='far fa-star'></i>")
        $("#review-star-5").html("<i class='far fa-star'></i>")        
        // rating = 1
    } else if(star_id == 'review-star-2'){ 
        $("#review-star-1").html("<i class='fas fa-star'></i>")
        $("#review-star-2").html("<i class='fas fa-star'></i>")

        $("#review-star-3").html("<i class='far fa-star'></i>")
        $("#review-star-4").html("<i class='far fa-star'></i>")
        $("#review-star-5").html("<i class='far fa-star'></i>")
        // rating = 2
    }else if(star_id == 'review-star-3'){ 
        $("#review-star-1").html("<i class='fas fa-star'></i>")
        $("#review-star-2").html("<i class='fas fa-star'></i>")
        $("#review-star-3").html("<i class='fas fa-star'></i>")

        $("#review-star-4").html("<i class='far fa-star'></i>")
        $("#review-star-5").html("<i class='far fa-star'></i>")
        // rating = 3
    }else if(star_id == 'review-star-4'){ 
        $("#review-star-1").html("<i class='fas fa-star'></i>")
        $("#review-star-2").html("<i class='fas fa-star'></i>")
        $("#review-star-3").html("<i class='fas fa-star'></i>")
        $("#review-star-4").html("<i class='fas fa-star'></i>")
    
        $("#review-star-5").html("<i class='far fa-star'></i>")
        // rating = 4
    }else if(star_id == 'review-star-5'){ 
        $("#review-star-1").html("<i class='fas fa-star'></i>")
        $("#review-star-2").html("<i class='fas fa-star'></i>")
        $("#review-star-3").html("<i class='fas fa-star'></i>")
        $("#review-star-4").html("<i class='fas fa-star'></i>")
        $("#review-star-5").html("<i class='fas fa-star'></i>")
        // rating = 5
    }
    // console.log("your rating is -> "+rating)

    // else if(star_id == 'rating-star-3'){}
    // else if(star_id == 'rating-star-4'){}
    // else if(star_id == 'rating-star-5'){}
}


function review_field_validate(){
    let val = $("input[name=rating]:checked").val()
    if(val == undefined){
        $("#rating-response").html("<span class='error blink_me'>Please select your rating.</span>")
        return false
    }else{
        let review_text = $("#reviewer-text").val()
        if(review_text == '' || review_text == null){
            $("#rating-text-response").html("<span class='error blink_me'>Required Field, Please write your review.</span>")
            return false
        }else{
            return true
        }
    }
}


function action_on_review(review_id,uid,pid,action){
    if(action=='edit'){
        let validated = review_field_validate()
        if(validated==true){
            let review_text = $("#reviewer-text").val().trim()
            let rate = $("input[name=rating]:checked").val()
            $.ajax({
                method:'POST',
                url:'/update-review/',
                data:{
                    'rating':rate,
                    'user-id':uid,
                    'product-id':pid,
                    'review-text':review_text,
                    csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
                },success:function(){
                    alert("Rating Updated...")
                }
            })
        }
    }else if(action == 'delete'){
        if(confirm("Do you want to remove your review?")){
            $("#id-reviews-wrapper-"+review_id).hide()
            // delete review
            $.ajax({
                method:'POST',
                url:'/remove-review/',
                data:{
                    'review_id':review_id,
                    'uid':uid,
                    'pid':pid,
                    csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
                }
            })
        }
    }
}

// ADDING NEW REVIEW VOTE IN DATABASE
function review_vote(r_id,p_id,u_id,tag,action){
    $.ajax({
        method:'POST',
        url:'/vote-for-review/',
        data:{
            'review-id':r_id,
            'product-id':p_id,
            'user-id':u_id,
            'tag':tag,
            'action':action,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(vote){
            // vote=vote.split("-")
            if(vote!='invalid-user'){
                let server_response = vote.split("-")
                $("#id-review-up_vote-count-"+r_id).html(server_response[0])
                $("#id-review-down_vote-count-"+r_id).html(server_response[1])
                // console.log(vote)
                // console.log(server_response)
            }
        }
    })
}

// VOTING MANAGEMENT 
function action_for_voting(r_id,p_id,u_id,tag){
    // console.log(r_id)
    // console.log(p_id)
    // console.log(u_id)
    // console.log(tag)
    if(tag=='up-vote'){
        let up_is_checked = $("input[name=product-review-up_vote-"+r_id+"]:checked").val()
        if(up_is_checked==undefined){
            // console.log("add into up vote")
            // ONCLICK VOTING NUMBER CHANGE
            
            // ONCLICK VOTING ICON
            $("#id-review-up_vote-"+r_id).html('<i class="fas fa-arrow-alt-circle-up" style="color:rgb(38, 110, 243);;"></i>')

            $("input[name=product-review-down_vote-"+r_id+"]").remove()
            $("#id-review-down_vote-checkbox-"+r_id).html(`<input type="checkbox" name="product-review-down_vote-`+r_id+`" id="id-review-down_vote-input-`+r_id+`" value='down vote' hidden>`)
            $("#id-review-down_vote-"+r_id).html('<i class="far fa-arrow-alt-circle-down"></i>')
            
            // SENDING DATA FOR SERVER, NOW SERVER WILL RESPONDING TWO VALUE UPVOTE,DOWNVOTE
            review_vote(r_id,p_id,u_id,'upvote','add')

        }else{
            $("#id-review-up_vote-"+r_id).html('<i class="far fa-arrow-alt-circle-up"></i>')
            // SENDING DATA FOR SERVER, NOW SERVER WILL RESPONDING TWO VALUE UPVOTE,DOWNVOTE
            review_vote(r_id,p_id,u_id,'upvote','remove')
        }
        
    }else if(tag=='down-vote'){
        let down_is_checked = $("input[name=product-review-down_vote-"+r_id+"]:checked").val()
        if(down_is_checked==undefined){
            $("#id-review-down_vote-"+r_id).html('<i class="fas fa-arrow-alt-circle-down" style="color:rgb(38, 110, 243);;"></i>')
            
            $("input[name=product-review-up_vote-"+r_id+"]").remove()
            $("#id-review-up_vote-checkbox-"+r_id).html(`<input type="checkbox" name="product-review-up_vote-`+r_id+`" id="id-review-up_vote-input-`+r_id+`" value='up vote' hidden>`)
            $("#id-review-up_vote-"+r_id).html('<i class="far fa-arrow-alt-circle-up"></i>')

            // SENDING DATA FOR SERVER, NOW SERVER WILL RESPONDING TWO VALUE UPVOTE,DOWNVOTE
            review_vote(r_id,p_id,u_id,'downvote','add')
        }else{
            $("#id-review-down_vote-"+r_id).html('<i class="far fa-arrow-alt-circle-down"></i>')
            
            // SENDING DATA FOR SERVER, NOW SERVER WILL RESPONDING TWO VALUE UPVOTE,DOWNVOTE
            review_vote(r_id,p_id,u_id,'downvote','remove')
        }
        
    }
}


start_limit=0
end_limit=5
review_sorted_by=''
// REVIEW SORTING
function sort_review(sortBy,uid,pid){
    $("#load-more-review-btn").show()
    review_sorted_by=sortBy
    start_limit=0
    end_limit=5
    $.ajax({
        method:'POST',
        url:'/sort-review/',
        data:{
            'sort-by':sortBy,
            'uid':uid,
            'pid':pid,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success(data){
            // console.log(data)
            $("#review-data-container").html(data)
        }
    })
}

// LOAD MORE REVIEW BUTTON ACTION
function fetch_more_review(pid,uid){

    // e.preventDefault()
    let total_review = parseInt($("#total-review-value").val())
    start_limit+=5
    end_limit+=5
    $.ajax({
        method:'GET',
        url:'/fetch-more-review/',
        data:{
            'uid':uid,
            'pid':pid,
            'start':start_limit,
            'end':end_limit,
            'is-sorted-data':review_sorted_by,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(response){
            if(end_limit>total_review){
                $("#load-more-review-btn").hide()
            }
            $("#review-data-container").append(response)
        }
    })
}

// NEW ARRIVAL PRODUCT 
function get_more_new_arrival_product(){
    window.location.href='/shop/'
}

// NEW ARRIVAL PRODUCT PAGINATION

$('#pagination-btn_left').on('click',function(e){
    // console.log("you clicke left btn")
    // const btn_left=document.getElementById('pagination-btn_left'),
    const pagination_content = document.getElementById('pagination-content')
    console.log(pagination_content)
    let content_scroll_left=pagination_content.scrollLeft
    console.log(content_scroll_left)

    content_scroll_left-=100
    if(content_scroll_left<=0){
        content_scroll_left=0
    }
    pagination_content.scrollLeft=content_scroll_left
})
$('#pagination-btn_right').on('click',function(e){
    // console.log("you clicke right btn")

    // const btn_left=document.getElementById('pagination-btn_left'),
    const pagination_content = document.getElementById('pagination-content')
    let content_scroll_left=pagination_content.scrollLeft
    const content_scroll_width = pagination_content.scrollWidth
    content_scroll_left+=100
    if(content_scroll_left>=content_scroll_width){
        content_scroll_left=content_scroll_width
    }
    pagination_content.scrollLeft=content_scroll_left
})

var new_arrival_items= {
    'slice_start':0,
    'slice_end':0,
    'previous_page':0,
    'order_by':'-id',
    'user':'',
    'shop_name':'',
    'page_length':0,
    'total_item_show':0,
    'total_items':0,
    'query':''
}
function set_default_items(shop_name,user,total_items){
    new_arrival_items.slice_start=0
    new_arrival_items.slice_end=9
    new_arrival_items.previous_page=1
    new_arrival_items.order_by='-id'
    new_arrival_items.total_item_show=9
    new_arrival_items.user=user
    new_arrival_items.shop_name=shop_name
    new_arrival_items.total_items=total_items
    let query=$("#main-search").val().trim()
    new_arrival_items.query=query
    setPagination()
    $("#page-1").attr('class','is-active')
}
function setPagination(){
    let html=``
    for(let i=1;i<=Math.ceil(new_arrival_items.total_items/new_arrival_items.total_item_show);i++){
        html+='<li id="page-'+i+'">'
            +'<a onclick="_get_new_arrival('+i+')">'+i+'</a></li>'
        +'<li>'
    }
    $("#pagination-content").html(html)
    $("#page-"+new_arrival_items.previous_page).attr('class','is-active')
}

function request_for_items(){
    $.ajax({
        method:'POST',
        url:'/more-new-arrival-product/',
        data:{
            'start':new_arrival_items.slice_start,
            'end':new_arrival_items.slice_end,
            'shop-name':new_arrival_items.shop_name,
            'order-by':new_arrival_items.order_by,
            'is-user':new_arrival_items.user,
            'query':new_arrival_items.query,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(response){
            $("#new-arrival-product-wrapper").html(response)
            $(".item-loader-top").attr('style','display:none;')
            $(".item-loader-bottom").attr('style','display:none;')
            setPagination()
            // $("#new-arrival-product-wrapper").append(response)
        }

    })
}

function _get_new_arrival(page){
    new_arrival_items.slice_end=(page*new_arrival_items.total_item_show)
    new_arrival_items.slice_start=(page*new_arrival_items.total_item_show)-new_arrival_items.total_item_show
    new_arrival_items.previous_page=page
    setPagination()
    $("#page-"+new_arrival_items.previous_page).attr('class','is-active')
    $(".item-loader-bottom").attr('style','display:block;')
    request_for_items()
    
}

function fetch_items_quantity(qty){
    $(".item-loader-top").attr('style','display:block;')
    new_arrival_items.slice_start=0
    new_arrival_items.slice_end=qty
    new_arrival_items.total_item_show=qty
    setPagination()
    $("#page-1").attr('class','is-active')
    $.ajax({
        method:'POST',
        url:'/more-new-arrival-product/',
        data:{
            'start':0,
            'end':qty,
            'shop-name':new_arrival_items.shop_name,
            'order-by':new_arrival_items.order_by,
            'is-user':new_arrival_items.user,
            'query':new_arrival_items.query,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(response){
            $(".item-loader-top").attr('style','display:none;')
            $("#new-arrival-product-wrapper").html(response)
            // $("#new-arrival-product-wrapper").append(response)
        }
    })
}

function get_item_order_by(order_by){
    setPagination()
    $("#page-1").attr('class','is-active')
    $(".item-loader-top").attr('style','display:block;')
    new_arrival_items.order_by=order_by
    request_for_items()
}

$("#main-search-item").on("submit",function(e){
    let query=$("#main-search").val().trim()
    if(query==''||query==null){
        // console.log("empty")
        window.location.href="/emptySearch/"
        return false
    }else{
        return true
        // e.preventDefault()
        // // console.log("you requested somthing")
        // // console.log($("#main-search").val())
        
        // new_arrival_items.query=query
        // request_for_items()
        // $("#pagination-content").hide()
        // $("#pagination-btn_left").hide()
        // $("#pagination-btn_right").hide()
    }
})

function set_default_query(query,number_of_product){
    new_arrival_items.query=query
    new_arrival_items.total_items=number_of_product
    new_arrival_items.start=0
    setPagination()
    $("#page-1").attr('class','is-active')
    // console.log(query)
}

$("#id_is_offer").on("change",function(e){
    let val=$("#id_is_offer").val()
    if(val=='NO' || val==''){
        $("#id_offer_end").attr('disabled','')
        $("#offer-end-label").html("OFFER EXPIRE DATE")
        $("#id_offer_end").attr('placeholder','Not Needed')
    } else {
        $("#id_offer_end").removeAttr('disabled')
        $("#id_offer_end").attr('placeholder','YYYY/MM/DD')
        $("#offer-end-label").html("OFFER EXPIRE DATE *")
    }
})


// BLOGGER
function redirect_at_newblog(){
    window.location.href="/blogs/new-blog-post/"
}

$("input[name=blog-media]").on("click",function(e){
    var val = $("input[name=blog-media]:checked").val()
    $("#id_image_blog").attr('disabled','')
    $("#id_audio").attr('disabled','')
    $("#id_video").attr('disabled','')
    if(val=='image'){
        $("#image-validate-response").html("<span class='blink_me error'>Required field*</span>")
        $("#audio-validate-response").html("<span>Please ignore this field...</span>")
        $("#video-validate-response").html("<span>Please ignore this field...</span>")
        $("#id_"+val+"_blog").removeAttr('disabled')
        
    }else if(val=='audio'){
        $("#image-validate-response").html("<span>Please ignore this field...</span>")
        $("#audio-validate-response").html("<span class='blink_me error'>Required field*</span>")
        $("#video-validate-response").html("<span>Please ignore this field...</span>")
        $("#id_"+val).removeAttr('disabled')
        
    }else if(val=='video'){
        $("#image-validate-response").html("<span>Please ignore this field...</span>")
        $("#audio-validate-response").html("<span>Please ignore this field...</span>")
        $("#video-validate-response").html("<span class='blink_me error'>Required field*</span>")
        $("#id_"+val).removeAttr('disabled')
    }

})

function hide(id){
    let show_reply = `<a class="p-comment__reply" onclick="reply_containt_show(`+id+`)">Reply</a>`
    $("#reply-data-"+id).show()
    $("#reply-data-"+id).attr("style",'display:none;')
    $("#reply-id-"+id).html(show_reply)
    // $("#blog-comment-reply-"+id).removeClass('d-block')
    $("#blog-comment-reply-"+id).attr('style','display:none;')
    // console.log(id)
}
function reply_containt_show(id,to){
    let hide_reply = `<a class="p-comment__reply" onclick="hide(`+id+`)">Hide</a>`
    let show_reply = `<a class="p-comment__reply" onclick="reply_containt_show(`+id+`)">Reply</a>`

    // $(".reply-anchor-container").html(show_reply)
    $(".children-comment").hide()
    $("#reply-data-"+id).show()
    $("#reply-data-"+id).removeAttr("style")
    $("#blog-comment-reply-"+id).removeAttr('style')
    $(".reply-comment").html("@"+to)
    // $("#reply-id-"+id).html(hide_reply)
}

function set_children_comment(to){
    $(".reply-comment").html("@"+to)

}


// VOTING MANAGEMENT 
function blog_comment_voting(bid,cid,tag){
    if(tag=='up-vote'){
        let up_is_checked = $("input[name=blog-comment-up_vote-checkbox-"+cid+"]:checked").val()
        if(up_is_checked==undefined){
            // console.log("upvote checked")
            // ONCLICK VOTING NUMBER CHANGE
            
            // ONCLICK VOTING ICON
            // SETTING UPVOTE BUTTON
            $("#up_vote-icon-"+cid).attr('style','color:rgb(38, 110, 243);','class')
            $("#up-icon-"+cid).attr('style',"cursor: pointer")
            $("#up_vote-icon-"+cid).removeAttr('class')
            $("#up_vote-icon-"+cid).attr('class','fas fa-arrow-alt-circle-up')
            
            // RESETING DOWNVOTE BUTTON
            $("#down_vote-icon-"+cid).removeAttr('style')
            $("#down_vote-icon-"+cid).attr('style',"cursor: pointer")
            $("#down_vote-icon-"+cid).removeAttr('class')
            $("#down_vote-icon-"+cid).attr('class','far fa-arrow-alt-circle-down')
            $("#down-checkbox-wrapper-"+cid).html(`<input type="checkbox" name="blog-comment-down_vote-checkbox-`+cid+`" id="blog-comment-down_vote-`+cid+`" value='down-vote' hidden=''>`)
            
            // // SENDING DATA FOR SERVER, NOW SERVER WILL RESPONDING TWO VALUE UPVOTE,DOWNVOTE
            blog_comments_vote_submit(bid,cid,'upvote','add')
            
        }else{
            console.log("upvote unchecked")
            $("#up_vote-icon-"+cid).removeAttr('style')
            $("#up_vote-icon-"+cid).removeAttr('class')
            $("#up_vote-icon-"+cid).attr('class','far fa-arrow-alt-circle-up')
            $("#up-checkbox-wrapper-"+cid).html()

            // SENDING DATA FOR SERVER, NOW SERVER WILL RESPONDING TWO VALUE UPVOTE,DOWNVOTE
            blog_comments_vote_submit(bid,cid,'upvote','remove')
        }
        
    }else if(tag=='down-vote'){
        let down_is_checked = $("input[name=blog-comment-down_vote-checkbox-"+cid+"]:checked").val()
        if(down_is_checked==undefined){
            console.log("downvote checked")
            // SETTING DOWNVOTE BUTTON
            $("#down_vote-icon-"+cid).attr('style','color:rgb(38, 110, 243);','class')
            $("#down-icon-"+cid).attr('style',"cursor: pointer")
            $("#down_vote-icon-"+cid).removeAttr('class')
            $("#down_vote-icon-"+cid).attr('class','fas fa-arrow-alt-circle-down')
            
            // RESETTING UPVOTE BUTTON
            $("#up_vote-icon-"+cid).removeAttr('style')
            $("#up_vote-icon-"+cid).attr('style',"cursor: pointer")
            $("#up_vote-icon-"+cid).removeAttr('class')
            $("#up_vote-icon-"+cid).attr('class','far fa-arrow-alt-circle-up')
            $("#up-checkbox-wrapper-"+cid).html(`<input type="checkbox" name="blog-comment-up_vote-checkbox-`+cid+`" id="blog-comment-up_vote-`+cid+`" value='up-vote' hidden=''>`)
            
            // // SENDING DATA FOR SERVER, NOW SERVER WILL RESPONDING TWO VALUE UPVOTE,DOWNVOTE
            blog_comments_vote_submit(bid,cid,'downvote','add')
        }else{
            console.log("downvote unchecked")
            $("#down_vote-icon-"+cid).removeAttr('style')
            $("#down_vote-icon-"+cid).removeAttr('class')
            $("#down_vote-icon-"+cid).attr('class','far fa-arrow-alt-circle-down')
            $("#down-checkbox-wrapper-"+cid).html()

            // // SENDING DATA FOR SERVER, NOW SERVER WILL RESPONDING TWO VALUE UPVOTE,DOWNVOTE
            blog_comments_vote_submit(bid,cid,'downvote','remove')
        }
        
    }
}



function blog_voting(bid,tag){
    if(tag=='up-vote'){
        let up_is_checked = $("input[name=upvote-of-"+bid+"]:checked").val()
        // console.log(up_is_checked)
        if(up_is_checked==undefined){
            // console.log("upvote checked")
            // ONCLICK VOTING NUMBER CHANGE
            
            // ONCLICK VOTING ICON
            // SETTING UPVOTE BUTTON
            $("#upvote-icon-"+bid).attr('style','color:rgb(38, 110, 243);cursor: pointer;')
            $("#upvote-icon-"+bid).removeAttr('class')
            $("#upvote-icon-"+bid).attr('class','fas fa-arrow-alt-circle-up')
            
            // RESETING DOWNVOTE BUTTON
            $("#downvote-icon-"+bid).removeAttr('style')
            $("#downvote-icon-"+bid).removeAttr('class')
            $("#downvote-icon-"+bid).attr('class','far fa-arrow-alt-circle-down')
            $("#downvote-checkbox-wrapper-"+bid).html(`<input type="checkbox" name="downvote-of-`+bid+`" id="downvote-checkbox-`+bid+`" value='on'  hidden>`)
            
            // // SENDING DATA FOR SERVER, NOW SERVER WILL RESPONDING TWO VALUE UPVOTE,DOWNVOTE
            blog_voting_submit(bid,'upvote','add')
            // console.log('vote')
            
        }else{
            // console.log("upvote unchecked")
            $("#upvote-icon-"+bid).removeAttr('style')
            $("#upvote-icon-"+bid).removeAttr('class')
            $("#upvote-icon-"+bid).attr('class','far fa-arrow-alt-circle-up')
            $("#upvote-checkbox-wrapper-"+bid).html()

            // SENDING DATA FOR SERVER, NOW SERVER WILL RESPONDING TWO VALUE UPVOTE,DOWNVOTE
            blog_voting_submit(bid,'upvote','remove')
        }
        
    }else if(tag=='down-vote'){
        let down_is_checked = $("input[name=downvote-of-"+bid+"]:checked").val()
        if(down_is_checked==undefined){
            // console.log("downvote checked")
            // SETTING DOWNVOTE BUTTON
            $("#downvote-icon-"+bid).attr('style','color:rgb(38, 110, 243);cursor: pointer;')
            $("#downvote-icon-"+bid).removeAttr('class')
            $("#downvote-icon-"+bid).attr('class','fas fa-arrow-alt-circle-down')
            
            // // RESETTING UPVOTE BUTTON
            $("#upvote-icon-"+bid).removeAttr('style')
            $("#upvote-icon-"+bid).attr('style',"cursor: pointer")
            $("#upvote-icon-"+bid).removeAttr('class')
            $("#upvote-icon-"+bid).attr('class','far fa-arrow-alt-circle-up')
            $("#upvote-checkbox-wrapper-"+bid).html(`<input type="checkbox" name="upvote-of-`+bid+`" id="upvote-checkbox-`+bid+`" value='on' hidden>`)
            
            // // SENDING DATA FOR SERVER, NOW SERVER WILL RESPONDING TWO VALUE UPVOTE,DOWNVOTE
            blog_voting_submit(bid,'downvote','add')
        }else{
            // console.log("downvote unchecked")
            $("#downvote-icon-"+bid).removeAttr('style')
            $("#downvote-icon-"+bid).removeAttr('class')
            $("#downvote-icon-"+bid).attr('class','far fa-arrow-alt-circle-down')
            $("#downvote-checkbox-wrapper-"+bid).html()

            // // SENDING DATA FOR SERVER, NOW SERVER WILL RESPONDING TWO VALUE UPVOTE,DOWNVOTE
            blog_voting_submit(bid,'downvote','remove')
        }
        
    }
}


var blogs_object={
    slice_start:0,
    slice_end:0,
    clicked_page:0,
    get_pages:0,
    total_pages:0,
    query:''
}
function get_blog_pagination(page,get_page,total_pages,query){
    blogs_object.clicked_page=parseInt(page)
    blogs_object.get_pages=parseInt(get_page)
    blogs_object.total_pages=parseInt(total_pages)
    blogs_object.query=query
    blogs_object.slice_end=blogs_object.clicked_page*blogs_object.get_pages
    blogs_object.slice_start=blogs_object.slice_end-blogs_object.get_pages
    for(let i=1;i<=blogs_object.total_pages;i++)
    $("#page-"+i).removeClass()
    $("#page-"+page).attr('class','blog-pg--active')
    $.ajax({
        method:'GET',
        url:'/blogs/get-more-blog/',
        data:{
            'start':blogs_object.slice_start,
            'end':blogs_object.slice_end,
            'order-by':'-id',
            'query':blogs_object.query,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(res){
            // $("#blogs-containt-wrapper-area").attr('style','dispaly:relative;background-color:red;')
            // $("#blogs-containt-wrapper-area").remove()
            $("#blogs-containt-wrapper-area").html(res)
        }
    })
}


// SHARE MY BLOG
function share_my_blog(site_domain,blog_id){
    // console.log("hii there "+blog_id.toString())
    let text = 'I read this blog, that was so intresting. You can visit as well, and find intresting things.';
    let path = "/blogs/blogDetails/"
    $("#blog-media-fb").attr('href','https://www.facebook.com/sharer/sharer.php?u='+site_domain+path+blog_id)
    $("#blog-media-tw").attr('href','https://twitter.com/share?url='+site_domain+path+blog_id+"&text="+text)
    $("#blog-media-insta").attr('href','https://www.instagram.com/share?url='+site_domain+path+blog_id+"&text="+text)
    $("#blog-media-link").attr('href','https://www.linkedin.com/shareArticle?url='+site_domain+path+blog_id+"&title=Excited Artical from E-SHOP&summary="+text)
    $("#blog-link").attr("value",site_domain+path+blog_id)
    $("#share-blog").modal("show")
}



function cancel_my_order(order_id){
    $.ajax({
        method:'POST',
        url:'/return-and-cancellation/',
        data:{
            'order-id':order_id,
            'action':'cancel',
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(res){
            window.location.href="/dashboard/dashCancellation/"
        }
    })
}

function return_my_order(order_id){
    $.ajax({
        method:'POST',
        url:'/return-and-cancellation/',
        data:{
            'order-id':order_id,
            'action':'return',
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(res){
            window.location.href="/dashboard/returned-order/"
        }
    })
}



function hold_item_action(cid){
    let holds = $("#hold_item_"+cid).val()
    let action = holds.split("_")
    if(holds != ''){
        $.ajax({
            method:"POST",
            url:"/selling_product/order-action/",
            data:{
                'action':action[0],
                'cid':action[1],
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
            },success:function(res){
                $("#checkout_processing_item_"+cid).remove()                
            }
        })
    }
}


function view_checkout(cid){
    $(".item-loader").removeAttr('style')
    $.ajax({
        method:"POST",
        url:"/selling_product/view-checkout/",
        data:{
            'cid':cid,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(response){
            $("#checkout_details").html(response)
            $(".item-loader").attr('style',"display:none;")
            window.location.href="/selling_product/holdDelevery/#checkout_details"           
        }
        })
    }

function view_returns(cid){
    $(".item-loader").removeAttr('style')
    $.ajax({
        method:"POST",
        url:"/selling_product/view-checkout/",
        data:{
            'cid':cid,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(response){
            $("#checkout_details").html(response)
            $(".item-loader").attr('style',"display:none;")
            window.location.href="/selling_product/returns-product/#checkout_details"           
        }
        })
    }
function view_deliveries(cid){
    $(".item-loader").removeAttr('style')
    $.ajax({
        method:"POST",
        url:"/selling_product/view-checkout/",
        data:{
            'cid':cid,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(response){
            $("#checkout_details").html(response)
            $(".item-loader").attr('style',"display:none;")
            window.location.href="/selling_product/deleverdProduct/#checkout_details"           
        }
        })
    }

function print_receipt(){
    print()
}

function client_details(client_id){
    $(".item-loader").removeAttr('style')
    $.ajax({
        method:"POST",
        url:"/selling_product/view-client/",
        data:{
            'client':client_id,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(response){
            $("#client_details").html(response)
            $(".item-loader").attr('style','display:none;')
            window.location.href="/selling_product/clientList/#client_details"           
        }
    })
}

