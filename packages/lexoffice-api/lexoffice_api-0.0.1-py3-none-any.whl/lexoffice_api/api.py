import uuid
import requests
from requests.exceptions import RequestException
from .datatypes import VoucherList, Invoice, VoucherType, VoucherStatus
from .exceptions import LexofficeException

class LexofficeClient:

    def __init__(self, api_key):
        self.version = 1
        self.url = f'https://api.lexoffice.io/v{self.version}'
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        }

    def ping(self) -> bool:
        """ Ping Lexoffice API and test the connection.

        :return: True if the /ping endpoint could be requested successfully.
        """
        response = requests.get(
            url=f'{self.url}/ping',
            headers=self.headers
        )
        if response.status_code == 200:
            print('Connected to lexoffice Public API')
            print('User:', response.json()['userEmail'])
            return True
        else:
            return False

    def get_voucherlist(self, voucher_type: VoucherType, status: list[VoucherStatus], page: int = None, size: int = None) -> VoucherList:
        """ Fetch a voucherlist.

        :param voucher_type: type(s) of the vouchers to be fetched
        :param status: status(es) of the vouchers to be fetched
        :param page: Number of the page to be fetched (optional) - If not specified, the first page will be fetched
        :param size: Size of the page (max. number of vouchers to be fetched
        :return: VoucherList contatining the requested Vouchers
        """
        if len(status) < 1:
            raise ValueError('Specify at least 1 status')
        status_str = []
        for s in status:
            status_str.append(s.value)
        params = {
            'voucherType': voucher_type.value,
            'voucherStatus': ','.join(status_str),
            'page': page,
            'size': size
        }
        response = requests.get(
            url=f'{self.url}/voucherlist',
            headers=self.headers,
            params=params
        )
        content = response.json()
        if response.status_code != 200:
            if 'error' in content and 'message' in content:
                error = content['error']
                msg = content['message']
                raise RequestException(f'{error}: {msg}')
            else:
                msg = content['message']
                raise RequestException(f'Error while getting VoucherList from Lexoffice API: {msg}')
        return VoucherList(content)

    def get_invoice(self, invoice_id: uuid.UUID) -> Invoice:
        """ Fetches an invoice with the specified ID from the /invoices endpoint.

        :param invoice_id: The UUID of the requested invoice
        :return: Invoice that was requested
        :raise RequestException if an error has occurred during the API call.
        """
        response = requests.get(
            url=f'{self.url}/invoices/{str(invoice_id)}',
            headers=self.headers
        )
        content = response.json()
        if response.status_code != 200:
            raise LexofficeException(response, 'Error while getting invoice from Lexoffice API')
        return Invoice(content)
