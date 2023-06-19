from sslcommerz_lib import SSLCOMMERZ


class PaymentProcessing:
    settings = { 'store_id': 'fortu60ee90da6583a', 'store_pass': 'fortu60ee90da6583a@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)

    def payment_request(self, order_details):
        post_body = {}
        post_body['total_amount'] =999.26
        post_body['currency'] = "BDT"
        post_body['tran_id'] = "12345"
        post_body['success_url'] = "your success url"
        post_body['fail_url'] = "your fail url"
        post_body['cancel_url'] = "your cancel url"
        post_body['emi_option'] = 0
        post_body['cus_name'] = "test"
        post_body['cus_email'] = "test@test.com"
        post_body['cus_phone'] = "01700000000"
        post_body['cus_add1'] = "customer address"
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = 1
        post_body['product_name'] = "Test"
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"

        response = self.sslcz.createSession(post_body) # API response
        print(response)
    # Need to redirect user to response['GatewayPageURL']

    def validate_payment(self):
        post_body = {}
        post_body['tran_id'] = '5E121A0D01F92'
        post_body['val_id'] = '200105225826116qFnATY9sHIwo'
        post_body['amount'] = "10.00"
        post_body['card_type'] = "VISA-Dutch Bangla"
        post_body['store_amount'] = "9.75"
        post_body['card_no'] = "418117XXXXXX6675"
        post_body['bank_tran_id'] = "200105225825DBgSoRGLvczhFjj"
        post_body['status'] = "VALID"
        post_body['tran_date'] = "2020-01-05 22:58:21"
        post_body['currency'] = "BDT"
        post_body['card_issuer'] = "TRUST BANK, LTD."
        post_body['card_brand'] = "VISA"
        post_body['card_issuer_country'] = "Bangladesh"
        post_body['card_issuer_country_code'] = "BD"
        post_body['store_id'] = "test_testemi"
        post_body['verify_sign'] = "d42fab70ae0bcbda5280e7baffef60b0"
        post_body[
            'verify_key'] = "amount,bank_tran_id,base_fair,card_brand,card_issuer,card_issuer_country,card_issuer_country_code,card_no,card_type,currency,currency_amount,currency_rate,currency_type,risk_level,risk_title,status,store_amount,store_id,tran_date,tran_id,val_id,value_a,value_b,value_c,value_d"
        post_body['verify_sign_sha2'] = "02c0417ff467c109006382d56eedccecd68382e47245266e7b47abbb3d43976e"
        post_body['currency_type'] = "BDT"
        post_body['currency_amount'] = "10.00"
        post_body['currency_rate'] = "1.0000"
        post_body['base_fair'] = "0.00"
        post_body['value_a'] = ""
        post_body['value_b'] = ""
        post_body['value_c'] = ""
        post_body['value_d'] = ""
        post_body['risk_level'] = "0"
        post_body['risk_title'] = "Safe"
        if self.sslcz.hash_validate_ipn(post_body):
            response = self.sslcz.validationTransactionOrder(post_body['val_id'])
            print(response)
            return response
        else:
            print("Hash validation failed")
            return None

    def get_payment_details_by_skey(self):
        sessionkey = 'A8EF93B75B8107E4F36049E80B4F9149'
        response = self.sslcz.transaction_query_session(sessionkey)
        print(response)
        return response

    def get_payment_details_by_tid(self):
        tranid = '59C2A4F6432F8'
        response = self.sslcz.transaction_query_tranid(tranid)
        print(response)

    def refund_request(self):
        bank_tran_id = '1709162345070ANJdZV8LyI4cMw'
        refund_amount = '5.50'
        refund_remarks = 'out of stock'
        response = self.sslcz.init_refund(bank_tran_id, refund_amount, refund_remarks)
        print(response)

    def refund_status(self):
        refund_ref_id = '59bd63fea5455'
        response = self.sslcz.query_refund_status(refund_ref_id)
        print(response)