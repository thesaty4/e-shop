let is_imgChange=0;
$(function () {
    /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
    let val = $("#id_image").val()
    let blog_val = $("#id_image_blog").val()
    let val2 = $("#id_img_path").val()
    let val3 = $("#id_img_path1").val()
    if(val!=undefined) {
      $("#id_image").change(function () {
        if (this.files && this.files[0]) {
          var reader = new FileReader();
          reader.onload = function (e) {
            $("#image").attr("src", e.target.result);
            $("#modalCrop").modal("show");
          }
          reader.readAsDataURL(this.files[0]);
        }
      });
    } else if(val2!= undefined || val3!= undefined){
      $("#id_img_path").change(function () {
        if (this.files && this.files[0]) {
          var reader = new FileReader();
          reader.onload = function (e) {
            $("#image").attr("src", e.target.result);
            $("#modalCrop").modal("show");
          }
          reader.readAsDataURL(this.files[0]);
        }
      });
      $("#id_img_path1").change(function () {
        is_imgChange = 1;
        if (this.files && this.files[0]) {
          var reader = new FileReader();
          reader.onload = function (e) {
            $("#image").attr("src", e.target.result);
            $("#modalCrop").modal("show");
          }
          reader.readAsDataURL(this.files[0]);
        }
      });
    } else if(blog_val!=undefined){
      $("#id_image_blog").change(function () {
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
    if(val!=undefined || val2!=undefined || val3!=undefined || blog_val!=undefined){
      
        var $image = $("#image");
        var cropBoxData;
        var canvasData;
        var ourVal = 0
        var mcvwidth = 0
        var mcvheight = 0
        if(blog_val!=undefined) {
          ourVal=2
          mcvwidth = 600
          mcvheight = 900
        }else if(val==undefined){
          ourVal=1
          mcvwidth = 1600
          mcvheight = 1600
        }else{
          ourVal=1
          mcvwidth = 600
          mcvheight = 600
        }
        $("#modalCrop").on("shown.bs.modal", function () {
          $image.cropper({
            viewMode: 1,
            aspectRatio: ourVal/1,
            minCropBoxWidth: mcvwidth,
            minCropBoxHeight: mcvheight,
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
          if(is_imgChange == 1){
            $("#id_x1").val(cropData["x"]);
            $("#id_y1").val(cropData["y"]);
            $("#id_height1").val(cropData["height"]);
            $("#id_width1").val(cropData["width"]);
            $("#product-images1").submit()
            $("#croppingButton").html("<div>&#8987;Updating...</div>")
          }else{
            $("#id_x").val(cropData["x"]);
            $("#id_y").val(cropData["y"]);
            $("#id_height").val(cropData["height"]);
            $("#id_width").val(cropData["width"]);
            if(blog_val!=undefined){
              $("#cropMe").attr("data-dismiss","modal")
            }else{
              if(val==undefined) {
                $("#product-images").submit()
                $("#croppingButton").html("<div>&#8987;Updating...</div>")
              }else{
                $("#cropMe").attr("data-dismiss","modal")
              }
            }
          }
          
        });
    }
});