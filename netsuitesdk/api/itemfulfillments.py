from collections import OrderedDict
from sqlite3.dbapi2 import Date

from .base import ApiBase
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ItemFulfillments(ApiBase):
    SIMPLE_FIELDS = [
        'generateIntegratedShipperLabel',
        'holdAtLocationFedEx',
        'insideDeliveryFedEx',
        'insidePickupFedEx',
        'isCargoAircraftOnlyFedEx',
        'isRoutedExportTransactionUps',
        'partiesToTransactionUps',
        'saturdayDeliveryFedEx',
        'saturdayDeliveryUps',
        'saturdayPickupFedex',
        'sendBackupEmailFedEx',
        'sendBackupEmailUps',
        'sendShipNotifyEmailFedEx',
        'sendShipNotifyEmailUps',
        'shipIsResidential',
        'signatureHomeDeliveryFedEx',
        'blanketEndDateUps',
        'blanketStartDateUps',
        'createdDate',
        'homeDeliveryDateFedEx',
        'lastModifiedDate',
        'licenseDateUps',
        'packedDate',
        'pickedDate',
        'shipDateFedEx',
        'shippedDate',
        'tranDate',
        'handlingCost',
        'shipmentWeightFedEx',
        'shipmentWeightUps',
        'shippingCost',
        'termsFreightChargeFedEx',
        'termsInsuranceChargeFedEx',
        'b13aStatementDataFedEx',
        'backupEmailAddressFedEx',
        'backupEmailAddressUps',
        'bookingConfirmationNumFedEx',
        'carrierIdUps',
        'eccNumberUps',
        'entryNumberUps',
        'halAddr1FedEx',
        'halAddr2FedEx',
        'halAddr3FedEx',
        'halCityFedEx',
        'halCountryFedEx',
        'halPhoneFedEx',
        'halStateFedEx',
        'halZipFedEx',
        'inbondCodeUps',
        'intlExemptionNumFedEx',
        'licenseNumberUps',
        'memo',
        'recipientTaxIdUps',
        'shipNotifyEmailAddress2Ups',
        'shipNotifyEmailAddressFedEx,'
        'shipNotifyEmailAddressUps',
        'shipNotifyEmailMessageUps',
        'thirdPartyAcctFedEx',
        'thirdPartyAcctUps',
        'thirdPartyZipcodeUps',
        'tranId'
    ]

    RECORD_REF_FIELDS = [
        'createdFrom'
        'customForm'
        'entity'
        'partner'
        'postingPeriod'
        'requestedBy'
        'shipAddressList'
        'shipMethod'
        'transferLocation'   
    ]


    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='ItemFulfillment')