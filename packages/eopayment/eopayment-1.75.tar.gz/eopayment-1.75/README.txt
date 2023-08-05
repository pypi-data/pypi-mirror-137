Interface with French's bank online credit card processing services
===================================================================

Services supported are:
- ATOS/SIPS v2 used by:
  - BNP under the name Mercanet,
  - Banque Populaire (before 2010/2011) under the name Cyberplus,
  - CCF under the name Elysnet,
  - HSBC under the name Elysnet,
  - Crédit Agricole under the name e-Transactions,
  - La Banque Postale under the name ScelliusNet,
  - LCL under the name Sherlocks,
  - Société Générale under the name Sogenactif
  - and Crédit du Nord under the name Webaffaires,
- Payzen/SystemPay v2 by Banque Populaire (since 2010/2011) and Caisse d'Épargne (Natixis)
- TIPI/PayFiP Régie
- PayFiP Régie Web-service
- Ogone
- Paybox
- Payzen

You can emit payment request under a simple API which takes as input a
dictionnary as configuration and an amount to pay. You get back a
transaction_id. Another unique API allows to handle the notifications coming
from those services, reporting whether the transaction was successful and which
one it was. The full content (which is specific to the service) is also
reported for logging purpose.

The paybox module also depend upon the python Cryptodome library for RSA
signature validation on the responses.

Some backends allow to specify the order and transaction ids in different
fields, in order to allow to match them in payment system backoffice. They are:
- Payzen
- SIPS
- SystemPay
- PayFiP Régie Web-Service

For other backends, the order and transaction ids, separated by '!' are sent in
order id field, so they can be matched in backoffice.

PayFiP Régie Web-Service
========================

You can test your PayFiP regie web-service connection with an integrated CLI utility:

    $ python3 -m eopayment.payfip_ws info-client --help
    Usage: payfip_ws.py info-client [OPTIONS] NUMCLI

    Options:
      --help  Show this message and exit.

    $ python3 -m eopayment.payfip_ws get-idop --help
    Usage: payfip_ws.py get-idop [OPTIONS] NUMCLI

    Options:
      --saisie [T|X|W]         [required]
      --exer TEXT              [required]
      --montant INTEGER        [required]
      --refdet TEXT            [required]
      --mel TEXT               [required]
      --url-notification TEXT  [required]
      --url-redirect TEXT      [required]
      --objet TEXT
      --help                   Show this message and exit.

    $ python3 -m eopayment.payfip_ws info-paiement --help
    Usage: payfip_ws.py info-paiement [OPTIONS] IDOP

    Options:
      --help  Show this message and exit.


Generic CLI Tool
================

You can put some configuration in ~/.config/eopayment.init ::

    [default]
    debug=yes

    [systempayv2]
    # same name as passed in the options argument to Payment.__init__()
    vads_site_id=12345678
    secret_test=xyzabcdefgh
    vads_ctx_mode=TEST

    $ python3 -m eopayment --option vads_site_id=56781234 request 10.0 --param transaction_id=1234 --param email=john.doe@example.com
    Transaction ID: 1234
    <form method="POST" action="https://paiement.systempay.fr/vads-payment/">
      <input type="hidden" name="vads_cust_country" value="FR"/>
      <input type="hidden" name="vads_validation_mode" value=""/>
      <input type="hidden" name="vads_site_id" value="12345678"/>
      <input type="hidden" name="vads_payment_config" value="SINGLE"/>
      <input type="hidden" name="vads_trans_id" value="GavPXW"/>
      <input type="hidden" name="vads_action_mode" value="INTERACTIVE"/>
      <input type="hidden" name="vads_contrib" value="eopayment"/>
      <input type="hidden" name="vads_page_action" value="PAYMENT"/>
      <input type="hidden" name="vads_amount" value="1010"/>
      <input type="hidden" name="signature" value="d5690d02fed621687b19c90053a77b37a1c78370"/>
      <input type="hidden" name="vads_ctx_mode" value="TEST"/>
      <input type="hidden" name="vads_version" value="V2"/>
      <input type="hidden" name="vads_payment_cards" value=""/>
      <input type="hidden" name="vads_ext_info_eopayment_trans_id" value="1234"/>
      <input type="hidden" name="vads_trans_date" value="20201027211254"/>
      <input type="hidden" name="vads_language" value="fr"/>
      <input type="hidden" name="vads_capture_delay" value=""/>
      <input type="hidden" name="vads_currency" value="978"/>
      <input type="hidden" name="vads_cust_email" value="john.doe@example.com"/>
      <input type="hidden" name="vads_return_mode" value="GET"/>
      <input type="submit" name="Submit" value="Submit" />
    </form>
    [ Local browser is automatically opened with this form which is auto-submitted ]

    $ python3 -m eopayment --debug response 'vads_amount=1010&vads_auth_mode=FULL&vads_auth_number=3fd070&vads_auth_result=00&vads_capture_delay=0&vads_card_brand=CB&vads_card_number=597010XXXXXX0018&vads_payment_certificate=f582e920616a33bdaa0c242ee3fc3d435d367575&vads_ctx_mode=TEST&vads_currency=978&vads_effective_amount=1010&vads_effective_currency=978&vads_site_id=12345678&vads_trans_date=20201029093825&vads_trans_id=Vlco55&vads_trans_uuid=e8defc7bd32c418c93c4b2be676d2796&vads_validation_mode=0&vads_version=V2&vads_warranty_result=&vads_payment_src=EC&vads_cust_country=FR&vads_contrib=eopayment&vads_tid=001&vads_sequence_number=1&vads_contract_used=2334410&vads_trans_status=AUTHORISED&vads_expiry_month=6&vads_expiry_year=2021&vads_bank_label=Banque+de+d%C3%A9mo+et+de+l%27innovation&vads_bank_product=MCW&vads_pays_ip=FR&vads_presentation_date=20201029093826&vads_effective_creation_date=20201029093826&vads_operation_type=DEBIT&vads_result=00&vads_extra_result=&vads_card_country=FR&vads_language=fr&vads_brand_management=%7B%22userChoice%22%3Afalse%2C%22brandList%22%3A%22CB%7CMASTERCARD%22%2C%22brand%22%3A%22CB%22%7D&vads_action_mode=INTERACTIVE&vads_payment_config=SINGLE&vads_page_action=PAYMENT&vads_threeds_enrolled=Y&vads_threeds_auth_type=CHALLENGE&vads_threeds_eci=02&vads_threeds_xid=RFBSMkdWdFE0Wk15VWw0RkJjMzU%3D&vads_threeds_cavvAlgorithm=2&vads_threeds_status=Y&vads_threeds_sign_valid=1&vads_threeds_error_code=&vads_threeds_exit_status=10&vads_threeds_cavv=jG26AYSjvclBARFYSf%2FtXRmjGXM%3D&signature=5594aa2bc35c9e45e759b08df339e5f8ecf2c410'
      result : 3
      signed : True
      bank_data  :
      {'__bank_id': '3fd070',
       'signature': '5594aa2bc35c9e45e759b08df339e5f8ecf2c410',
       'vads_action_mode': 'INTERACTIVE',
       'vads_amount': '1010',
       'vads_auth_mode': 'FULL',
       'vads_auth_number': '3fd070',
       'vads_auth_result': '00',
       'vads_auth_result_message': 'Transaction approuvée ou traitée avec succès',
       'vads_bank_label': "Banque de démo et de l'innovation",
       'vads_bank_product': 'MCW',
       'vads_brand_management': '{"userChoice":false,"brandList":"CB|MASTERCARD","brand":"CB"}',
       'vads_capture_delay': '0',
       'vads_card_brand': 'CB',
       'vads_card_country': 'FR',
       'vads_card_number': '597010XXXXXX0018',
       'vads_contract_used': '2334410',
       'vads_contrib': 'eopayment',
       'vads_ctx_mode': 'TEST',
       'vads_currency': '978',
       'vads_cust_country': 'FR',
       'vads_effective_amount': '1010',
       'vads_effective_creation_date': '20201029093826',
       'vads_effective_currency': '978',
       'vads_expiry_month': '6',
       'vads_expiry_year': '2021',
       'vads_extra_result': '',
       'vads_extra_result_message': 'Pas de contrôle effectué.',
       'vads_language': 'fr',
       'vads_operation_type': 'DEBIT',
       'vads_page_action': 'PAYMENT',
       'vads_payment_certificate': 'f582e920616a33bdaa0c242ee3fc3d435d367575',
       'vads_payment_config': 'SINGLE',
       'vads_payment_src': 'EC',
       'vads_pays_ip': 'FR',
       'vads_presentation_date': '20201029093826',
       'vads_result': '00',
       'vads_result_message': 'Paiement réalisé avec succés.',
       'vads_sequence_number': '1',
       'vads_site_id': '12345678',
       'vads_threeds_auth_type': 'CHALLENGE',
       'vads_threeds_cavv': 'jG26AYSjvclBARFYSf/tXRmjGXM=',
       'vads_threeds_cavvAlgorithm': '2',
       'vads_threeds_eci': '02',
       'vads_threeds_enrolled': 'Y',
       'vads_threeds_error_code': '',
       'vads_threeds_exit_status': '10',
       'vads_threeds_sign_valid': '1',
       'vads_threeds_status': 'Y',
       'vads_threeds_xid': 'RFBSMkdWdFE0Wk15VWw0RkJjMzU=',
       'vads_tid': '001',
       'vads_trans_date': '20201029093825',
       'vads_trans_id': 'Vlco55',
       'vads_trans_status': 'AUTHORISED',
       'vads_trans_uuid': 'e8defc7bd32c418c93c4b2be676d2796',
       'vads_validation_mode': '0',
       'vads_version': 'V2',
       'vads_warranty_result': ''}
      return_content : None
      bank_status : Paiement réalisé avec succés.
      transaction_id : 3fd070
      order_id : 20201029093825_Vlco55
      test : True
      transaction_date : 2020-10-29 09:38:26+00:00

Code Style
==========

black is used to format the code, using thoses parameters:

    black --target-version py35 --skip-string-normalization --line-length 110

isort is used to format the imports, using those parameters:

    isort --profile black --line-length 110

pyupgrade is used to automatically upgrade syntax, using those parameters:

    pyupgrade --keep-percent-format --py37-plus

There is .pre-commit-config.yaml to use pre-commit to automatically run black,
isort and pyupgrade before commits. (execute `pre-commit install` to install
the git hook.)



