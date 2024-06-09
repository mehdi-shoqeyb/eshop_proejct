function filterProducts(){
    const filterPrice = $('#sl2').val();
    const start_price = filterPrice.split(',')[0];
    const end_price = filterPrice.split(',')[1];


    $('#start_price').val(start_price);
    $('#end_price').val(end_price);
    $('#filter_form').submit();
}

function fillPage(page){
    $('#page').val(page);
    $('#filter_form').submit();
}

function showLargeImage(imageSrc){
    $('#main_image').attr('src',imageSrc);
    $('#show_large_image_modal').attr('href',imageSrc);
}


function addProductToOrder(productId){
    const productCount = $('#product-count').val();
    $.get('/order/add-to-order?product_id=' + productId + '&count=' + productCount).then(res => {
        Swal.fire({
          title: 'اعلان?',
          text: res.text,
          icon: res.icon,
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: res.confirmButtonText,
          cancelButtonText: 'لغو'
        }).then((result) => {
            if (result.isConfirmed && res.status === 'not_auth') {
                window.location.href = '/login';
            }
        });
    });

}

function removeOrderDetail(detailId){
    $.get('/user/remove-order-detail?detail_id=' + detailId).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}

function changeOrderDetailCount(detailId, state){
    $.get('/user/change-order-detail?detail_id=' + detailId + '&state=' + state).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}
