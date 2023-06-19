$(document).ready(function () {
    'use strict';
    let wishlist = (JSON.parse(localStorage.getItem('wishlist')) || []);
    const wishlistDOM = document.querySelector('.wishlist');

    const addTowishlistButtonsDOM = document.querySelectorAll('[data-action="ADD_TO_WISHLIST"]');

    var wishlisttotal = 0;
    var is_is_wpage = document.getElementById('is_wishlist_page');
    if (wishlist.length > 0) {
        // document.getElementById('empty_bag').style.display = 'none';
        wishlist.forEach(wishlistItem => {
            const product = wishlistItem;
            // var tablenew = document.getElementById('wishlisttable');

            if (!(document.getElementById('wishlist__item' + product.name))) {
                var txt = `<tr class="wishlist__item" id="wishlist__item${product.name}">
                            <td class="">
                              <div>
                                <a
                                  title="Remove this product"
                                  class="remove remove_from_wishlist"
                                  href="javascript:void(0)"
                                  data-action="REMOVE_WISH_ITEM"
                                  style="border-radius: 50px; background-color:#f5363e;color: white !important; "
                                  
                                  >×</a
                                >
                              </div>
                            </td>
                            <td class="product-thumbnail">
                              <a href="/product/${product.name}/">
                                <img
                                  width="180"
                                  height="180"
                                  alt=""
                                  class="wp-post-image"
                                  src="${product.image}"
                                />
                              </a>
                            </td>
                            <td class="product-name">
                              <a href="single-product-fullwidth.html"
                                >${product.title}
                              </a>
                            </td>
                            <td class="product-price">
                              <ins>
                                <span class="woocommerce-Price-amount amount">
                                  <span class="woocommerce-Price-currencySymbol"
                                    >tk</span
                                  >${product.price}</span
                                >
                              </ins>
<!--                              <del>-->
<!--                                <span class="woocommerce-Price-amount amount">-->
<!--                                  <span class="woocommerce-Price-currencySymbol"-->
<!--                                    >tk</span-->
<!--                                  >22999</span-->
<!--                                >-->
<!--                              </del>-->
                            </td>
<!--                            <td class="product-stock-status">-->
<!--                              <span class="wishlist-in-stock">In Stock</span>-->
<!--                            </td>-->
                            <td class="product-add-to-wishlist">
                            <p hidden class="wishlist__item__name" id="wishlist_item_name_${product.name}">${product.name}</p>
                            <div class="hover-area cartable">
                              <p hidden class="product__image_src">${product.image}</p>
                              <p hidden class="product__name">${product.name}</p>
                              <p hidden class="product__title">${product.title}</p>
                              <p hidden class="product__price">${product.price}</p>
                              <a class="button quick-btn" style="color:white" name="${product.name}">
                              Quick View
                              </a>
                                <a class="button add_to_cart_button button " style="color:white" name="btn${product.name}" data-action="ADD_TO_CART">Add to Cart</a>
                              </div>
                              
                            </td>
                          </tr>`;
                var tablenew = document.getElementById('wishlist_table');
                $(tablenew).find('tbody').append(txt);


                document.getElementById('wishlistcount').innerHTML = parseFloat(document.getElementById('wishlistcount').innerHTML) + 1;
                document.getElementById('mobilewishlistcount').innerHTML = parseFloat(document.getElementById('mobilewishlistcount').innerHTML) + 1;
                var wishlistItemsDOM = wishlistDOM.querySelectorAll('.wishlist__item');
                console.log(wishlistItemsDOM.length);
                // const wishlistItemsDOM = Array.prototype.slice.call(wishlistDOM.querySelectorAll('.wishlist__item')).concat(Array.prototype.slice.call(document.querySelectorAll(".product_in_wishlist")));
                // wishlistItemsDOM.forEach(wishlistItemDOM => {
                //     if (wishlistItemDOM.querySelector('.wishlist__item__name').innerText === product.name) {
                var is_wish_page = document.getElementById('is_wishlist_page');
                if (is_wish_page != null){

                    document.getElementById('wishlist__item' + product.name).querySelector('[data-action="REMOVE_WISH_ITEM"]').addEventListener('click', () => {
                        wishlist.forEach(wishlistItem => {
                            if (wishlistItem.name === product.name) {
                                // document.getElementById('titlerow' + wishlistItem.name).remove()
                                document.getElementById('wishlist__item' + wishlistItem.name).remove()
                                document.getElementById('wishlistcount').innerHTML = parseFloat(document.getElementById('wishlistcount').innerHTML) - 1;
                                document.getElementById('mobilewishlistcount').innerHTML = parseFloat(document.getElementById('mobilewishlistcount').innerHTML) - 1;
                                wishlist = wishlist.filter(wishlistItem => wishlistItem.name !== product.name);
                                localStorage.setItem('wishlist', JSON.stringify(wishlist));
                                updateWhenRemoveFromwishlist(wishlistItem);

                            }
                        });
                    });
                }

                //     }
                // });
                addTowishlistButtonsDOM.forEach(addTowishlistButtonDOM => {
                    const productDOM = addTowishlistButtonDOM.closest(".cartable");
                    var pronameDom = '';
                    try {
                        pronameDom = productDOM.querySelector('.product__name').innerText;
                    } catch (e) {
                        pronameDom = '';
                    }

                    if (pronameDom === wishlistItem.name) {
                        if (addTowishlistButtonDOM.tagName.toLowerCase() === 'a') {
                            addTowishlistButtonDOM.style.pointerEvents = "none";
                            addTowishlistButtonDOM.style.cursor="default";
                        }
                    }


                });
            }
        });
        // if (document.getElementById('wishlist_total').innerText >= 1000) {
        //     document.getElementById('deliverycharge').innerText = 40;
        // } else {
        //     document.getElementById('deliverycharge').innerText = 60;
        // }
    }

    addTowishlistButtonsDOM.forEach(addTowishlistButtonDOM => {
        addTowishlistButtonDOM.addEventListener('click', () => {
                const productDOM = addTowishlistButtonDOM.closest(".product");
                console.log(productDOM)
                const product = {
                    image: productDOM.querySelector('.product__image_src').innerText,
                    name: productDOM.querySelector('.product__name').innerText,
                    title: productDOM.querySelector('.product__title').innerText,
                    price: productDOM.querySelector('.product__price').innerText,
                    quantity: 1,
                };
                console.log((product));
                const isInwishlist = (wishlist.filter(wishlistItem => (wishlistItem.name === product.name)).length > 0);
                if (!isInwishlist && !(document.getElementById('wishlist__item' + product.name))) {

                    wishlist.push(product);
                    document.getElementById('wishlistcount').innerHTML = parseFloat(document.getElementById('wishlistcount').innerHTML) + 1;
                    document.getElementById('mobilewishlistcount').innerHTML = parseFloat(document.getElementById('mobilewishlistcount').innerHTML) + 1;
                    localStorage.setItem('wishlist', JSON.stringify(wishlist));
                    updateQuantityOnButton(product);
                    const wishlistItemsDOM = Array.prototype.slice.call(wishlistDOM.querySelectorAll('.wishlist__item')).concat(Array.prototype.slice.call(document.querySelectorAll(".product_in_wishlist")));
                    wishlistItemsDOM.forEach(wishlistItemDOM => {
                        if (wishlistItemDOM.querySelector('.wishlist__item__name').innerText === product.name) {


                        }
                    });
                }
            }
        );
    });
});

function updateQuantityOnButton(product) {

    // try {
    //     var btn = document.getElementsByName('btn' + product.name);
    //     btn.forEach(a => {
    //         // aTODO: ADD ITEM COUNT BEFORE IN wishlist
    //         if (a.tagName.toLowerCase() === 'a') {
    //             a.style.pointerEvents = "none";
    //             a.style.cursor = "default";
    //         }
    //
    //     });
    // } catch (e) {
    //     console.log(e);
    // }
}

function updateWhenRemoveFromwishlist(product) {
    try {
        // try {
        //     var el = document.getElementById('overlay_second' + product.name);
        //     var el1 = el.querySelector('[data-action="DECREASE_ITEM"]');
        //     elClone = el1.cloneNode(true);
        //     el1.parentNode.replaceChild(elClone, el1);
        //     var el2 = el.querySelector('[data-action="INCREASE_ITEM"]');
        //     elClone = el2.cloneNode(true);
        //     el2.parentNode.replaceChild(elClone, el2);
        // } catch (e) {
        //
        // }
        var btn = document.getElementsByName('btn' + product.name);

        btn.forEach(a => {
            if (a.tagName === 'A') {
                a.style.pointerEvents = "auto";
                a.style.cursor = "pointer";
            }
            // else if (a.tagName === 'A') {
            //     document.getElementById("overlay_first" + product.name).style.display = 'block';
            //     document.getElementById("overlay_second" + product.name).style.display = 'none';
            //     document.getElementById("overlay_second_num_of_items" + product.name).innerText = "ADD TO wishlist";
            // }
        });
        let wishlist = (JSON.parse(localStorage.getItem('wishlist')) || []);
        // if (wishlist.length == 0) {
        //     document.getElementById('empty_bag').style.display = 'block';
        // } else {
        //     document.getElementById('empty_bag').style.display = 'none';
        // }


    } catch (e) {
        alert(e);
    }
}