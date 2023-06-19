$(document).ready(function () {
    'use strict';

    let cart = (JSON.parse(localStorage.getItem('cart')) || []);
    const cartDOM = document.querySelector('.cart');
    const addToCartButtonsDOM = document.querySelectorAll('[data-action="ADD_TO_CART"]');
    var carttotal = 0;
    // if (cart.length > 0) {
    //     document.getElementById('empty_bag').style.display = 'none';
    //     cart.forEach(cartItem => {
    //         const product = cartItem;
    //         var itemtotal = product.price * product.quantity;
    //         var tablenew = document.getElementById('carttable');
    //         var txt = `
    //                         <tr id="titlerow${product.name}"  style="width: 300px !important; " >
    //                             <td colspan="3" style=" padding-bottom: 0px; width: 300px !important;" >${product.title}
    //                                 <a style="float: right" id="removeitem${product.name}" data-action="REMOVE_ITEM">
    //                                     <i class="fas fa-trash"
    //                                        style="padding-right: 0px !important; font-size: 15px !important; color:#cd0d0d; " ></i >
    //                                 </a >
    //                             </td >
    //                         </tr >
    //                         <tr class="cart__item" style="border-bottom:1pt solid lightgray;" id="bodyrow${product.name}">
    //                             <th scope="col" ><img style="width: 50px;" class="cart__item__image" id="cart_item_image_${product.name}" src="${product.image}" alt="${product.image}" ></th >
    //                             <th scope="col" style="padding-bottom: 15px; text-align: center">
    //                                 <button class="btn  btn-small" style="padding: 0px 5px; background-color: #c3e6cb" data-action="INCREASE_ITEM" >&plus;</button >
    //                                 <span class="cart__item__quantity font-weight-bold" id="cart_item_quantity_${product.name}">${product.quantity}</span >
    //                                 <button class="btn  btn-small${(product.quantity === 1 ? ' btn--danger' : '')}" style="padding: 0px 5px;background-color: #fadc8c " data-action="DECREASE_ITEM">&minus;</button>
    //                                 <p hidden class="cart__item__name" id="cart_item_name_${product.name}">${product.name}</p>
    //                             </th >
    //                             <th scope="col" style="text-align: right; padding-bottom: 22px">Tk. <span class="cart__item__price" id="cart_item_price_${product.name}">${itemtotal}</span></th >
    //                         </tr >
    //                       `;
    //         $(tablenew).find('tbody').append(txt);
    //         carttotal = parseFloat(document.getElementById('cart_total').innerText)
    //         document.getElementById('cart_total').innerHTML = carttotal + (product.price * product.quantity);
    //         document.getElementById('floatcarttotal').innerHTML = carttotal + (product.price * product.quantity);
    //         document.getElementById('floatingtotalitems').innerHTML = parseFloat(document.getElementById('floatingtotalitems').innerHTML) + 1;
    //         document.getElementById('cartheadingtotalitems').innerHTML = parseFloat(document.getElementById('cartheadingtotalitems').innerHTML) + 1;
    //
    //         const cartItemsDOM = Array.prototype.slice.call(cartDOM.querySelectorAll('.cart__item')).concat(Array.prototype.slice.call(document.querySelectorAll(".product_in_cart")));
    //         cartItemsDOM.forEach(cartItemDOM => {
    //             if (cartItemDOM.querySelector('.cart__item__name').innerText === product.name) {
    //                 cartItemDOM.querySelector('[data-action="INCREASE_ITEM"]').addEventListener('click', () => {
    //                     cart.forEach(cartItem => {
    //                         if (cartItem.name === product.name) {
    //                             try {
    //                                 document.getElementById("cart_item_quantity_" + product.name).innerText = ++cartItem.quantity;
    //                                 document.getElementById("cart_item_price_" + product.name).innerText = (document.getElementById("cart_item_quantity_" + product.name).innerText) * cartItem.price;
    //                                 carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
    //                                 document.getElementById('cart_total').innerHTML = carttotal + parseFloat(product.price);
    //                                 document.getElementById('floatcarttotal').innerHTML = carttotal + parseFloat(product.price);
    //                                 localStorage.setItem('cart', JSON.stringify(cart));
    //                                 // show increased item on button
    //                                 updateQuantityOnButton(product);
    //                                 if (document.getElementById('cart_total').innerText >= 1000) {
    //                                     document.getElementById('deliverycharge').innerText = 40;
    //                                 } else {
    //                                     document.getElementById('deliverycharge').innerText = 60;
    //                                 }
    //                             } catch (e) {
    //                                 console.log(e);
    //                             }
    //                         }
    //                     });
    //                 });
    //
    //                 cartItemDOM.querySelector('[data-action="DECREASE_ITEM"]').addEventListener('click', () => {
    //                     cart.forEach(cartItem => {
    //                         if (cartItem.name === product.name) {
    //                             if (cartItem.quantity > 1) {
    //                                 document.getElementById("cart_item_quantity_" + product.name).innerText = --cartItem.quantity;
    //                                 document.getElementById("cart_item_price_" + product.name).innerText = (document.getElementById("cart_item_quantity_" + product.name).innerText) * cartItem.price
    //                                 carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
    //                                 document.getElementById('cart_total').innerHTML = carttotal - parseFloat(product.price);
    //                                 document.getElementById('floatcarttotal').innerHTML = carttotal - parseFloat(product.price);
    //                                 localStorage.setItem('cart', JSON.stringify(cart));
    //                                 updateQuantityOnButton(cartItem);
    //                                 if (document.getElementById('cart_total').innerText >= 1000) {
    //                                     document.getElementById('deliverycharge').innerText = 40;
    //                                 } else {
    //                                     document.getElementById('deliverycharge').innerText = 60;
    //                                 }
    //                             } else {
    //                                 try {
    //                                     document.getElementById('titlerow' + cartItem.name).remove()
    //                                     document.getElementById('bodyrow' + cartItem.name).remove()
    //                                     cart = cart.filter(cartItem => cartItem.name !== product.name);
    //                                     carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
    //                                     document.getElementById('cart_total').innerHTML = carttotal - parseFloat(product.price);
    //                                     document.getElementById('floatcarttotal').innerHTML = carttotal - parseFloat(product.price);
    //                                     document.getElementById('floatingtotalitems').innerHTML = parseFloat(document.getElementById('floatingtotalitems').innerHTML) - 1;
    //                                     document.getElementById('cartheadingtotalitems').innerHTML = parseFloat(document.getElementById('cartheadingtotalitems').innerHTML) - 1;
    //                                     localStorage.setItem('cart', JSON.stringify(cart));
    //                                     updateWhenRemoveFromCart(cartItem);
    //                                     if (document.getElementById('cart_total').innerText >= 1000) {
    //                                         document.getElementById('deliverycharge').innerText = 40;
    //                                     } else {
    //                                         document.getElementById('deliverycharge').innerText = 60;
    //                                     }
    //                                 } catch (e) {
    //                                     console.log(e);
    //
    //                                 }
    //                             }
    //
    //
    //                         }
    //                     });
    //                 });
    //                 document.getElementById('titlerow' + product.name).querySelector('[data-action="REMOVE_ITEM"]').addEventListener('click', () => {
    //                     cart.forEach(cartItem => {
    //                         if (cartItem.name === product.name) {
    //                             cartItemDOM.classList.add('cart__item--removed');
    //                             document.getElementById('titlerow' + cartItem.name).remove()
    //                             document.getElementById('bodyrow' + cartItem.name).remove()
    //                             carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
    //                             document.getElementById('cart_total').innerHTML = carttotal - parseFloat(product.price) * cartItem.quantity;
    //                             document.getElementById('floatcarttotal').innerHTML = carttotal - parseFloat(product.price) * cartItem.quantity;
    //                             document.getElementById('floatingtotalitems').innerHTML = parseFloat(document.getElementById('floatingtotalitems').innerHTML) - 1;
    //                             document.getElementById('cartheadingtotalitems').innerHTML = parseFloat(document.getElementById('cartheadingtotalitems').innerHTML) - 1;
    //                             cart = cart.filter(cartItem => cartItem.name !== product.name);
    //                             localStorage.setItem('cart', JSON.stringify(cart));
    //                             updateWhenRemoveFromCart(cartItem);
    //                             if (document.getElementById('cart_total').innerText >= 1000) {
    //                                 document.getElementById('deliverycharge').innerText = 40;
    //                             } else {
    //                                 document.getElementById('deliverycharge').innerText = 60;
    //                             }
    //                         }
    //                     });
    //                 });
    //
    //             }
    //         });
    //         addToCartButtonsDOM.forEach(addToCartButtonDOM => {
    //             const productDOM = addToCartButtonDOM.closest(".cartable");
    //             var pronameDom = '';
    //             try {
    //                 pronameDom = productDOM.querySelector('.product__name').innerText;
    //             } catch (e) {
    //                 pronameDom = '';
    //             }
    //
    //             if (pronameDom === cartItem.name) {
    //                 if (addToCartButtonDOM.tagName.toLowerCase() === 'button') {
    //                     addToCartButtonDOM.innerText = `${cartItem.quantity} In Cart`;
    //                     addToCartButtonDOM.disabled = true;
    //                 }
    //
    //                 document.getElementById("overlay_first" + product.name).style.display = 'none';
    //                 document.getElementById("overlay_second" + product.name).style.display = 'block'
    //                 document.getElementById("overlay_second_num_of_items" + product.name).innerText = product.quantity + " IN CART"
    //             }
    //
    //
    //         });
    //
    //     });
    //     if (document.getElementById('cart_total').innerText >= 1000) {
    //         document.getElementById('deliverycharge').innerText = 40;
    //     } else {
    //         document.getElementById('deliverycharge').innerText = 60;
    //     }
    // }

    addToCartButtonsDOM.forEach(addToCartButtonDOM => {
        addToCartButtonDOM.addEventListener('click', () => {
                const productDOM = addToCartButtonDOM.closest(".cartable");
                const product = {
                    image: productDOM.querySelector('.product__image').getAttribute('src'),
                    name: productDOM.querySelector('.product__name').innerText,
                    title: productDOM.querySelector('.product__title').innerText,
                    price: productDOM.querySelector('.product__price').innerText,
                    quantity: 1,
                };
                const isInCart = (cart.filter(cartItem => (cartItem.name === product.name)).length > 0);

                var table = document.getElementById('carttable');
                // {#cartDOM.insertAdjacentHTML('beforeend',"<img src='${product.image}'>" );#}
                if (!isInCart) {
                    cart.push(product);
                    localStorage.setItem('cart', JSON.stringify(cart));
                    document.getElementById('cart_count').innerText = cart.length.toString()
                    // document.getElementById('cart_amount').innerText = cart.length.toString()
                }
                else{}
                    pass
                //     var txt = `
                //             <tr id="titlerow${product.name}"  style="width: 300px !important; " >
                //                 <td colspan="3" style=" padding-bottom: 0px; width: 300px !important;" >${product.title}
                //                     <a style="float: right" id="removeitem${product.name}">
                //                         <i class="fas fa-trash"
                //                            style="padding-right: 0px !important; font-size: 15px !important; color:#cd0d0d; " ></i >
                //                     </a >
                //                 </td >
                //             </tr >
                //             <tr class="cart__item" style="border-bottom:1pt solid lightgray;" id="bodyrow${product.name}">
                //                 <th scope="col" ><img style="width: 50px;" class="cart__item__image" id="cart_item_image_${product.name}" src="${product.image}" alt="${product.image}" ></th >
                //                 <th scope="col" style="padding-bottom: 15px; text-align: center">
                //                     <button class="btn  btn-small" style="padding: 0px 5px; background-color: #c3e6cb" data-action="INCREASE_ITEM" >&plus;</button >
                //                     <span class="cart__item__quantity font-weight-bold" id="cart_item_quantity_${product.name}">${product.quantity}</span >
                //                     <button class="btn  btn-small${(product.quantity === 1 ? ' btn--danger' : '')}" style="padding: 0px 5px;background-color: #fadc8c " data-action="DECREASE_ITEM">&minus;</button>
                //                     <p hidden class="cart__item__name" id="cart_item_name_${product.name}">${product.name}</p>
                //                 </th >
                //                 <th scope="col" style="text-align: right; padding-bottom: 22px">Tk. <span class="cart__item__price" id="cart_item_price_${product.name}">${product.price}</span></th >
                //             </tr >
                //           `;
                //     $(table).find('tbody').append(txt);
                //     /*
                //     EXPAND THE CART WHEN FIRST TIME IS ADDED
                //     AT THIS MOMENT IT OPENS WHEN THE THE PRODUCT COUNT IS ZERO
                //     IF YOU REMOVE ALL THE OTHER PRODUCTS FROM THE LIST AND THEN ADD
                //     AGAIN, IT SHOULD WORK THE SAME
                //     */
                //     if (cart.length == 0) {
                //         document.getElementById('empty_bag').style.display = 'none';
                //         sidebarOPen();
                //
                //     }
                //     cart.push(product);
                //     carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
                //     document.getElementById('cart_total').innerHTML = carttotal + parseFloat(product.price * product.quantity);
                //     document.getElementById('floatcarttotal').innerHTML = carttotal + parseFloat(product.price * product.quantity);
                //     document.getElementById('floatingtotalitems').innerHTML = parseFloat(document.getElementById('floatingtotalitems').innerHTML) + 1;
                //     document.getElementById('cartheadingtotalitems').innerHTML = parseFloat(document.getElementById('cartheadingtotalitems').innerHTML) + 1;
                //     localStorage.setItem('cart', JSON.stringify(cart));
                //     try {
                //         var btn = document.getElementsByName('btn' + product.name);
                //         btn.forEach(a => {
                //             // TODO: ADD ITEM COUNT BEFORE IN CART
                //             if (a.tagName === 'BUTTON') {
                //                 a.innerText = `${product.quantity} In Cart`;
                //                 a.disabled = true;
                //             } else if (a.tagName === 'A') {
                //                 document.getElementById("overlay_first" + product.name).style.display = 'none';
                //                 document.getElementById("overlay_second" + product.name).style.display = 'block'
                //                 document.getElementById("overlay_second_num_of_items" + product.name).innerText = product.quantity + " IN CART"
                //             }
                //
                //         });
                //     } catch (e) {
                //         console.log(e);
                //     }
                //     if (document.getElementById('cart_total').innerText >= 1000) {
                //         document.getElementById('deliverycharge').innerText = 40;
                //     } else {
                //         document.getElementById('deliverycharge').innerText = 60;
                //     }
                //
                //     // {#const cartItemsDOM = cartDOM.querySelectorAll('.cart__item');#}
                //     const cartItemsDOM = Array.prototype.slice.call(cartDOM.querySelectorAll('.cart__item')).concat(Array.prototype.slice.call(document.querySelectorAll(".product_in_cart")));
                //     cartItemsDOM.forEach(cartItemDOM => {
                //         if (cartItemDOM.querySelector('.cart__item__name').innerText === product.name) {
                //
                //             cartItemDOM.querySelector('[data-action="INCREASE_ITEM"]').addEventListener('click', () => {
                //                 cart.forEach(cartItem => {
                //                     if (cartItem.name === product.name) {
                //                         document.getElementById("cart_item_quantity_" + product.name).innerText = ++cartItem.quantity;
                //                         carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
                //                         document.getElementById('cart_total').innerHTML = carttotal + parseFloat(product.price);
                //                         document.getElementById('floatcarttotal').innerHTML = carttotal + parseFloat(product.price);
                //                         document.getElementById("cart_item_price_" + product.name).innerText = (document.getElementById("cart_item_quantity_" + product.name).innerText) * cartItem.price
                //                         localStorage.setItem('cart', JSON.stringify(cart));
                //                         // show increased item on button
                //                         updateQuantityOnButton(product);
                //                         if (document.getElementById('cart_total').innerText >= 1000) {
                //                             document.getElementById('deliverycharge').innerText = 40;
                //                         } else {
                //                             document.getElementById('deliverycharge').innerText = 60;
                //                         }
                //
                //                     }
                //                 });
                //             });
                //
                //             cartItemDOM.querySelector('[data-action="DECREASE_ITEM"]').addEventListener('click', () => {
                //                 cart.forEach(cartItem => {
                //                         if (cartItem.name === product.name) {
                //                             if (cartItem.quantity > 1) {
                //                                 document.getElementById("cart_item_quantity_" + product.name).innerText = --cartItem.quantity;
                //                                 document.getElementById("cart_item_price_" + product.name).innerText = (document.getElementById("cart_item_quantity_" + product.name).innerText) * cartItem.price
                //                                 carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
                //                                 document.getElementById('cart_total').innerHTML = carttotal - parseFloat(product.price);
                //                                 document.getElementById('floatcarttotal').innerHTML = carttotal - parseFloat(product.price);
                //                                 localStorage.setItem('cart', JSON.stringify(cart));
                //                                 updateQuantityOnButton(product);
                //                                 if (document.getElementById('cart_total').innerText >= 1000) {
                //                                     document.getElementById('deliverycharge').innerText = 40;
                //                                 } else {
                //                                     document.getElementById('deliverycharge').innerText = 60;
                //                                 }
                //                             } else {
                //                                 setTimeout(() => document.getElementById('titlerow' + product.name).remove(), 50);
                //                                 setTimeout(() => document.getElementById('bodyrow' + product.name).remove(), 50);
                //                                 cart = cart.filter(cartItem => cartItem.name !== product.name);
                //                                 carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
                //                                 document.getElementById('cart_total').innerHTML = carttotal - parseFloat(product.price);
                //                                 document.getElementById('floatcarttotal').innerHTML = carttotal - parseFloat(product.price);
                //                                 document.getElementById('floatingtotalitems').innerHTML = parseFloat(document.getElementById('floatingtotalitems').innerHTML) - 1;
                //                                 document.getElementById('cartheadingtotalitems').innerHTML = parseFloat(document.getElementById('cartheadingtotalitems').innerHTML) - 1;
                //                                 localStorage.setItem('cart', JSON.stringify(cart));
                //                                 updateWhenRemoveFromCart(product);
                //
                //                                 if (document.getElementById('cart_total').innerText >= 1000) {
                //                                     document.getElementById('deliverycharge').innerText = 40;
                //                                 } else {
                //                                     document.getElementById('deliverycharge').innerText = 60;
                //                                 }
                //                             }
                //
                //
                //                         }
                //                     }
                //                 );
                //             });
                //
                //             document.getElementById('removeitem' + product.name).addEventListener('click', () => {
                //                 cart.forEach(cartItem => {
                //                         if (cartItem.name === product.name) {
                //                             cartItemDOM.classList.add('cart__item--removed');
                //                             setTimeout(() => document.getElementById('titlerow' + product.name).remove(), 50);
                //                             setTimeout(() => document.getElementById('bodyrow' + product.name).remove(), 50);
                //                             carttotal = parseFloat(document.getElementById('cart_total').innerHTML);
                //                             document.getElementById('cart_total').innerHTML = carttotal - parseFloat(product.price) * product.quantity;
                //                             document.getElementById('floatcarttotal').innerHTML = carttotal - parseFloat(product.price) * product.quantity;
                //                             document.getElementById('floatingtotalitems').innerHTML = parseFloat(document.getElementById('floatingtotalitems').innerHTML) - 1;
                //                             document.getElementById('cartheadingtotalitems').innerHTML = parseFloat(document.getElementById('cartheadingtotalitems').innerHTML) - 1;
                //                             cart = cart.filter(cartItem => cartItem.name !== product.name);
                //                             localStorage.setItem('cart', JSON.stringify(cart));
                //                             updateWhenRemoveFromCart(product);
                //
                //                             if (document.getElementById('cart_total').innerText >= 1000) {
                //                                 document.getElementById('deliverycharge').innerText = 40;
                //                             } else {
                //                                 document.getElementById('deliverycharge').innerText = 60;
                //                             }
                //                         }
                //                     }
                //                 );
                //             });
                //
                //         }
                //     });
                // }
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
    console.log(1);
    try {
        var btn = document.getElementsByName('btn' + product.name);
        btn.forEach(a => {
            // TODO: ADD ITEM COUNT BEFORE IN CART
            if (a.tagName.toLowerCase() === 'button') {
                a.innerText = `${product.quantity} In Cart`;
                a.disabled = true;
            }
            document.getElementById("overlay_second_num_of_items" + product.name).innerText = `${product.quantity} IN CART`;
        });
    } catch (e) {
        console.log(e);
    }
}

function updateWhenRemoveFromCart(product) {
    try {
        try {
            var el = document.getElementById('overlay_second' + product.name);
            var el1 = el.querySelector('[data-action="DECREASE_ITEM"]');
            elClone = el1.cloneNode(true);
            el1.parentNode.replaceChild(elClone, el1);
            var el2 = el.querySelector('[data-action="INCREASE_ITEM"]');
            elClone = el2.cloneNode(true);
            el2.parentNode.replaceChild(elClone, el2);
        } catch (e) {

        }
        var btn = document.getElementsByName('btn' + product.name);
        btn.forEach(a => {
            if (a.tagName === 'BUTTON') {
                a.innerText = 'Add to Cart';
                a.disabled = false;
            } else if (a.tagName === 'A') {
                document.getElementById("overlay_first" + product.name).style.display = 'block';
                document.getElementById("overlay_second" + product.name).style.display = 'none';
                document.getElementById("overlay_second_num_of_items" + product.name).innerText = "ADD TO CART";
            }
        });
        let cart = (JSON.parse(localStorage.getItem('cart')) || []);
        if (cart.length == 0) {
            document.getElementById('empty_bag').style.display = 'block';
        } else {
            document.getElementById('empty_bag').style.display = 'none';
        }
    } catch (e) {
        alert(e);
    }
}