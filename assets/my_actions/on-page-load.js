function add_host_id(hostname_ip,product_id,user_id){
    // console.log(hostname_ip)
    $.ajax({
        method:'POST',
        url:'/product-viewer/',
        data:{
            'hostname-ip':hostname_ip,
            'product-id':product_id,
            'user-id':user_id,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        }
    })
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

function defaultMessages(msg){
    if(msg==''||msg==null){
        $("#blog-message").modal("hide")
        // $("#response-message").html(msg)
    }else{
        $("#blog-message").modal("show")
        $("#response-message").html(msg)

    }
}



function load_top_sells_graph(products, sells, type){
    let label = products.split(",")
    let sell = sells.split(",")
    let data = []
    for(i=0;i<(sell.length)-1;i++){
        data.push(parseInt(sell[i]))
    }

    // console.log(products)
    // console.log(data)
    
    const ctx = document.getElementById('top_sells_graph').getContext('2d');
const myChart = new Chart(ctx, {
    // type: 'radar',
    type: 'pie',
    // type: 'bubble',
    // type: 'scatter',
    // type: 'doughnut',
    // type: 'bar',
    data: {
        labels: label,
        datasets: [{
            label: '# Total Selled Product',
            data: data,
            backgroundColor: [
                'rgba(225, 99, 132, 2)',
                'rgba(54, 162, 235, 2)',
                // 'rgba(75, 192, 192, 2)',
                // 'rgba(255, 206, 86, 2)',
                // 'rgba(153, 102, 255, 2)',

                'rgba(199, 199, 132, 2)',
                'rgba(40, 162, 22, 2)',
                'rgba(44, 33, 86, 2)',
                'rgba(29, 192, 192, 2)',
                'rgba(50, 102, 33, 2)',
                'rgba(233, 223, 21, 2)'
            ],
            borderColor: [
                'rgba(225, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                // 'rgba(75, 192, 192, 1)',
                // 'rgba(255, 206, 86, 1)',
                // 'rgba(153, 102, 255, 1)',
                'rgba(199, 199, 132, 1)',
                'rgba(40, 162, 22, 1)',
                'rgba(44, 33, 86, 1)',
                'rgba(29, 192, 192, 1)',
                'rgba(50, 102, 33, 1)',
                'rgba(233, 223, 21, 1)'
            ],
            borderWidth: 2
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


function load_hold_graph(process,shipped,deliverd,cancel,returns,total_sells){
    const ctx = document.getElementById('hold_delivery_graph').getContext('2d');
    const myChart = new Chart(ctx, {
    // type: 'radar',
    // type: 'pie',
    // type: 'scatter',
    // type: 'doughnut',
    type: 'bar',
    data: {
        labels: ['Processing','Shipped','Deliverd',"Cancelled","Returns"],
        datasets: [{
            label: '# Total '+total_sells+" Selled",
            data: [process,shipped,deliverd,cancel,returns],
            backgroundColor: [
                'rgba(225, 99, 132, 2)',
                'rgba(54, 162, 235, 2)',
                'rgba(255, 206, 86, 2)',
                'rgba(75, 192, 192, 2)',
                'rgba(153, 102, 255, 2)',
                'rgba(255, 159, 64, 2)'
            ],
            borderColor: [
                'rgba(225, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 2
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

function remaining_and_selled(selled,remaining){
    const ctx = document.getElementById('remaining_and_selled').getContext('2d');
    const myChart = new Chart(ctx, {
    // type: 'radar',
    // type: 'pie',
    // type: 'scatter',
    type: 'doughnut',
    // type: 'bar',
    data: {
        labels: ['Total Selled','Remaining Items'],
        datasets: [{
            label: '# Total '+selled+" Selled",
            data: [remaining,selled],
            backgroundColor: [
                'rgba(153, 99, 255, 2)',
                'rgba(255, 159, 64, 2)'
            ],
            borderColor: [
                'rgba(153, 99, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 2
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

function returns_analysis(deliverd,returns){
    const ctx = document.getElementById('returns_analysis_canvas').getContext('2d');
    const myChart = new Chart(ctx, {
    // type: 'radar',
    type: 'polarArea',

    // type: 'scatter',
    // type: 'doughnut',
    // type: 'bar',
    data: {
        labels: ['Total Accepted','Returns Items'],
        datasets: [{
            label: '# Total Selled',
            data: [deliverd,returns],
            backgroundColor: [
                'rgba(153, 153, 255, 1)',
                'red'
            ],
            borderColor: [
                'rgba(153, 153, 255, 6)',
                'red'
            ],
            borderWidth: 2,
            hoverOffset: 8
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
function returns_analysis_2(deliverd,returns){
    const ctx = document.getElementById('returns_analysis_canvas_2').getContext('2d');
    const myChart = new Chart(ctx, {
    // type: 'radar',
    // type: 'pie',
    // type: 'scatter',
    // type: 'line',
    // type: 'doughnut',
    type: 'bar',
    data: {
        labels: ['Total Accepted','Returns Items'],
        datasets: [{
            label: '# Total Selled',
            data: [deliverd,returns],
            backgroundColor: [
                'green',
                'red'
            ],
            borderColor: [
                'green',
                'red'
            ],
            borderWidth: 2
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


function products_graph(deliverd,returns){
    const ctx = document.getElementById('product-graph').getContext('2d');
    const myChart = new Chart(ctx, {
    // type: 'radar',
    // type: 'pie',
    // type: 'scatter',
    // type: 'line',
    // type: 'doughnut',
    type: 'bar',
    data: {
        labels: ['Total Accepted','Returns Items'],
        datasets: [{
            label: '# Total Selled',
            data: [deliverd,returns],
            backgroundColor: [
                'green',
                'red'
            ],
            borderColor: [
                'green',
                'red'
            ],
            borderWidth: 2
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
