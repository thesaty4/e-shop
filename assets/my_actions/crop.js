$(function () {
    /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
    let val = $("#id_profile_pic").val()
    let val2 = $("#upload_image").val()
    if(val!=undefined) {
      $("#id_profile_pic").change(function () {
        if (this.files && this.files[0]) {
          var reader = new FileReader();
          reader.onload = function (e) {
            $("#image").attr("src", e.target.result);
            $("#modalCrop").modal("show");
          }
          reader.readAsDataURL(this.files[0]);
        }
      });
    } else if(val2!= undefined){
      $("#upload_image").change(function () {
      
        if (this.files && this.files[0]) {
          var reader = new FileReader();
          reader.onload = function (e) {
            $("#image").attr("src", e.target.result);
            $("#modalCrop").modal("show");
          }
          reader.readAsDataURL(this.files[0]);
        }
      });
    }

    /* SCRIPTS TO HANDLE THE CROPPER BOX */
    if(val!=undefined || val2!=undefined){
      
        var $image = $("#image");
        var cropBoxData;
        var canvasData;
        $("#modalCrop").on("shown.bs.modal", function () {
          $image.cropper({
            viewMode: 1,
            aspectRatio: 1/1,
            minCropBoxWidth: 200,
            minCropBoxHeight: 200,
            ready: function () {
              $image.cropper("setCanvasData", canvasData);
              $image.cropper("setCropBoxData", cropBoxData);
            }
            
          });
          
        }).on("hidden.bs.modal", function () {
          cropBoxData = $image.cropper("getCropBoxData");
          canvasData = $image.cropper("getCanvasData");
          $image.cropper("destroy");
        });

        $(".js-zoom-in").click(function () {
          $image.cropper("zoom", 0.1);
        });

        $(".js-zoom-out").click(function () {
          $image.cropper("zoom", -0.1);
        });

        /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
        $(".js-crop-and-upload").click(function () {
          //Processing Bar
          var cropData = $image.cropper("getData");
          $("#id_x").val(cropData["x"]);
          $("#id_y").val(cropData["y"]);
          $("#id_height").val(cropData["height"]);
          $("#id_width").val(cropData["width"]);
          if(val==undefined) {
            $("#updateProfilePic").submit()
            $("#croppingButton").html("<div>&#8987;Updating...</div>")
          }else{
            //console.log("#Cropped Data saved, The data is : ")
            //console.log(cropData);
            //$("#formUpload").submit(); <------ You can upload data too.
            
            let width= document.getElementById("image").width
            let height= document.getElementById("image").height
            let img= document.getElementById("image")
            // Creating Image
            let imgData = getBase64Image(img,width,height)
            bannerImg = document.getElementById('uploaded_image');
            bannerImg.src = "data:image/png;base64," + imgData;
            $("#cropMe").attr("data-dismiss","modal")
          }
        });
    }
});
      // Function for creating image base64Formate
      function getBase64Image(img,imgwidth,imgheight) {
        var canvas = document.createElement("canvas");
        canvas.width = imgwidth
        canvas.height = imgheight

        var ctx = canvas.getContext("2d")
        ctx.drawImage(img,0,0)

        var dataURL = canvas.toDataURL("image/png")
        return dataURL.replace(/^data:image\/(png|jpg);base64,/, "")
    }