// @Author SATYA NARAYAN MISHRA
// ################################### Subscribing Verification ###############################
class User_email_verification{
    constructor(user,email){
        this.user=user
        this.email=email
    }
}
let is_verified_user = false
let is_verified_email = false
$("#logout").click(function(e){
    e.preventDefault();
    $.ajax({
        method:'POST',
        url:"/accounts/logout/",
        data:{
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },
        success:function(response){
            $("#modalText").html("<span class='success'>Thank You ! Logout Successfully..</span>")
            $("#ourModal").modal("show");
            redirect_at_home()
        },error:function(response){
            $("#modalText").html("<span class='error'>Opps ! Problem occured during logout </span>")
            $("#ourModal").modal("show");
            redirect_at_home()
        }
    })
})

$(document).on('submit',"#subscribe-form",function(e){
    e.preventDefault();
    let usrgender = ""
    if($(".gender").val()=="" || $("#newsletter").val()==""){
        $("#modalText").html("<span style='color:red;'><i class='fa fa-exclamation'></i>&nbsp;&nbsp;&nbsp;Sorry, All fields required* &#128524;</span>")
        $('#ourCloseButton').html("<b>Try,Again</b>");
        $("#ourModal").modal("show");
    }else{
        usrgender = $("input[name='gender']:checked").val();
        $.ajax({
            method:'POST',
            url:"/",
            data:{
                gender:usrgender,
                email:$("#newsletter").val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function (){
                $("#ourModalLabel").html("<span>E-SHOP SUBSCRIBE</span>");
                $("#modalText").html("<span style='color:green;'><i class='fa fa-check'></i>&nbsp;&nbsp;&nbsp;Thanks, You have successfully subscribe. &#128525;</span>")
                $('#ourCloseButton').html("<b>Done</b>");
                $("#ourModal").modal("show");
            },  
            error:function (){
                $("#modalText").html("<span style='color:red;'><i class='fa fa-exclamation'></i>&nbsp;&nbsp;&nbsp;Sorry, You are, already subscribed &#128524;</span>")
                $('#ourCloseButton').html("<b>Try,another</b>");
                $("#ourModal").modal("show");
            },
        });
    }
});

// ################################### ALERT MESSAGE ##################################
function alert_message(message,tag){
    html_content = modal()
    document.getElementById("alert-message").innerHTML=html_content;
    if(tag=="success"){
        $("#modalText").html("<span style='color:green;'><i class='fa fa-check'></i>&nbsp;&nbsp;&nbsp;"+message+" &#128525;</span>")
        $('#alertCloseButton').html("<b>Ok</b>");
        $("#alertModal").modal("show");
    }else{
        $("#modalText").html("<span style='color:red;'><i class='fa fa-exclamation'></i>&nbsp;&nbsp;&nbsp;"+message+" &#128553;</span>")
        $('#alertCloseButton').html("<b>Try,Again</b>");
        $("#alertModal").modal("show");
    }
}
// Bootstrap modal
function modal(){
    return '<div class="modal fade" id="alertModal" tabindex="-1" role="dialog" aria-labelledby="alertModalLabel" aria-hidden="true">'
        +'<div class="modal-dialog" role="document">'
        +'<div class="modal-content">'
            +'<div class="modal-header">'
            +'<h5 class="modal-title" id="alertModalLabel"><b style="color: black;">E-SHOP</b></h5>'
            +'<button class="normal-text-shadow" type="button" data-dismiss="modal" aria-label="Close" style="border:none;background:transparent;color:red">'
                +'<span aria-hidden="true">&times;</span>'
            +'</button>'
            +'</div>'
            +'<div class="modal-body px-5" id="modalText">'


            +'</div>'
            +'<div class="modal-footer">'
            +'<button type="button" class="btn btn--e-brand" data-dismiss="modal" id="alertCloseButton" style="padding: 10px;font:bold;"><b>Close</b></button>'
            +'</div>'
        +'</div>'
        +'</div>'
    +'</div>'

}
//########################################## USERNAME VALIDATION #####################################
function check_space(val){
    for(let i=0;i<val.length;i++) if(val[i]==" ") return true
}
function null_val_warning(id){
    $(id).html("<span class='response-message invalid blink_me'>Required Field *</span>")
}
function min_max_val_warning(min,max,name,id){
    $(id).html("<span class='response-message invalid'>Warning : "+name+", Min : "+min+" & Max : "+max+" word *</span>")
}
function check_usr(usr_name){
    // console.log(usr_name)
    if(usr_name == "" || usr_name == null){
        null_val_warning('#username-validate-response')
        is_verified_user=false
    }else if(usr_name.length<4 || usr_name.length>50){
        min_max_val_warning(4,50,"Username",'#username-validate-response')
        is_verified_user=false
    }else if(check_space(usr_name)){
        $('#username-validate-response').html("<span class='response-message invalid'>Warning : Space are not allowed in Username *</span>")
        is_verified_user=false
    }else{
        $.ajax({
            method:'POST',
            url:"/accounts/register/",
            data:{'user_name':usr_name.trim(),
            'username_validation':'validation',
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val().trim()},
            success:function (response) {
                if(response=="valid"){
                    $('#username-validate-response').html("<span class='response-message valid'> &#10004; Valid Username..</span>")
                    is_verified_user=true
                }else if(response=="invalid"){
                    $('#username-validate-response').html("<span class='response-message invalid'> &#10006; This Username already exist*</span>")
                    is_verified_user=false
                }
            },
            error:function(response){
                alert("SERVER ERROR : Server response error..")
            }
        })
    }
}
$("#id_username").blur(function(e){
    e.preventDefault();
    let usr_name = $("#id_username").val().trim()
    check_usr(usr_name)
})

// ############################################ EMAIL VALIDATION ####################################
function check_email(myemail){
    // saving user verification
    if(myemail=='' || myemail==null){
        $('#email-validate-response').html("<span class='response-message invalid'>Required Field *</span>")
        is_verified_email = false
    }else{
        $.ajax({
            method:'POST',
            url:"/accounts/register/",
            data:{'email':myemail,
            'email_validation':'validation',
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val().trim()},
            success:function (response) {
                if(response=="valid"){
                    $('#email-validate-response').html("<span class='response-message valid'> &#10004; Valid Email..</span>")
                    is_verified_email = true
                }else if(response=="invalid"){
                    $('#email-validate-response').html("<span class='response-message invalid'> &#10006; This email already exist*</span>")
                    is_verified_email = false
                }else if(response=="invalid email"){   
                    $('#email-validate-response').html("<span class='response-message invalid'> &#10006; Invalid Email : Ex - somthing@subdomain.domain*</span>")   
                    is_verified_email = false
                }
            },
            error:function(rs){
                is_verified_email = false
                alert("Opps ! Server respond error...")
            }
        })
    }
}
$("#id_email").blur(function(e){
    e.preventDefault();
    let myemail = $("#id_email").val().trim()
    check_email(myemail)
})


// ############################# Registration Verification ###################################
// $("#submit-registration").submit();
function phone_number_validate(data){
    let can_be ="+0123456789"
    let val=data.trim()
    if(data!=null||data!=''){
        if(val[0]!=can_be[0]){
            return false
        }else{
            if(val[0]!=can_be[0])
            for(let i=0;i<val.length;i++){
                let counter=0
                for(let j=0;j<can_be.length;j++){
                    if(val[i] != can_be[j]){
                        counter+=1
                    }
                }
                if(counter==can_be.length) return false
            }
            return true
        }
    }else return false
}
function number_validate(data){
    let can_be ="0123456789"
    let val=data.trim()
    if(data!=null||data!=''){
        for(let i=0;i<val.length;i++){
            let counter=0
            for(let j=0;j<can_be.length;j++){
                if(val[i] != can_be[j]){
                    counter+=1
                }
            }
            if(counter==can_be.length) return false
        }
        return true
    }else return false
}

//Date of Birth Validator
function dob_validate(val){
    let dob = val.trim()
    let can_be = "0987654321-"
    let dob_sample = "yyyy-mm-yy"
    let split_dob = dob.split("-")
    if(dob.length>10 || dob.length<10){
        return false
    }else{
        for(let i=0;i<dob.length;i++){
            let counter=0
            for(let j=0;j<can_be.length;j++){
                if (dob[i] != can_be[j]){
                    counter+=1
                }
            }
            if(counter==can_be.length){return false}
        }
        for (let i=0;i>dob_sample.length;i++){
            if(dob[i].length == dob_sample[i].length){
                return true
            }else return false
        }
        return true
    }
}
function date_validate(val){
    let date = val.trim()
    let can_be = "0987654321/"
    let date_sample = "yyyy/mm/yy"
    let split_date = date.split("-")
    if(date.length>10 || date.length<10){
        return false
    }else{
        for(let i=0;i<date.length;i++){
            let counter=0
            for(let j=0;j<can_be.length;j++){
                if (date[i] != can_be[j]){
                    counter+=1
                }
            }
            if(counter==can_be.length){return false}
        }
        for (let i=0;i>date_sample.length;i++){
            if(dob[i].length == date_sample[i].length){
                return true
            }else return false
        }
        return true
    }
}


$("#submit-registration-form").click(function (e){
    let usrname=$("#id_username").val().trim()
    let fname=$("#id_first_name").val().trim()
    let lname=$("#id_last_name").val().trim()
    let gender=$("#id_gender").val().trim()
    let dob=$("#id_dob").val().trim()
    let profile_pic=$("#id_profile_pic").val()
    let email=$("#id_email").val().trim()
    let country=$("#id_country").val().trim()
    let password=$("#id_password").val().trim()
    e.preventDefault();
    if(is_verified_email && is_verified_user){
        if(profile_pic == '' || profile_pic == null || fname=='' || fname == null || gender==""||gender==null||dob==""||dob==null||email==""||email==null||country==""||country==null||password==""||password==null){
            // Null Value Validation
            if(fname=='' || fname == null) null_val_warning("#fname-validate-response")
            if(gender=='' || gender == null) null_val_warning("#gender-validate-response")
            if(dob=='' || dob == null) null_val_warning("#dob-validate-response")
            if(email=='' || email == null) null_val_warning("#email-validate-response")
            if(country=='' || country == null) null_val_warning("#country-validate-response")
            if(password=='' || password == null) null_val_warning("#password-validate-response")
            if(profile_pic == '' || profile_pic == null) null_val_warning("#profile_pic_help_text")
        }else if(fname.length<2 || fname.length>50 || lname.length>50 || password.length<8){
            // Length Validation
            if(fname.length<2 || fname.length>50) min_max_val_warning(2,50,"First Name ",'#fname-validate-response')
            if(lname.length>50) min_max_val_warning("Null",50,"Last Name","#lname-validate-response")
            if(password.length<8 || password.length>300) min_max_val_warning(8,300,"Password ",'#password-validate-response')
        }else if(!dob_validate(dob)){
            $('#dob-validate-response').html("<span class='response-message invalid'>&#10006; DOB : Ex - YYYY-MM-DD *</span>")   
        }else{
            $("#registration-form").submit();
        }
    }else{
        console.log("username and email not verified")
    }  

})

// DOB- VALIDATER
$("#reg_dob").blur(function(e){
    let dob = $("#reg_dob").val();
    if(!dob_validate(dob)){
        $('#dob-validate-response').html("<span class='response-message invalid'>&#10006; DOB : Ex - YYYY-MM-DD *</span>")   
    }else{
        $('#dob-validate-response').html("<span class='response-message valid'>&#10004; Valid DOB</span>")   
    }
})

// Email validation
function validateEmail($email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    return emailReg.test( $email );
}

// Redirect me on login page
function redirect_at_login(){
    setTimeout(function(){
        window.location.href="/accounts/login/"
    },2000)
}
function redirect_at_home(){
    setTimeout(function(){
        window.location.href="/"
    },2000)
}
function redirect_me_signup(){
    window.location.href="/accounts/register/"
}



// ################################################## LOGIN ##########################################################
$("#login-form").on("submit",function(e){
    e.preventDefault()
    let loginId = $("#login-id").val().trim()
    let passwd = $("#login-password").val().trim()
    let remember_me = $("input[name='remember-name']:checked")
    
    if(loginId == "" || loginId == null || passwd == null || passwd==""){
        if(loginId == "" || loginId == null){
            $("#loginid-validate-response").html("<span class='response-message invalid'>User ID are Field Required*</span>")
        }else if(passwd == "" || passwd == null){
            $("#password-validate-response").html("<span class='response-message invalid'>Password are Field Required*</span>")
        }
    }else{
        if(remember_me=="on"){
            // Cookie expire after 10 day
            $.cookie('login-id',loginId,{expires:10}) 
            $.cookie('password',passwd,{expires:10})
            $.cookie("remember-me",true,{expires:10})
        }
        html_content = modal()
        $.ajax({
            method:'POST',
            url:"/accounts/login/",
            data:{
                'usrId':loginId,
                'password':passwd,
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
            },
            success:function(response){
                if(response=='success'){
                    window.location.href="/"
                }else{
                    $("#pop-up-response").html(html_content)
                    $('#modalText').html("Opps ! Invalid Credential.")
                    $("#modalCloseButton").html("Try, Agin")
                    $("#alertModal").modal("show")
                }
            },
            error:function(response){
                alert("Opps ! somthing wrong during login..")
            }
        })
    }
    
})

// &#10004; => Check
// &#10006  => Cross


// ################### RESET PASSWORD #####################
$("#reset-password").on("submit",function(e){
    e.preventDefault()
    let email = $("#reset-email").val().trim()
    if(email == '' || email == false){
        $("#gmail-help-text").html("<span class='error response-message blink_me'>Email are required field*</span>")
    }else{
        $.ajax({
            method:'POST',
            url:'/accounts/lostPassword/',
            data:{
                'email':email,
                 csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val().trim()
            },
            success:function(response){
                html_content = modal()
                document.getElementById("alert-message").innerHTML=html_content;
                if(response=="success"){
                    $("#modalText").html("<span style='color:green;'><i class='fa fa-check'></i>&nbsp;&nbsp;&nbsp;Check Your mail. Password Reset Link Send successfully.</span>")
                    $('#alertCloseButton').html("<b>Ok</b>");
                    $("#alertModal").modal("show");
                }else{
                    $("#modalText").html("<span style='color:red;'><i class='fa fa-exclamation'></i>&nbsp;&nbsp;&nbsp;Sorry ! You are not signup yet.</span>")
                    $('#alertCloseButton').html("<b>Try,Again</b>");
                    $("#alertModal").modal("show");
                }
            },
            error:function(){
                alert("Error : Server responding some error.")
            }
        });
    }
});









// ###################################### USER EDIT PROFILE #####################################
$("#edit-user-profile").on("submit",function(e){
    e.preventDefault()
    let loggedUserId = $("#loggedUserId").val().trim()
    let username = $("#id_username").val().trim()
    let email = $("#id_email").val().trim()
    let fname = $("#id_first_name").val().trim()
    let lname = $("#id_last_name").val().trim()
    let gender = $("#reg-gender").val().trim()
    let dob = $("#reg_dob").val().trim()
    let country = $("#reg-country").val().trim()
    if(email=="" || email==null||username==""||username==null||fname=="" || fname==null || gender == '' || gender == null || dob == '' || dob == null || country == '' || country ==null){
        if(username=='' || username == null) null_val_warning("#username-validate-response")
        if(email=='' || email == null) null_val_warning("#email-validate-response")
        if(fname=='' || fname == null) null_val_warning("#fname-validate-response")
        if(gender=='' || gender == null) null_val_warning("#gender-validate-response")
        if(dob=='' || dob == null) null_val_warning("#dob-validate-response")
        if(country=='' || country == null) null_val_warning("#country-validate-response")
    }else{
        if(dob_validate(dob)){
            
            $.ajax({
                method:'POST',
                url:'/dashboard/update-user-profile/',
                data:{
                    'loggedUserId':loggedUserId,
                    'username':username,
                    'email':email,
                    'fname':fname,
                    'lname':lname,
                    'gender':gender,
                    'dob':dob,
                    'country':country,
                    csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
                },
                success:function(response){
                    alert("Your profile updated...")
                },
                error:function(response){
                    alert("error updating")
                }
            });
        }else{
            $("#dob-validate-response").html("<span class='invalid response-message blink_me'> Invalid DOB : YYYY-MM-DD</span>")
        }
    }
})


$("#old-password").blur(function(e){
    e.preventDefault()
    // $("#ourModal").html=modal()
    $.ajax({
        method:'POST',
        url:'/dashboard/verify-password/',
        data:{
            'loggedUser':$("#loggedUser").val().trim(),
            'password':$("#old-password").val().trim(),
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()},
        success:function(res){
            if(res == 'valid'){
                $("#old-password-response").html("<span class='success'>&#10004; Verified</span>")
                $("#pass2").html('<input type="password" class="input-text input-text--primary-style" placeholder="Type new password" id="new-password2">')
                $("#pass1").html('<input type="password" class="input-text input-text--primary-style" placeholder="Re-Type new password" id="new-password1">')
                // console.log("valid")
            }else{
                $("#old-password-response").html("<span class='error blink_me'>&#10006; Invalid Password</span>")
                $("#pass1").html('<input type="password" class="input-text input-text--primary-style" placeholder="Type new password" disabled>')
                $("#pass2").html('<input type="password" class="input-text input-text--primary-style" placeholder="Type new password" disabled>')
                // console.log("invalid")
            }
        },error:function(res){
            alert("Opps ! Somthing wrong..");
        }

    })
})

$("#changePass").on("submit",function(e){
    e.preventDefault()
    loggedUser = $("#loggedUser").val().trim()
    oldPass = $("#old-password").val().trim()
    pass1 = $("#new-password1").val().trim()
    pass2 = $("#new-password2").val().trim()
    csrf = $("input[name=csrfmiddlewaretoken]").val()
    if(oldPass==''||oldPass==null){
        $("#old-password-response").html("<span class='error blink_me'>Required Field*</span>")
    }else if(pass1==''||pass1==null){
        $("#new-password1-response").html("<span class='error blink_me'>Required Field*</span>")
        $("#new-password2-response").html("")
    }else if(pass2==''||pass2==null){
        $("#new-password2-response").html("<span class='error blink_me'>Required Field*</span>")
        $("#new-password1-response").html("")
    }else if(pass1.length<8||pass1.length>300){
        $("#new-password1-response").html("<span class='error blink_me'>Password should, at least 8 charecter*</span>")
        $("#new-password2-response").html("")
    }else if(pass2.length<8||pass2.length>300){
        $("#new-password2-response").html("<span class='error blink_me'>Password should, at least 8 charecter*</span>")
        $("#new-password1-response").html("")
    }else if(pass1!=pass2){
        $("#new-password1-response").html("<span class='error blink_me'>Password should be same..</span>")
        $("#new-password2-response").html("<span class='error blink_me'>Password should be same..</span>")
    }else{
        $("#new-password1-response").html("")
        $("#new-password2-response").html("")
        $("#ourModal").html(modal())
        $.ajax({
            method:"POST",
            url:"/dashboard/change-password/",
            data:{
                'loggedUser':loggedUser,
                'oldPassword':oldPass,
                'newPassword':pass1,
                csrfmiddlewaretoken:csrf,
            },
            success:function(response){
                if(response=='updated'){
                    $("#modalText").html("<span class='success'>Password Changed successfully...</span>")
                    $('#alertModal').modal("show")
                    setTimeout(function(){
                        window.location.href="/accounts/login/"
                    },2000)
                    // alert("password changed")
                }else{
                    $("#modalText").html("<span class='error'>Opps ! Invalid Credential...</span>")
                    $('#alertModal').modal("show")
                    // alert("Not changed...")
                }
            },
            error:function(response){
                alert("Opps ! Somthing wen't wrong during password changing")
            }
        })
    }
})



let loggedUser = 0
function set_logged_user(id){
    loggedUser = id
}

let loggedUsername = ''
function set_logged_username_id(params1,params2) {
    loggedUser = params1
    loggedUsername = params2
}
let EditaddressId = 0
function set_address_id(id){
    EditaddressId=id
}
function submit_address_form(ourMethod,ourUrl){
    let fname = $("#id_first_name").val().trim()
    let lname = $("#id_last_name").val().trim()
    let phone = $("#id_mobile").val().trim()
    let country = $("#id_country").val().trim()
    let state = $("#id_state").val().trim()
    let zip = $("#id_pin_code").val().trim()
    let address = $("#id_full_address").val().trim()
    if(fname==null||fname==""||phone==""||phone==null||country==""||country==null||state==""||state==null||zip==""||zip==null||address==""||address==null){
        if(fname==null||fname=="") null_val_warning("#fname-response")
        if(phone==null||phone=="") null_val_warning("#mobile-response")
        if(country==null||country=="") null_val_warning("#country-response")
        if(state==null||state=="") null_val_warning("#state-response")
        if(zip==null||zip=="") null_val_warning("#pincode-response")
        if(address==null||address=="") null_val_warning("#address-response")
    }else{
        if(number_validate(zip)&&phone_number_validate(phone)){
            $('#mobile-response').html("<span class='success'>&#10004 Valid</span>") 
            $('#pincode-response').html("<span class='success'>&#10004 Valid</span>")
            if(lname==''||lname==null) lname=''
            $("#Modal").html(modal())
            $.ajax({
                method:ourMethod,
                url:ourUrl,
                data:{
                    'loggedUser':loggedUser,
                    'fname':fname,
                    'lname':lname,
                    'phone':phone,
                    'country':country,
                    'state':state,
                    'zip':zip,
                    'address':address,
                    csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
                },
                success:function(response){
                    if(response=='success'){
                        $("#modalText").html("<span class='success'>Record Updated successfully !</span>")
                        $('#alertCloseButton').html("<b>Ok</b>");
                        $("#alertModal").modal("show")
                    }else{
                        $("#modalText").html("<span class='error'>Opps ! Somthing problem during updating.. !</span>")
                        $('#alertCloseButton').html("<b>Try, Again</b>");
                        $("#alertModal").modal("show")
                    }
                },error:function(res){
                    alert("Error : Somthing problem..")
                }
            })
        }else{
            if(!phone_number_validate(phone)){
                $('#mobile-response').html("<span class='error blink_me'>Warning : Invalid mobile number. it should be number</span>")
            }else $('#mobile-response').html("<span class='success'>&#10004; Valid</span>")

            if(!number_validate(zip)) 
            {
                $('#pincode-response').html("<span class='error blink_me'>Warning : Invalid ZIP/Postal Code. it should be number</span>")
            }else $('#pincode-response').html("<span class='success'>&#10004; Valid</span>")

        }
    }
}
// EDIT ADDRESS
$("#edit-address").on("submit",function(e){
    e.preventDefault()
    if(loggedUser==0 && EditaddressId == 0){
        $("#id-response").html("<span class='error blink_me'>There are unexpected behaviour..</span>");
        setTimeout(() => {
            window.location.href="/dashboard/dashAddressBook/"
        }, 2000);
    }else{
        submit_address_form('POST','/dashboard/dashAddressEdit/'+EditaddressId+"/",)
    }
})

// Add New Address
$("#add-new-address").on("submit",function(e){
    e.preventDefault()
    if(loggedUser==0){
        $("#id-response").html("<span class='error blink_me'>There are unexpected behaviour..</span>");
        setTimeout(() => {
            window.location.href="/dashboard/dashAddressBook/"
        }, 2000);
    }else{
        submit_address_form('POST','/dashboard/dashAddressAdd/',)
    }
    
})



// ################## PRODUCT RELATED ACTIONS ##################
$("#add-product").on("submit",function() {
    let category = $("#id_category").val()
    let subcategory = $("#id_subcategory").val()
    let brand = $("#id_brand").val()
    let title = $("#id_title").val()
    let discount = $("#id_m_r_p").val()
    let available = $("#id_available_product").val()
    let isOffer = $("#id_is_offer").val()
    let color_code = $("#id_color_code").val()
    let charge = $("#id_shipping_charge").val()
    let tags = $("#id_tags").val()
    let policy = $("#id_product_policy").val()
    let image = $("#id_image").val()
    let discription = $("#id_discription").val()
    let embed = $("#id_video_url").val()
    let price = $("#id_price").val()
    let offer=$("#id_is_offer").val()
    let flag=false
    if(offer=='YES'){
        let expire = $("#id_offer_end").val().trim()
        if(date_validate(expire) == true & expire != ''){
            flag=true
        }else{
            $("#offer-expire-response").html("<span class='blink_me'>Date format is not valid, Date should be YYYY/MM/DD</span>")
        }
    }else{
        // date validation isn't required
        flag=true
    }

    if(flag=true){
        if(loggedUser==0 || loggedUsername =='' || category==null||category==''||subcategory==null||subcategory==''
            ||brand==null||brand==''||title==null||title==''||discount==null||discount==''
            ||available==null||available==''||isOffer==null||isOffer==''||color_code==null||color_code==''
            ||charge==null||charge==''||tags==null||tags==''||policy==null||policy==''||image==null||image==''
            ||discription==null||discription==''||embed==null||embed==''||price==null||price==''){
                if(loggedUser==0||loggedUsername=='') window.location.href='/'
                if(title==null||title=='') $("#accessories-response").html("<span class='error blink_me'>Required field *</span>")
                if(color_code==null||color_code=='') $("#color-response").html("<span class='error blink_me'>Required field *</span>")
                if(category==null||category=='') $("#category-response").html("<span class='error blink_me'>Required field *</span>")
                if(subcategory==null||subcategory=='') $("#subcategory-response").html("<span class='error blink_me'>Required field *</span>")
                if(brand==null||brand=='') $("#brandname-response").html("<span class='error blink_me'>Required field *</span>")
                if(isOffer==null||isOffer=='') $("#offer-response").html("<span class='error blink_me'>Required field *</span>")
                if(available==null||available=='') $("#available-response").html("<span class='error blink_me'>Required field *</span>")
                if(price==null||price=='') $("#price-response").html("<span class='error blink_me'>Required field *</span>")
                if(charge==null||charge=='') $("#shipping-charge-response").html("<span class='error blink_me'>Required field *</span>")
                if(discount==null||discount=='') $("#mrp-response").html("<span class='error blink_me'>Required field *</span>")
                if(image==null||image=='') $("#image-response").html("<span class='error blink_me'>Required field *</span>")
                if(embed==null||embed=='') $("#embed-response").html("<span class='error blink_me'>Required field *</span>")
                if(policy==null||policy=='') $("#policy-response").html("<span class='error blink_me'>Required field *</span>")
                if(tags==null||tags=='') $("#tag-response").html("<span class='error blink_me'>Required field *</span>")
                if(discription==null||discription=='') $("#discription-response").html("<span class='error blink_me'>Required field *</span>")
            }else{$("#add-product").submit()}
    }
})

$("#product-edit-form").on("submit",function() {
    let category = $("#id_category").val()
    let subcategory = $("#id_subcategory").val()
    let brand = $("#id_brand").val()
    let title = $("#id_title").val()
    let discount = $("#id_m_r_p").val()
    let available = $("#id_available_product").val()
    let isOffer = $("#id_is_offer").val()
    let color_code = $("#id_color_code").val()
    let charge = $("#id_shipping_charge").val()
    let tags = $("#id_tags").val()
    let policy = $("#id_product_policy").val()
    let discription = $("#id_discription").val()
    let embed = $("#id_video_url").val()
    let price = $("#id_price").val()
    if(loggedUser==0 || loggedUsername =='' || category==null||category==''||subcategory==null||subcategory==''
    ||brand==null||brand==''||title==null||title==''||discount==null||discount==''
    ||available==null||available==''||isOffer==null||isOffer==''||color_code==null||color_code==''
    ||charge==null||charge==''||tags==null||tags==''||policy==null||policy==''
    ||discription==null||discription==''||embed==null||embed==''||price==null||price==''){
        if(loggedUser==0||loggedUsername=='') window.location.href='/'
        if(title==null||title=='') $("#accessories-response").html("<span class='error blink_me'>Required field *</span>")
        if(color_code==null||color_code=='') $("#color-response").html("<span class='error blink_me'>Required field *</span>")
        if(category==null||category=='') $("#category-response").html("<span class='error blink_me'>Required field *</span>")
        if(subcategory==null||subcategory=='') $("#subcategory-response").html("<span class='error blink_me'>Required field *</span>")
        if(brand==null||brand=='') $("#brandname-response").html("<span class='error blink_me'>Required field *</span>")
        if(isOffer==null||isOffer=='') $("#offer-response").html("<span class='error blink_me'>Required field *</span>")
        if(available==null||available=='') $("#available-response").html("<span class='error blink_me'>Required field *</span>")
        if(price==null||price=='') $("#price-response").html("<span class='error blink_me'>Required field *</span>")
        if(charge==null||charge=='') $("#shipping-charge-response").html("<span class='error blink_me'>Required field *</span>")
        if(discount==null||discount=='') $("#mrp-response").html("<span class='error blink_me'>Required field *</span>")
        if(embed==null||embed=='') $("#embed-response").html("<span class='error blink_me'>Required field *</span>")
        if(policy==null||policy=='') $("#policy-response").html("<span class='error blink_me'>Required field *</span>")
        if(tags==null||tags=='') $("#tag-response").html("<span class='error blink_me'>Required field *</span>")
        if(discription==null||discription=='') $("#discription-response").html("<span class='error blink_me'>Required field *</span>")
    }else{$(this).submit()}
})


// PRODUCT SEARCHING
$("#product-search").on("keyup",function(e){
    e.preventDefault()
    let productId = $(this).val()
    let filterBy = $("#filterBy").val().trim()
    $.ajax({
        method:'GET',
        url:'/selling_product/get-product/',
        data:{
            'productId':productId,
            'filterBy':filterBy,
            'loggedUser':loggedUser,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },
        success:function(response){
            if(response == 'invalid') $("#product-table").html("<thead>No Data Found</thead>")
            else $("#product-table").html(response)
        }
    })
})

$("#filterBy").on("change",function(e){
    e.preventDefault()
    let productId = $("#product-search").val()
    let filterBy = $("#filterBy").val().trim()
    $.ajax({
        method:'GET',
        url:'/selling_product/get-product/',
        data:{
            'productId':productId,
            'filterBy':filterBy,
            'loggedUser':loggedUser,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },
        success:function(response){
            if(response == 'invalid') $("#product-table").html("<thead>No Data Found</thead>")
            else $("#product-table").html(response)
        }
    })
})




// ADD PRODUCT SUBSCRIBER INTO DATABASE
function add__subscriber(user_id,product_id,status){
    $.ajax({
        method:'POST',
        url:'/selling_product/add-product-subscriber/',
        data:{
            'user':user_id,
            'product':product_id,
            'status':status,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        }
    })
}


// BLOGGER
$("#new-blog-post-form").on("submit",function(e){
    // e.preventDefault()
    let radio = $("input[name='blog-media]:checked").val()
    let title = $("#id_title").val()
    let tag = $("#id_tags").val()
    tinyMCE.triggerSave();
    let dis = $("#id_discription").tinymce().activeEditor.getContent()

    // let dis = $("#id_discription_ifr").val()
    if(title==''||title==null||tag==''||tag==null||dis==''||dis==null){
        $("#title-validate-response").html("<span class='error blink_me'>Required Field*</span>")
        $("#tag-validate-response").html("<span class='error blink_me'>Required Field*</span>")
        $("#dis-validate-response").html("<span class='error blink_me'>Required Field*</span>")
        return false
    }else{
        $("#new-blog-post-form").submit()
    }
})

function get_blog(blog_id,label){
    $.ajax({
        method:'GET',
        url:'/blogs/get-blog/',
        data:{
        'blog-id':blog_id,
        'label':label,
        csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(data){
            $("#blog-wrapper").html(data)
        }
    })
}
let comment_html=`

`
$("#comment-form").on("submit",function(e){
    // e.preventDefault()
    blog_id = $("#blog-id").val().trim()
    comment = $("#comment").val().trim()
    if(blog_id=='' || blog_id==null || comment=='' || comment==null){
        alert("All Field Required !")
        return false
    }else{
        return true
    }
    // $.ajax({
    //     method:'GET',
    //     url:'/blogs/blog-comment/',
    //     data:{
    //         'blog-id':blog_id,
    //         'comment':comment,
    //         csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
    //     }
    // })
})


function delete_blog_comment(comment_id){
    let blog_id = $("#blog-id").val()
    let comment_containt = `
<span class="d-meta__text-2 u-s-m-b-6">Join the Conversation</span>

<span class="d-meta__text-3 u-s-m-b-16">Your email address will not be published. Required fields are marked *</span>
<form class="respond__form" action="/blogs/blog-comment/" method="GET" id="comment-form">
    <div class="respond__group">
        <div class="u-s-m-b-15">
            
            <label class="gl-label" for="comment">COMMENT *</label><textarea name="comment" class="text-area text-area--primary-style" id="comment" ></textarea>
        </div>
        <div>
            <input type="hidden" name="blog-id" id="blog-id" value="`+blog_id+`">
        </div>
    </div>
    <div>

        <button class="btn btn--e-brand-shadow" type="submit">POST COMMENT</button>
    </div>
</form>
`
    $("#comment-wrapper-"+comment_id).hide()
    $("#comment_form").html(comment_containt)
    $.ajax({
        method:'GET',
        url:"/blogs/delete-comment/",
        data:{
            'comment-id':comment_id,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        }
    })
}

$("#comment-reply-form").on("submit",function(e){
    let rcid = $("#reply-comment-id").val()
    let bid = $("#reply-blog-id").val()
    let rc = $("#reply-comment").val()
    if(bid==null||bid==''||rc==null||rc==''||rcid==''||rcid==null){
        return false
    }else{
        return true
    }
})

function delete_reply_blog_comment(comment_id,bid,uid){
    $("#reply-comment-target-"+comment_id+"-"+uid).hide()
    // console.log(uid)
    $.ajax({
        method:"GET",
        url:'/blogs/delete-reply-comment/'+bid,
        data:{
            'comment-id':comment_id,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        }
    })
}

function blog_comments_vote_submit(bid,cid,vote_type,action){
    $.ajax({
        method:'GET',
        url:'/blogs/blog-comment-vote/',
        data:{
            'bid':bid,
            'cid':cid,
            'vote-type':vote_type,
            'action':action,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(data){
            let response = data.split(",")
            $("#blog-comment-up_vote_counter-"+cid).html(response[0])
            $("#blog-comment-down_vote_counter-"+cid).html(response[1])
        }
    })
}


// BLOG VOTING
function blog_voting_submit(bid,vote_type,action){
    // console.log("want update")
    $.ajax({
        method:'GET',
        url:'/blogs/blog-voting/',
        data:{
            'blog-id':bid,
            'vote-type':vote_type,
            'action':action,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(data){
            let response=data.split(",")
            $("#blog-upvote-"+bid).html(response[0])
            $("#blog-downvote-"+bid).html(response[1])
        }
    })
}

// blog searching
$("#blog-search-form").on("submit",function(e){
    
    let q=$("#blog-search").val()
    if(q=='' || q==null){
        return false
    }else{
        return true
    }
})

function edit_blog(media_url,blog_id){
    $("#blog_id").val(blog_id)
    $.ajax({
        method:"GET",
        url:"/blogs/get-blog-details/",
        data:{
            'blog-id':blog_id,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(response){
            split_response=response.split("::")
            $("#id_title").val(split_response[1])
            $("#id_tags").val(split_response[2])
            tinyMCE.activeEditor.setContent(split_response[3]);
            // $(".mce-content-body").val(split_response[3])
            // console.log($("#tinymce").val())
            // console.log(split_response[4])
            // console.log(split_response[5])
            // console.log(split_response[6])
            if(split_response[4] == "" & split_response[5] == '' & split_response[6] == ''){
                $("#id_image_blog").attr("disabled","")
                    $("#id_video").attr("disabled","")
                    $("#id_video").val("")
    
                    $("#audio-validate-response").html("Please ignore this field..")
                    $("#video-validate-response").html("Please ignore this field..")
                    $("#image-validate-response").html("Please ignore this field..")
    
                    $("input[name=blog-media]").removeAttr("checked")
                    $("#none").attr("checked","")
    
            }else{
                if(split_response[4] == "" & split_response[5] == "" ){
                    $("#id_image_blog").attr("disabled","")
                    $("#id_audio").attr("disabled","")
    
                    $("#id_video").removeAttr("disabled")
                    $("#id_video").val(split_response[6])
                    $("#video-validate-response").html("<a href='"+split_response[6]+"'>"+split_response[6]+"</a>")
                    $("#image-validate-response").html("Please ignore this field..")
                    $("#audio-validate-response").html("Please ignore this field..")
    
                    $("input[name=blog-media]").removeAttr("checked")
                    $("#video").attr("checked","")
                }else if(split_response[6] == "" & split_response[5] == ""){
                    $("#id_audio").attr("disabled","")
                    $("#id_video").attr("disabled","")
                    
                    $("#id_image_blog").removeAttr("disabled")
                    $("#id_video").val("")
                    $("#image-validate-response").html("<a href='"+media_url+split_response[4]+"'>"+media_url+split_response[4]+"</a>")
                    $("#video-validate-response").html("Please ignore this field..")
                    $("#audio-validate-response").html("Please ignore this field..")
    
                    $("input[name=blog-media]").removeAttr("checked")
                    $("#photo").attr("checked","")
                }else if(split_response[6] == "" & split_response[4] == ""){
                    $("#id_image_blog").attr("disabled","")
                    $("#id_video").attr("disabled","")
    
                    $("#id_audio").removeAttr("disabled")
                    $("#id_video").val("")
    
                    $("#audio-validate-response").html("<a href='"+media_url+split_response[5]+"'>"+media_url+split_response[5]+"</a>")
                    $("#video-validate-response").html("Please ignore this field..")
                    $("#image-validate-response").html("Please ignore this field..")
    
                    
                    $("input[name=blog-media]").removeAttr("checked")
                    $("#audio").attr("checked","")
                }else{
                    $("#id_image_blog").attr("disabled","")
                    $("#id_video").attr("disabled","")
                    $("#id_video").val("")
    
                    $("#audio-validate-response").html("Please ignore this field..")
                    $("#video-validate-response").html("Please ignore this field..")
                    $("#image-validate-response").html("Please ignore this field..")
    
                    $("input[name=blog-media]").removeAttr("checked")
                    $("#none").attr("checked","")
    
                }
            }
        },error:function(){
            $("#id_title").val("")
            $("#id_tags").val("")
            
            // $("#id_discription_ifr").val("")
            tinyMCE.activeEditor.setContent(split_response[3]);

            $("#id_video").val("")

            $("#image-validate-response").html("Please ignore this field...")
            $("#audio-validate-response").html("Please ignore this field...")
            $("#video-validate-response").html("Please ignore this field...")

            $("input[name=blog-media]").removeAttr("checked")
            $("#none").attr("checked","")
        }
    })
}

$("#blog_id").on("blur",function(e){
    let bid = $("#blog_id").val()
    let murl = $("#media-url").val()
    edit_blog(murl,bid)
})

function delete_blog(blog_id){
    if(confirm("Do you want to delete?")){
        $(".blog-wrapper-"+blog_id).hide()
        $.ajax({
            method:'GET',
            url:'/blogs/delete-blog/',
            data:{
                'blog-id':blog_id,
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
            },success:function(res){
                $("#response-message").html(res)
                $("#response-message").attr('style','color:green;')
                $("#blog-message").modal("show")
            },
            error:function(res){
                $("#response-message").html("Opps ! Blog Deleting problem. Please Try again...")
                $("#response-message").attr('style','color:red;')
                $("#blog-message").modal("show")
                $("#blog-wrapper-"+blog_id).show()
            }
        })
    }
}


$("#delete-blog-from-form").on("click",function(e){
    let bid = $("#blog_id").val()
    if(bid == '' || bid == null){
        $("#response-message").html("Hey there ! Please put the Blog ID...")
        $("#response-message").attr('style','color:red;')
        $("#blog-message").modal("show")
        $("#blog-wrapper-"+blog_id).show()
    }else{
        delete_blog(bid)
    }
})

// TINYMCE API
// $('#content').tinymce().activeEditor.getContent() // overall html
// $('#content').tinymce().activeEditor.getContent({format : 'text'}) // overall text
// $('#content').tinymce().selection.getContent() // selected html
// $('#content').tinymce().selection.getContent({format : 'text'})) // selected text

$("#update-blog-post-form").on("submit",function(e){
    let bid = $("#blog_id").val()
    let title = $("#id_title").val()
    let tags = $("#id_tags").val()
    tinyMCE.triggerSave();
    let discription = $("#id_discription").tinymce().activeEditor.getContent()
    // console.log(discription)
    // return false
    let media = $("input[name=blog-media]:checked")
    if(bid==''||bid==null||title==''||title==null||tags==''||tags==null||discription==''||discription==null||media==''||media==null){
        $("#response-message").html("Opps ! All field required *")
        $("#response-message").attr('style','color:red;')
        $("#blog-message").modal("show")
        $("#blog-wrapper-"+blog_id).show()
        return false
    }else{
        return true
    }
})


function pickProductColor(color){
    
}



var p_qtty={
    "pid":0,
    "counter":0,
    "price":0.0,
    "delevery":0.0,
    "tax":0.0,
    "m_r_p":0.0,
    "total":0
}
function set_loaded_quantity(qty){
    p_qtty.counter=parseInt(qty)
    p_qtty.total=parseInt(qty)
}

function duplicateOrder(id,p_price,p_mrp,tax,p_delevery,deadline){
    // console.log('hello there....')
    if(p_qtty.counter==parseInt(deadline)){
        alert("Sorry ! Stock is out of reach.")
    }else{
        p_qtty.counter+=1
        p_qtty.total+=1
        p_qtty.pid=parseInt(id)
        p_qtty.price=parseFloat(p_price)
        p_qtty.tax=parseFloat(tax)
        p_qtty.m_r_p=parseFloat(p_mrp)
        p_qtty.delevery=parseFloat(p_delevery)
    
        let tax_per = p_qtty.tax/100
        let tax_amt = tax_per*p_qtty.price

        let shipping = p_qtty.price*p_qtty.counter
        let discount = parseFloat((p_mrp*p_qtty.counter)-shipping)

        let shipping_charge = p_qtty.delevery
        let total_tax = parseFloat(tax_amt*p_qtty.counter)

        let subtotal = parseFloat((p_qtty.m_r_p*p_qtty.counter)+shipping_charge+total_tax)
        let grandtotal = parseFloat(shipping+shipping_charge+total_tax)
        obj = new NumberConvertIntoComman()
        $("#shipping").html(obj.convert_data_into_comma(parseFloat(p_qtty.m_r_p*p_qtty.counter)))
        $("#shipping_charge").html(shipping_charge)
        $("#subtotal").html(obj.convert_data_into_comma(parseFloat(subtotal)))
        $("#id_tax").html(total_tax)
        $("#extra_discount").html(obj.convert_data_into_comma(parseFloat(discount)))
        $("#grandtotal").html(obj.convert_data_into_comma((grandtotal)))
        $.ajax({
            method:"GET",
            url:"/add-more-order/",
            data:{
                'pid':id,
                'p-counter':p_qtty.counter,
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
            },
            success:function(response){
                $(".order-products").append(response)
            }
        });
    }
}

// function tax_cal(amt,tax){
//     let per = tax/100;
//     let amt = per*amt;
//     return amt
// }

function removeOrder(cls,id,p_price,p_mrp,tax,p_delevery){
    if(p_qtty.total!=1){
        p_qtty.total-=1
        p_qtty.pid=parseInt(id)
        p_qtty.price=parseFloat(p_price)
        p_qtty.tax=parseFloat(tax)
        p_qtty.m_r_p=parseFloat(p_mrp)
        p_qtty.delevery=parseFloat(p_delevery)

        // p_qtty.counter-=1
        let subtotal = (p_qtty.m_r_p*p_qtty.total)+p_qtty.delevery+p_qtty.tax
        let grandtotal = (p_qtty.price*p_qtty.total)+p_qtty.delevery+p_qtty.tax
        let discount = (p_qtty.m_r_p-p_qtty.price)*p_qtty.total
        let tax_per = p_qtty.tax/100
        let tax_amt = (tax_per*p_qtty.price)*p_qtty.total
        $("#shipping").html(p_qtty.m_r_p*p_qtty.total)
        $("#shipping_charge").html(p_qtty.delevery)
        $("#id_tax").html(tax_amt)
        $("#extra_discount").html(discount)
        $("#subtotal").html(subtotal)
        $("#grandtotal").html(grandtotal)

        $(".product-wrapper-"+cls).remove()
    }else{
        alert("You can't remove all product !");
    }

}

function loadMyChart(){
    const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 21, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
}


// ORDER PLACING
$("#place_order").on("submit",function(e){
    let order_method = $("input[id=cash-on-delivery]:checked").val()
    let tac = $("input[id=term-and-condition]:checked").val()
    $("#product_quantity").attr("value",p_qtty.total)
    let pid = $("input[id='product_id']").val()
    if(order_method == undefined){
        alert("Order place method is required.")
        return false;
    }
    if(tac == undefined){
        alert("Please ensure that, You Checked Term & Service ?")
        return false;
    }
    if(pid == ''){
        alert("Don't try any, Every field is required.")
        return false;
    }

    $("#order-button").removeAttr('type')
    $("#order-button").html("Please wait...")
    $("#order-button").attr("style","cursor:no-drop;")
    return true
})


function track_order(){
    let order_id = $("#order-id").val().trim()
    if(order_id != ''){
        window.location.href=("/dashboard/dashManageOrder/"+order_id)
    }else{
        alert("Please Enter ORDER ID")
    }
}


$("#my-order-sort").on("change",function(e){
    let qty = $("#my-order-sort").val()
    $.ajax({
        method:'GET',
        url:'/dashboard/my-order-sort/',
        data:{
            'qty':qty,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },success:function(response){
            $("#my-orders").html(response)
        },error:function(response){
            alert("Somthing wen't wrong...")
        }
    })
})
