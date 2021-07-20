from __future__ import annotations

from collections import OrderedDict
from sqlite3.dbapi2 import Date

from .base import ApiBase
import logging
from datetime import datetime


logger = logging.getLogger(__name__)

class InventoryItems(ApiBase):

    DEFAULT_SUBSIDIARY='2'

    SIMPLE_FIELDS = [
        'costEstimateUnits',
        'costingMethodDisplay',
        'costUnits',
        'currency',
        'displayName',
        'featuredDescription',
        'handlingCostUnits',
        'hazmatHazardClass',
        'hazmatId',
        'hazmatItemUnits',
        'hazmatShippingName',
        'itemId',
        'manufacturer',
        'manufacturerAddr1',
        'manufacturerCity',
        'manufacturerState',
        'manufacturerTariff',
        'manufacturerTaxId',
        'manufacturerZip',
        'matrixItemNameTemplate',
        'metaTagHtml',
        'minimumQuantityUnits',
        'mpn',
        'nexTagCategory',
        'noPriceMessage',
        'outOfStockMessage',
        'pageTitle',
        'preferredStockLevelUnits',
        'purchaseDescription',
        'quantityAvailableUnits',
        'quantityCommittedUnits',
        'quantityOnHandUnits',
        'quantityOnOrderUnits',
        'quantityReorderUnits',
        'relatedItemsDescription',
        'reorderPointUnits',
        'safetyStockLevelUnits',
        'salesDescription',
        'scheduleBNumber',
        'searchKeywords',
        'shippingCostUnits',
        'shoppingDotComCategory',
        'specialsDescription',
        'stockDescription',
        'storeDescription',
        'storeDetailedDescription',
        'storeDisplayName',
        'upcCode',
        'urlComponent',
        'vendorName',
        'weightUnits',
        'backwardConsumptionDays',
        'demandTimeFence',
        'forwardConsumptionDays',
        'futureHorizon',
        'invtCountInterval',
        'leadTime',
        'maximumQuantity',
        'minimumQuantity',
        'periodicLotSizeDays',
        'reorderMultiple',
        'rescheduleInDays',
        'rescheduleOutDays',
        'safetyStockLevelDays',
        'scheduleBQuantity',
        'shopzillaCategoryId',
        'supplyTimeFence',
        'createdDate',
        'dateConvertedToInv',
        'lastInvtCountDate',
        'lastModifiedDate',
        'nextInvtCountDate',
        'averageCost',
        'conversionRate',
        'cost',
        'costEstimate',
        'defaultReturnCost',
        'demandModifier',
        'fixedLotSize',
        'handlingCost',
        'hazmatItemUnitsQty',
        'lastPurchasePrice',
        'lowerWarningLimit',
        'maxDonationAmount',
        'onHandValueMli',
        'preferredStockLevel',
        'preferredStockLevelDays',
        'purchaseOrderAmount',
        'purchaseOrderQuantity',
        'purchaseOrderQuantityDiff',
        'quantityAvailable',
        'quantityBackOrdered',
        'quantityCommitted',
        'quantityOnHand',
        'quantityOnOrder',
        'rate',
        'receiptAmount',
        'receiptQuantity',
        'receiptQuantityDiff',
        'reorderPoint',
        'safetyStockLevel',
        'shippingCost',
        'totalValue',
        'transferPrice',
        'upperWarningLimit',
        'vsoePrice',
        'weight',
        'weightUnit',
        'autoLeadTime',
        'autoPreferredStockLevel',
        'autoReorderPoint',
        'availableToPartners',
        'contingentRevenueHandling',
        'copyDescription',
        'deferRevRec',
        'directRevenuePosting',
        'dontShowPrice',
        'enableCatchWeight',
        'enforceMinQtyInternally',
        'excludeFromSitemap',
        'includeChildren',
        'isDonationItem',
        'isDropShipItem',
        'isGcoCompliant',
        'isHazmatItem',
        'isInactive',
        'isOnline',
        'isSpecialOrderItem',
        'isStorePickupAllowed',
        'isTaxable',
        'matchBillToReceipt',
        'multManufactureAddr',
        'offerSupport',
        'onSpecial',
        'pricesIncludeTax',
        'producer',
        'roundUpAsComponent',
        'seasonalDemand',
        'shipIndividually',
        'showDefaultDonationAmount',
        'trackLandedCost',
        'useBins',
        'useMarginalRates',
        'vsoeDelivered',
    ]

    RECORD_REF_FIELDS = [
        'alternateDemandSourceItem',
        'assetAccount',
        'billExchRateVarianceAcct',
        'billingSchedule',
        'billPriceVarianceAcct',
        'billQtyVarianceAcct',
        'class',
        'cogsAccount',
        'consumptionUnit',
        'costCategory',
        'createRevenuePlansOn',
        'customForm',
        'defaultItemShipMethod',
        'deferredRevenueAccount',
        'demandSource',
        'department',
        'distributionCategory',
        'distributionNetwork',
        'dropshipExpenseAccount',
        'expenseAccount',
        'gainLossAccount',
        'incomeAccount',
        'intercoCogsAccount',
        'intercoDefRevAccount',
        'intercoIncomeAccount',
        'issueProduct',
        'itemRevenueCategory',
        'location',
        'parent',
        'planningItemCategory',
        'preferredLocation',
        'pricingGroup',
        'purchasePriceVarianceAcct',
        'purchaseTaxCode',
        'purchaseUnit',
        'quantityPricingSchedule',
        'revenueAllocationGroup',
        'revenueRecognitionRule',
        'revRecForecastRule',
        'revReclassFXAccount',
        'revRecSchedule',
        'salesTaxCode',
        'saleUnit',
        'secondaryBaseUnit',
        'secondaryConsumptionUnit',
        'secondaryPurchaseUnit',
        'secondarySaleUnit',
        'secondaryStockUnit',
        'secondaryUnitsType',
        'shipPackage',
        'softDescriptor',
        'stockUnit',
        'storeDisplayImage',
        'storeDisplayThumbnail',
        'storeItemTemplate',
        'supplyLotSizingMethod',
        'supplyReplenishmentMethod',
        'supplyType',
        'taxSchedule',
        'unitsType',
        'vendor'
    ]

    READ_ONLY_FIELDS = ['internalId', 'createdDate', 'lastModifiedDate', 'currency', 'averageCost',
                        'lastPurchasePrice', 'totalValue']


    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='InventoryItem')

    def blank(self, externalId) -> OrderedDict:

        blank = OrderedDict()
        blank.externalId = externalId
        blank.customFieldList = self.ns_client.CustomFieldList([])
        blank.subsidiaryList = {'recordRef': [self.ns_client.RecordRef(**({'internalId': '2'}))]}
        blank.taxSchedule = self.ns_client.RecordRef(**({'internalId': '2'}))

        return blank

    def post(self, data) -> OrderedDict:
        if data.externalId in ['', None, 0, [], {}]:
            raise ValueError("externalId is required")

        inventoryitem = self.ns_client.InventoryItem(externalId=data.externalId)

        self.build_simple_fields(self.SIMPLE_FIELDS, data, inventoryitem)

        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, inventoryitem)

        self.build_custom_fields(data, inventoryitem)

        self.build_bin_list(data, inventoryitem)

        self.remove_readonly(inventoryitem, self.READ_ONLY_FIELDS)

        if hasattr(data, 'subsidiaryList'):
            inventoryitem.subsidiaryList = data.subsidiaryList
        else:
            inventoryitem.subsidiaryList = self.blank().subsidiaryList

        logger.debug('able to create inventoryitem = %s', inventoryitem)
        return self.ns_client.upsert(inventoryitem)


    def build_bin_list(self, data, inventoryitem) -> OrderedDict:

        if not hasattr(data, 'binNumberList'):
            inventoryitem.useBins = True

            inventoryitem.binNumberList = self.ns_client.InventoryItemBinNumberList()
            inventoryitem.binNumberList.binNumber = []
            inventoryitem.binNumberList.binNumber.append(self.ns_client.InventoryItemBinNumber())
            inventoryitem.binNumberList.binNumber[0].binNumber = self.ns_client.RecordRef(internalId='7710')
            inventoryitem.binNumberList.binNumber[0].location = '1'

        logger.debug('breakpoint')
