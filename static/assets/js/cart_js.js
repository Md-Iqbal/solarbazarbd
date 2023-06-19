$(document).ready(function () {
    'use strict';
    let cart = (JSON.parse(localStorage.getItem('cart')) || []);
    const cartDOM = document.querySelector('.cart');

    const addToCartButtonsDOM = document.querySelectorAll('[data-action="ADD_TO_CART"]');

    var carttotal = 0;
    if (cart.length > 0) {
        // document.getElementById('empty_bag').style.display = 'none';
        cart.forEach(cartItem => {
            const product = cartItem;
            var itemtotal = product.price * product.quantity;
            // var tablenew = document.getElementById('carttable');
            if (!(document.getElementById('cart__item' + product.name))) {
                var txt = `<li class="woocommerce-mini-cart-item mini_cart_item cart__item" id="cart__item${product.name}">
                                <p hidden class="cart__item__name" id="cart_item_name_${product.name}">${product.name}</p>
                                <a
                                        href="javascript:void(0)"
                                        data-action="REMOVE_ITEM"
                                        class="remove"
                                        aria-label="Remove this item"
                                        data-product_id="65"
                                        data-product_sku=""
                                        id="removeitem${product.name}"
                                >×</a
                                >
                                <a href="javascript:void(0)">
                                    <img
                                            class="attachment-shop_thumbnail size-shop_thumbnail wp-post-image cart__item__image" 
                                            id="cart_item_image_${product.name}" 
                                            src="${product.image}" 
                                            alt="${product.image}"
                                    />${product.title}&nbsp;
                                </a>
<!--                                <span-->
<!--                                        class="quantity"-->
<!--                                >1 ×-->
                               <button class="btn  btn-small${(product.quantity === 1 ? ' btn--danger' : '')}" style="padding: 0px 5px;background-color: whitesmoke " data-action="DECREASE_ITEM">&minus;</button>
                               <span class="cart__item__quantity " id="cart_item_quantity_${product.name}">${product.quantity}</span >&nbsp;
                               <button class="btn  btn-small" style="padding: 0px 5px; background-color: whitesmoke" data-action="INCREASE_ITEM" >&plus;</button >&nbsp;
                                &nbsp;
                              <span class="woocommerce-Price-amount amount">
                                <span
		                                class="woocommerce-Price-currencySymbol"
                                >৳</span>
                                <span class="cart__item__price" id="cart_item_price_${product.name}">${product.price * product.quantity}</span>
                            </span>
											</li>`;
                $('#cartlist').append(txt);


                var is_cart_page = document.getElementById('cart_page');
                if (is_cart_page !== null) {
                    var trow = `<tr class="cart__item" id="cart__item${product.name}">
                                <td class="product-remove">

                                  <a class="remove" 
                                    href="javascript:void(0)"
                                    data-action="REMOVE_ITEM"
                                    id="removeitem${product.name}"
                                  >×</a>
                                </td>
                                <td class="product-thumbnail">
                                  <a href="javascript:void(0)">
                                  <p hidden class="cart__item__name" id="cart_item_name_${product.name}">${product.name}</p>
                                    <img
                                      width="180"
                                      height="180"
                                      alt=""
                                      class="wp-post-image"
                                      src=""
                                    />
                                  </a>
                                </td>
                                <td data-title="Product" class="product-name">
                                  <div class="media cart-item-product-detail">
                                    <a href="#">
                                      <img
                                        width="180"
                                        height="180"
                                        alt=""
                                        class="wp-post-image"
                                        id="cart_item_image_${product.name}" 
                                        src="${product.image}" 
                                      />
                                    </a>
                                    <div class="media-body align-self-center">
                                      <a href="#"
                                        >${product.title}</a
                                      >
                                    </div>
                                  </div>
                                </td>
                                <td data-title="Price" class="product-price">
                                  <span class="woocommerce-Price-amount amount">
                                    <span
                                      class="woocommerce-Price-currencySymbol"
                                      >৳</span
                                    >${product.price}
                                  </span>
                                </td>
                                <td
                                  class="product-quantity"
                                  data-title="Quantity"
                                >
                                <p hidden class="cart__item__name" id="cart_item_name_${product.name}">${product.name}</p>
                                  <div class="quantity">
                                    <label for="quantity-input-1"
                                      >Quantity</label
                                    >
<!--                                    <input-->
<!--                                      id="quantity-input-1"-->
<!--                                      type="number"-->
<!--                                      name="cart[e2230b853516e7b05d79744fbd4c9c13][qty]"-->
<!--                                      value="1"-->
<!--                                      title="Qty"-->
<!--                                      class="input-text qty text"-->
<!--                                      size="4"-->
<!--                                    />-->
                                   <button class="btn  btn-smal" style="padding: 0px 5px;background-color: whitesmoke " data-action="DECREASE_ITEM">&minus;</button>
                                   <span class="cart__item__quantity " id="cart_item_quantity_${product.name}">${product.quantity}</span >&nbsp;
                                   <button class="btn  btn-small" style="padding: 0px 5px; background-color: whitesmoke" data-action="INCREASE_ITEM" >&plus;</button >&nbsp;
                                    &nbsp;
                                  </div>
                                </td>
                                <td data-title="Total" class="product-subtotal">
                                  <span class="woocommerce-Price-amount amount">
                                    <span
                                      class="woocommerce-Price-currencySymbol"
                                      >৳</span
                                    >${parseFloat(product.price) * parseFloat(product.quantity)}
                                  </span>
                                  <a
                                    title="Remove this item"
                                    class="remove"
                                    href="#"
                                    >×</a
                                  >
                                </td>
                              </tr>`

                    var tablenew = document.getElementById('carttable');
                    $(tablenew).find('tbody').append(trow);
                }


                carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
                // document.getElementById('main_cart_total').innerHTML = carttotal + parseFloat(product.price * product.quantity);
                document.getElementById('cart_total').innerHTML = carttotal + parseFloat(product.price * product.quantity);
                document.getElementById('floatcarttotal').innerHTML = carttotal + parseFloat(product.price * product.quantity);
                document.getElementById('floatingtotalitems').innerHTML = parseFloat(document.getElementById('floatingtotalitems').innerHTML) + 1;
                document.getElementById('mobiletotalitems').innerHTML = parseFloat(document.getElementById('mobiletotalitems').innerHTML) + 1;
                // document.getElementById('cartheadingtotalitems').innerHTML = parseFloat(document.getElementById('cartheadingtotalitems').innerHTML) + 1;

                // var cartItemsDOM = Array.prototype.slice.call(cartDOM[0].querySelectorAll('.cart__item')).concat(Array.prototype.slice.call(cartDOM[1].querySelectorAll('.cart__item')));
                var cartItemsDOM = cartDOM.querySelectorAll('.cart__item');
                // console.log(cartItemsDOM.length);
                // const cartItemsDOM = Array.prototype.slice.call(cartDOM.querySelectorAll('.cart__item')).concat(Array.prototype.slice.call(document.querySelectorAll(".product_in_cart")));
                cartItemsDOM.forEach(cartItemDOM => {
                    if (cartItemDOM.querySelector('.cart__item__name').innerText === product.name) {
                        cartItemDOM.querySelector('[data-action="INCREASE_ITEM"]').addEventListener('click', () => {
                            cart.forEach(cartItem => {
                                if (cartItem.name === product.name) {
                                    try {
                                        document.getElementById("cart_item_quantity_" + product.name).innerText = ++cartItem.quantity;
                                        document.getElementById("cart_item_price_" + product.name).innerText = (document.getElementById("cart_item_quantity_" + product.name).innerText) * cartItem.price;
                                        carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
                                        document.getElementById('cart_total').innerHTML = carttotal + parseFloat(product.price);
                                        document.getElementById('floatcarttotal').innerHTML = carttotal + parseFloat(product.price);
                                        localStorage.setItem('cart', JSON.stringify(cart));
                                        // show increased item on button
                                        updateQuantityOnButton(product);
                                        // if (document.getElementById('cart_total').innerText >= 1000) {
                                        //     document.getElementById('deliverycharge').innerText = 40;
                                        // } else {
                                        //     document.getElementById('deliverycharge').innerText = 60;
                                        // }

                                    } catch (e) {
                                        console.log(e);
                                    }
                                }
                            });
                        });

                        cartItemDOM.querySelector('[data-action="DECREASE_ITEM"]').addEventListener('click', () => {
                            cart.forEach(cartItem => {
                                if (cartItem.name === product.name) {
                                    if (cartItem.quantity > 1) {
                                        document.getElementById("cart_item_quantity_" + product.name).innerText = --cartItem.quantity;
                                        document.getElementById("cart_item_price_" + product.name).innerText = (document.getElementById("cart_item_quantity_" + product.name).innerText) * cartItem.price
                                        carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
                                        document.getElementById('cart_total').innerHTML = carttotal - parseFloat(product.price);
                                        document.getElementById('floatcarttotal').innerHTML = carttotal - parseFloat(product.price);
                                        localStorage.setItem('cart', JSON.stringify(cart));
                                        updateQuantityOnButton(cartItem);
                                        // if (document.getElementById('cart_total').innerText >= 1000) {
                                        //     document.getElementById('deliverycharge').innerText = 40;
                                        // } else {
                                        //     document.getElementById('deliverycharge').innerText = 60;
                                        // }
                                    } else {
                                        try {
                                            // document.getElementById('titlerow' + cartItem.name).remove()
                                            document.getElementById('cart__item' + cartItem.name).remove();
                                            cart = cart.filter(cartItem => cartItem.name !== product.name);
                                            carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
                                            document.getElementById('cart_total').innerHTML = carttotal - parseFloat(product.price);
                                            document.getElementById('floatcarttotal').innerHTML = carttotal - parseFloat(product.price);
                                            document.getElementById('floatingtotalitems').innerHTML = parseFloat(document.getElementById('floatingtotalitems').innerHTML) - 1;
                                            document.getElementById('mobiletotalitems').innerHTML = parseFloat(document.getElementById('mobiletotalitems').innerHTML) - 1;
                                            // document.getElementById('cartheadingtotalitems').innerHTML = parseFloat(document.getElementById('cartheadingtotalitems').innerHTML) - 1;
                                            localStorage.setItem('cart', JSON.stringify(cart));
                                            updateWhenRemoveFromCart(cartItem);
                                            // if (document.getElementById('cart_total').innerText >= 1000) {
                                            //     document.getElementById('deliverycharge').innerText = 40;
                                            // } else {
                                            //     document.getElementById('deliverycharge').innerText = 60;
                                            // }
                                        } catch (e) {
                                            console.log(e);

                                        }
                                    }


                                }
                            });
                        });
                        document.getElementById('cart__item' + product.name).querySelector('[data-action="REMOVE_ITEM"]').addEventListener('click', () => {
                            cart.forEach(cartItem => {
                                if (cartItem.name === product.name) {
                                    cartItemDOM.classList.add('cart__item--removed');
                                    // document.getElementById('titlerow' + cartItem.name).remove()
                                    document.getElementById('cart__item' + cartItem.name).remove()
                                    carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
                                    var floatcarttotal = carttotal - parseFloat(product.price) * cartItem.quantity
                                    if (floatcarttotal > 0) {
                                        document.getElementById('cart_total').innerHTML = floatcarttotal;
                                        document.getElementById('floatcarttotal').innerHTML = floatcarttotal;
                                    } else {
                                        document.getElementById('floatcarttotal').innerHTML = 0;
                                        document.getElementById('cart_total').innerHTML = 0
                                    }

                                    document.getElementById('floatingtotalitems').innerHTML = parseFloat(document.getElementById('floatingtotalitems').innerHTML) - 1;
                                    document.getElementById('mobiletotalitems').innerHTML = parseFloat(document.getElementById('mobiletotalitems').innerHTML) - 1;
                                    // document.getElementById('cartheadingtotalitems').innerHTML = parseFloat(document.getElementById('cartheadingtotalitems').innerHTML) - 1;
                                    cart = cart.filter(cartItem => cartItem.name !== product.name);
                                    localStorage.setItem('cart', JSON.stringify(cart));
                                    updateWhenRemoveFromCart(cartItem);
                                    // if (document.getElementById('cart_total').innerText >= 1000) {
                                    //     document.getElementById('deliverycharge').innerText = 40;
                                    // } else {
                                    //     document.getElementById('deliverycharge').innerText = 60;
                                    // }
                                }
                            });
                        });

                    }
                });
                addToCartButtonsDOM.forEach(addToCartButtonDOM => {
                    const productDOM = addToCartButtonDOM.closest(".cartable");
                    var pronameDom = '';
                    try {
                        pronameDom = productDOM.querySelector('.product__name').innerText;
                    } catch (e) {
                        pronameDom = '';
                    }

                    if (pronameDom === cartItem.name) {
                        if (addToCartButtonDOM.tagName.toLowerCase() === 'a') {
                            addToCartButtonDOM.innerText = `${cartItem.quantity} In Cart`;
                            addToCartButtonDOM.style.pointerEvents = "none";
                        }

                        // document.getElementById("overlay_first" + product.name).style.display = 'none';
                        // document.getElementById("overlay_second" + product.name).style.display = 'block'
                        // document.getElementById("overlay_second_num_of_items" + product.name).innerText = product.quantity + " IN CART"
                    }


                });
            }
        });
        // if (document.getElementById('cart_total').innerText >= 1000) {
        //     document.getElementById('deliverycharge').innerText = 40;
        // } else {
        //     document.getElementById('deliverycharge').innerText = 60;
        // }
    }

    addToCartButtonsDOM.forEach(addToCartButtonDOM => {
        addToCartButtonDOM.addEventListener('click', () => {
                const productDOM = addToCartButtonDOM.closest(".cartable");
                const product = {
                    image: productDOM.querySelector('.product__image_src').innerText,
                    name: productDOM.querySelector('.product__name').innerText,
                    title: productDOM.querySelector('.product__title').innerText,
                    price: productDOM.querySelector('.product__price').innerText,
                    quantity: 1,
                };
                console.log((product));
                const isInCart = (cart.filter(cartItem => (cartItem.name === product.name)).length > 0);
                var ul = document.getElementById('cartlist');
                // {#cartDOM.insertAdjacentHTML('beforeend',"<img src='${product.image}'>" );#}

                if (!isInCart && !(document.getElementById('cart__item' + product.name))) {
                    var txt = `<li class="woocommerce-mini-cart-item mini_cart_item cart__item" id="cart__item${product.name}">
                                <p hidden class="cart__item__name" id="cart_item_name_${product.name}">${product.name}</p>
                                <a
                                        href="javascript:void(0)"
                                        data-action="REMOVE_ITEM"
                                        class="remove"
                                        aria-label="Remove this item"
                                        data-product_id="65"
                                        data-product_sku=""
                                        id="removeitem${product.name}"
                                >×</a
                                >
                                <a href="javascript:void(0)">
                                    <img
                                            class="attachment-shop_thumbnail size-shop_thumbnail wp-post-image cart__item__image" 
                                            id="cart_item_image_${product.name}" 
                                            src="${product.image}" 
                                            alt="${product.image}"
                                    />${product.title}&nbsp;
                                </a>
<!--                                <span-->
<!--                                        class="quantity"-->
<!--                                >1 ×-->
                               <button class="btn  btn-small${(product.quantity === 1 ? ' btn--danger' : '')}" style="padding: 0px 5px;background-color: whitesmoke " data-action="DECREASE_ITEM">&minus;</button>
                               <span class="cart__item__quantity " id="cart_item_quantity_${product.name}">${product.quantity}</span >&nbsp;
                               <button class="btn  btn-small" style="padding: 0px 5px; background-color: whitesmoke" data-action="INCREASE_ITEM" >&plus;</button >&nbsp;
                                &nbsp;
                              <span class="woocommerce-Price-amount amount">
                                <span
		                                class="woocommerce-Price-currencySymbol"
                                >৳</span>
                                <span class="cart__item__price" id="cart_item_price_${product.name}">${product.price * product.quantity}</span>
                            </span>
											</li>`;

                    // + `
                    //
                    //
                    //
                    //
                    //
                    //
                    //     <tr id="titlerow${product.name}"  style="width: 300px !important; " >
                    //         <td colspan="3" style=" padding-bottom: 0px; width: 300px !important;" >${product.title}
                    //             <a style="float: right" id="removeitem${product.name}">
                    //                 <i class="fas fa-trash"
                    //                    style="padding-right: 0px !important; font-size: 15px !important; color:#cd0d0d; " ></i >
                    //             </a >
                    //         </td >
                    //     </tr >
                    //     <tr class="cart__item" style="border-bottom:1pt solid lightgray;" id="bodyrow${product.name}">
                    //         <th scope="col" ><img style="width: 50px;" class="cart__item__image" id="cart_item_image_${product.name}" src="${product.image}" alt="${product.image}" ></th >
                    //         <th scope="col" style="padding-bottom: 15px; text-align: center">
                    //             <button class="btn  btn-small" style="padding: 0px 5px; background-color: #c3e6cb" data-action="INCREASE_ITEM" >&plus;</button >
                    //             <span class="cart__item__quantity font-weight-bold" id="cart_item_quantity_${product.name}">${product.quantity}</span >
                    //             <button class="btn  btn-small${(product.quantity === 1 ? ' btn--danger' : '')}" style="padding: 0px 5px;background-color: #fadc8c " data-action="DECREASE_ITEM">&minus;</button>
                    //             <p hidden class="cart__item__name" id="cart_item_name_${product.name}">${product.name}</p>
                    //         </th >
                    //         <th scope="col" style="text-align: right; padding-bottom: 22px">৳. <span class="cart__item__price" id="cart_item_price_${product.name}">${product.price}</span></th >
                    //     </tr >
                    //   `;
                    $('#cartlist').append(txt);
                    /*
                    EXPAND THE CART WHEN FIRST TIME IS ADDED
                    AT THIS MOMENT IT OPENS WHEN THE THE PRODUCT COUNT IS ZERO
                    IF YOU REMOVE ALL THE OTHER PRODUCTS FROM THE LIST AND THEN ADD
                    AGAIN, IT SHOULD WORK THE SAME
                    */
                    // if (cart.length === 0) {
                    //     document.getElementById('empty_bag').style.display = 'none';
                    //     sidebarOPen();
                    //
                    // }
                    cart.push(product);
                    carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
                    document.getElementById('cart_total').innerHTML = carttotal + parseFloat(product.price * product.quantity);
                    document.getElementById('floatcarttotal').innerHTML = carttotal + parseFloat(product.price * product.quantity);
                    document.getElementById('floatingtotalitems').innerHTML = parseFloat(document.getElementById('floatingtotalitems').innerHTML) + 1;
                    document.getElementById('mobiletotalitems').innerHTML = parseFloat(document.getElementById('mobiletotalitems').innerHTML) + 1;
                    // document.getElementById('cartheadingtotalitems').innerHTML = parseFloat(document.getElementById('cartheadingtotalitems').innerHTML) + 1;
                    localStorage.setItem('cart', JSON.stringify(cart));
                    updateQuantityOnButton(product);
                    // var btn = document.getElementsByName('btn' + product.name);
                    // try {
                    //     // var btn = document.getElementsByName('btn' + product.name);
                    //     btn.forEach(a => {
                    //         // aTODO: ADD ITEM COUNT BEFORE IN CART
                    //         if (a.tagName === 'a') {
                    //             a.innerText = `${product.quantity} In Cart`;
                    //             addToCartButtonDOM.style.pointerEvents = "none";
                    //         }
                    //         // else if (a.tagName === 'A') {
                    //         //     document.getElementById("overlay_first" + product.name).style.display = 'none';
                    //         //     document.getElementById("overlay_second" + product.name).style.display = 'block'
                    //         //     document.getElementById("overlay_second_num_of_items" + product.name).innerText = product.quantity + " IN CART"
                    //         // }
                    //
                    //     });
                    // } catch (e) {
                    //     console.log(e);
                    // }
                    // if (document.getElementById('cart_total').innerText >= 1000) {
                    //     document.getElementById('deliverycharge').innerText = 40;
                    // } else {
                    //     document.getElementById('deliverycharge').innerText = 60;
                    // }

                    // {#const cartItemsDOM = cartDOM.querySelectorAll('.cart__item');#}
                    const cartItemsDOM = Array.prototype.slice.call(cartDOM.querySelectorAll('.cart__item')).concat(Array.prototype.slice.call(document.querySelectorAll(".product_in_cart")));
                    cartItemsDOM.forEach(cartItemDOM => {
                        if (cartItemDOM.querySelector('.cart__item__name').innerText === product.name) {

                            cartItemDOM.querySelector('[data-action="INCREASE_ITEM"]').addEventListener('click', () => {
                                cart.forEach(cartItem => {
                                    if (cartItem.name === product.name) {
                                        document.getElementById("cart_item_quantity_" + product.name).innerText = ++cartItem.quantity;
                                        document.getElementById("cart_item_price_" + product.name).innerText = (document.getElementById("cart_item_quantity_" + product.name).innerText) * cartItem.price;
                                        carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
                                        document.getElementById('cart_total').innerHTML = carttotal + parseFloat(product.price);
                                        document.getElementById('floatcarttotal').innerHTML = carttotal + parseFloat(product.price);
                                        localStorage.setItem('cart', JSON.stringify(cart));
                                        // show increased item on button
                                        localStorage.setItem('cart', JSON.stringify(cart));
                                        // show increased item on button
                                        updateQuantityOnButton(product);
                                        // if (document.getElementById('cart_total').innerText >= 1000) {
                                        //     document.getElementById('deliverycharge').innerText = 40;
                                        // } else {
                                        //     document.getElementById('deliverycharge').innerText = 60;
                                        // }

                                    }
                                });
                            });

                            cartItemDOM.querySelector('[data-action="DECREASE_ITEM"]').addEventListener('click', () => {
                                cart.forEach(cartItem => {
                                        if (cartItem.name === product.name) {
                                            if (cartItem.quantity > 1) {
                                                document.getElementById("cart_item_quantity_" + product.name).innerText = --cartItem.quantity;
                                                document.getElementById("cart_item_price_" + product.name).innerText = (document.getElementById("cart_item_quantity_" + product.name).innerText) * cartItem.price
                                                carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
                                                document.getElementById('cart_total').innerHTML = carttotal - parseFloat(product.price);
                                                document.getElementById('floatcarttotal').innerHTML = carttotal - parseFloat(product.price);
                                                localStorage.setItem('cart', JSON.stringify(cart));
                                                updateQuantityOnButton(product);
                                                // if (document.getElementById('cart_total').innerText >= 1000) {
                                                //     document.getElementById('deliverycharge').innerText = 40;
                                                // } else {
                                                //     document.getElementById('deliverycharge').innerText = 60;
                                                // }
                                            } else {
                                                // setTimeout(() => document.getElementById('titlerow' + product.name).remove(), 50);
                                                setTimeout(() => document.getElementById('cart__item' + product.name).remove(), 50);
                                                cart = cart.filter(cartItem => cartItem.name !== product.name);
                                                carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
                                                document.getElementById('cart_total').innerHTML = carttotal - parseFloat(product.price);
                                                document.getElementById('floatcarttotal').innerHTML = carttotal - parseFloat(product.price);
                                                document.getElementById('floatingtotalitems').innerHTML = parseFloat(document.getElementById('floatingtotalitems').innerHTML) - 1;
                                                document.getElementById('mobiletotalitems').innerHTML = parseFloat(document.getElementById('mobiletotalitems').innerHTML) - 1;
                                                // document.getElementById('cartheadingtotalitems').innerHTML = parseFloat(document.getElementById('cartheadingtotalitems').innerHTML) - 1;
                                                localStorage.setItem('cart', JSON.stringify(cart));
                                                updateWhenRemoveFromCart(product);

                                                // if (document.getElementById('cart_total').innerText >= 1000) {
                                                //     document.getElementById('deliverycharge').innerText = 40;
                                                // } else {
                                                //     document.getElementById('deliverycharge').innerText = 60;
                                                // }
                                            }


                                        }
                                    }
                                );
                            });

                            document.getElementById('removeitem' + product.name).addEventListener('click', () => {
                                cart.forEach(cartItem => {
                                        if (cartItem.name === product.name) {
                                            cartItemDOM.classList.add('cart__item--removed');
                                            // setTimeout(() => document.getElementById('titlerow' + product.name).remove(), 50);
                                            setTimeout(() => document.getElementById('cart__item' + product.name).remove(), 50);
                                            carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
                                            document.getElementById('cart_total').innerHTML = carttotal - parseFloat(product.price) * product.quantity;
                                            document.getElementById('floatcarttotal').innerHTML = carttotal - parseFloat(product.price) * product.quantity;
                                            document.getElementById('floatingtotalitems').innerHTML = parseFloat(document.getElementById('floatingtotalitems').innerHTML) - 1;
                                            document.getElementById('mobiletotalitems').innerHTML = parseFloat(document.getElementById('mobiletotalitems').innerHTML) - 1;
                                            // document.getElementById('cartheadingtotalitems').innerHTML = parseFloat(document.getElementById('cartheadingtotalitems').innerHTML) - 1;
                                            cart = cart.filter(cartItem => cartItem.name !== product.name);
                                            localStorage.setItem('cart', JSON.stringify(cart));
                                            updateWhenRemoveFromCart(product);

                                            // if (document.getElementById('cart_total').innerText >= 1000) {
                                            //     document.getElementById('deliverycharge').innerText = 40;
                                            // } else {
                                            //     document.getElementById('deliverycharge').innerText = 60;
                                            // }
                                        }
                                    }
                                );
                            });

                        }
                    });
                }
            }
        );
    });
    document.getElementById('placeorderbtn').addEventListener('click', () => {
        // {#alert({'carts':JSON.stringify(localStorage.getItem('cart'))});#}
        var token = '{{csrf_token}}';
        var item = JSON.stringify(localStorage.getItem('cart'));
        $.ajax({
            url: '/place-order/',
            type: 'post',
            dataType: 'json',
            data: {'carts': JSON.stringify(cart)},
            // {#data: JSON.stringify({'carts':localStorage.getItem('cart')}),#}
            success: function (data) {


                if (data) {
                    location.href = '/checkout/';
                } else {
                    // {#$("#loginmodal").modal("show");#}
                    window.location.href = '/user_login';
                }
            }
        });
    });
});

function updateQuantityOnButton(product) {
    var is_checkout_page = document.getElementById('is_checkout_page');
    if (is_checkout_page != null) {
        summary()
    }
    try {
        var btn = document.getElementsByName('btn' + product.name);
        btn.forEach(a => {
            // aTODO: ADD ITEM COUNT BEFORE IN CART
            if (a.tagName.toLowerCase() === 'a') {
                a.innerText = `${product.quantity} In Cart`;
                a.style.pointerEvents = "none";
            }
            // document.getElementById("overlay_second_num_of_items" + product.name).innerText = `${product.quantity} IN CART`;

        });
    } catch (e) {
        console.log(e);
    }
}

function updateWhenRemoveFromCart(product) {
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

                a.innerText = "Add to Cart";
                a.style.pointerEvents = "auto";
            }
            // else if (a.tagName === 'A') {
            //     document.getElementById("overlay_first" + product.name).style.display = 'block';
            //     document.getElementById("overlay_second" + product.name).style.display = 'none';
            //     document.getElementById("overlay_second_num_of_items" + product.name).innerText = "ADD TO CART";
            // }
        });
        let cart = (JSON.parse(localStorage.getItem('cart')) || []);
        // if (cart.length == 0) {
        //     document.getElementById('empty_bag').style.display = 'block';
        // } else {
        //     document.getElementById('empty_bag').style.display = 'none';
        // }
        var is_checkout_page = document.getElementById('is_checkout_page');
        if (is_checkout_page != null) {
            summary()
        }


    } catch (e) {
        alert(e);
    }
}