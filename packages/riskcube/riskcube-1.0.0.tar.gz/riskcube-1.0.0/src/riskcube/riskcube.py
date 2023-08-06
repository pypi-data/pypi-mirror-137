# -*- coding: utf-8 -*-
# Copyright: giordano.ch AG

import requests
import json
import socket


class RiskCube:
    shopId = ''
    apiKey = ''
    baseUrl = ''
    authHeader = {}
    productionsUrl = 'https://service-zs.riskcube.ch/api/v1/RiskCube'

    def __init__(self, shop_id, api_key):
        self.shopId = shop_id
        self.apiKey = api_key

        self.authHeader = {
            'X-API-KEY': self.apiKey,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        print(self.authHeader)

        self.baseUrl = self.productionsUrl

    def call_service(self, endpoint, request_data):
        response = requests.post(self.baseUrl + endpoint, json=request_data, headers=self.authHeader)
        return response.json()

    def get_ip_address(self):
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip

    def claim(self, response):
        endpoint = '/claim'
        '''
        response = {
            "shopId": self.shopId,
            "orderProcessId": "ref001",
            "ipAddress": self.get_ip_address(),
            "macAddress": null,
            "customerId": "cus001",
            "billingAddress": {
                "type": "Consumer",
                "businessName": null,
                "firstName": "Martin",
                "lastName": "Früh",
                "co": null,
                "street": "Funkenbüelstrasse",
                "houseNumber": "1",
                "postCode": "9243",
                "locationName": "Jonschwil",
                "country": "CH",
                "email": null,
                "phone": null,
                "dateOfBirth": null
            },
            "shippingAddress": null,
            "orderAmount": 1200
        }
        '''

        request = self.call_service(endpoint, response)
        return request

    def purchase(self, response):
        endpoint = '/purchase'

        '''
        response = {
          "shopId": "20071992",
          "shopOrderId": "soi001",
          "orderProcessToken": "responsekey123",
          "dateOfOrder": "2021-12-08 14-47-27",
          "paymentMethod": "Invoice"
        }
        '''
        request = self.call_service(endpoint, response)
        return request

    def invoice(self, response):
        endpoint = '/invoice'

        '''
        response = {
          "shopId": "20071992",
          "shopOrderId": "soi001",
          "orderProcessToken": "responsekey123",
          "language": "DE",
          "transmissions": "Mail",
          "additionalInfo": null,
          "shoppingCart": [
            {
              "claimType": "Claim",
              "itemId": "ite0001",
              "itemDefinition": "an item",
              "numberOfItems": 1,
              "unitAmountNet": 9,
              "unitAmountGross": 10,
              "totalAmountNet": 9,
              "totalAmountGross": 200,
              "currency": "CHF",
              "vat": 10
            },
            {
              "claimType": "Claim",
              "itemId": "ite0002",
              "itemDefinition": "another item",
              "numberOfItems": 1,
              "unitAmountNet": 9,
              "unitAmountGross": 10,
              "totalAmountNet": 9,
              "totalAmountGross": 1000,
              "currency": "CHF",
              "vat": 10
            }
          ]
        }
        '''

        request = self.call_service(endpoint, response)
        return request

    def cancel(self, response):
        endpoint = '/cancel'

        '''
        response = {
          "shopId": "string",
          "shopOrderId": "string",
          "orderProcessToken": "string",
          "cancellationReference": "string",
          "shoppingCart": [
            {
              "claimType": "reduction",
              "itemId": "string",
              "itemDefinition": "string",
              "numberOfItems": 0,
              "unitAmountNet": 0,
              "unitAmountGross": 0,
              "totalAmountNet": 0,
              "totalAmountGross": 0,
              "currency": "string",
              "vat": 0
            }
          ]
        }
        '''

        request = self.call_service(endpoint, response)
        return request
