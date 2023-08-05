# eopayment - online payment library
# Copyright (C) 2011-2020 Entr'ouvert
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from xml.etree import ElementTree as ET

import pytest
from six.moves.urllib import parse as urllib

import eopayment
import eopayment.ogone as ogone
from eopayment import ResponseError

PSPID = '2352566ö'


@pytest.fixture(params=[None, 'iso-8859-1', 'utf-8'])
def params(request):
    params = {
        'environment': ogone.ENVIRONMENT_TEST,
        'pspid': PSPID,
        'sha_in': 'sécret',
        'sha_out': 'sécret',
        'automatic_return_url': 'http://example.com/autömatic_réturn_url',
    }
    encoding = request.param
    if encoding:
        params['encoding'] = encoding
    return params


def test_request(params):
    ogone_backend = eopayment.Payment('ogone', params)
    amount = '42.42'
    order_id = 'my ordér'
    reference, kind, what = ogone_backend.request(amount=amount, orderid=order_id, email='foo@example.com')
    assert len(reference) == 32
    root = ET.fromstring(str(what))
    assert root.tag == 'form'
    assert root.attrib['method'] == 'POST'
    assert root.attrib['action'] == ogone.ENVIRONMENT_TEST_URL
    values = {
        'CURRENCY': 'EUR',
        'ORDERID': order_id,
        'PSPID': PSPID,
        'EMAIL': 'foo@example.com',
        'AMOUNT': amount.replace('.', ''),
        'LANGUAGE': 'fr_FR',
        'COMPLUS': reference,
    }
    values.update({'SHASIGN': ogone_backend.backend.sha_sign_in(values)})
    for node in root:
        assert node.attrib['type'] in ('hidden', 'submit')
        assert set(node.attrib.keys()), {'type', 'name' == 'value'}
        name = node.attrib['name']
        if node.attrib['type'] == 'hidden':
            assert name in values
            assert node.attrib['value'] == values[name]


def test_response(params):
    ogone_backend = eopayment.Payment('ogone', params)
    order_id = 'myorder'
    data = {
        'orderid': 'myorder',
        'status': '9',
        'payid': '3011229363',
        'cn': 'Usér',
        'ncerror': '0',
        'trxdate': '10/24/16',
        'acceptance': 'test123',
        'currency': 'eur',
        'amount': '7.5',
    }
    data['shasign'] = ogone_backend.backend.sha_sign_out(data, encoding=params.get('encoding', 'iso-8859-1'))
    # uniformize to utf-8 first
    for k in data:
        data[k] = eopayment.common.force_byte(data[k], encoding=params.get('encoding', 'iso-8859-1'))
    response = ogone_backend.response(urllib.urlencode(data))
    assert response.signed
    assert response.order_id == order_id


def test_iso_8859_1_response():
    params = {
        'environment': ogone.ENVIRONMENT_TEST,
        'pspid': PSPID,
        'sha_in': 'sécret',
        'sha_out': 'sécret',
        'automatic_return_url': 'http://example.com/autömatic_réturn_url',
    }
    ogone_backend = eopayment.Payment('ogone', params)
    order_id = 'lRXK4Rl1N2yIR3R5z7Kc'
    backend_response = (
        'orderID=lRXK4Rl1N2yIR3R5z7Kc&currency=EUR&amount=7%2E5'
        '&PM=CreditCard&ACCEPTANCE=test123&STATUS=9'
        '&CARDNO=XXXXXXXXXXXX9999&ED=0118'
        '&CN=Miha%EF+Serghe%EF&TRXDATE=10%2F24%2F16'
        '&PAYID=3011228911&NCERROR=0&BRAND=MasterCard'
        '&IP=80%2E12%2E92%2E47&SHASIGN=C429BE892FACFBFCE5E2CC809B102D866DD3D48C'
    )
    response = ogone_backend.response(backend_response)
    assert response.signed
    assert response.order_id == order_id


def test_bad_response(params):
    ogone_backend = eopayment.Payment('ogone', params)
    data = {'payid': '32100123', 'status': 9, 'ncerror': 0}
    with pytest.raises(ResponseError, match='missing ORDERID, PAYID, STATUS or NCERROR'):
        ogone_backend.response(urllib.urlencode(data))


def test_bank_transfer_response(params):
    ogone_backend = eopayment.Payment('ogone', params)
    data = {
        'orderid': 'myorder',
        'status': '41',
        'payid': '3011229363',
        'cn': 'User',
        'ncerror': '0',
        'trxdate': '10/24/16',
        'brand': 'Bank transfer',
        'pm': 'bank transfer',
        'currency': 'eur',
        'amount': '7.5',
        'shasign': '944CBD1E010BA4945415AE4B16CC40FD533F6CE2',
    }
    # uniformize to expected encoding
    for k in data:
        data[k] = eopayment.common.force_byte(data[k], encoding=params.get('encoding', 'iso-8859-1'))
    response = ogone_backend.response(urllib.urlencode(data))
    assert response.signed
    assert response.result == eopayment.WAITING

    # check utf-8 based signature is also ok
    data['shasign'] = b'0E35F687ACBEAA6CA769E0ADDBD0863EB6C1678A'
    response = ogone_backend.response(urllib.urlencode(data))
    assert response.signed
    assert response.result == eopayment.WAITING

    # check invalid signature is not marked ok
    data['shasign'] = b'0000000000000000000000000000000000000000'
    response = ogone_backend.response(urllib.urlencode(data))
    assert not response.signed
