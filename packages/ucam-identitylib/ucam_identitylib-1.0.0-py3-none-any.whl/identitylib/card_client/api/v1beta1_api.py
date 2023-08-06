"""
    University Card API

      ## Introduction  The Card API allows access to information about University Cards.  The API broadly follows the principles of REST and strives to provide an interface that can be easily consumed by downstream systems.  The API is currently read-only, and does not expose any operations to create / update or delete University Card data.  ### Stability  This release of the Card API is a `beta` offering: a service we are moving towards live but which requires wider testing with a broader group of users. We consider the Card API as being at least as stable as the legacy card system which it aims to replace, so we encourage users to make use of the Card API rather than relying on the legacy card system.  ### Versioning  The Card API is versioned using url path prefixes in the format: `/v1beta1/cards`. This follows the pattern established by the [GCP API](https://cloud.google.com/apis/design/versioning). Breaking changes will not be made without a change in API major version, however non-breaking changes will be introduced without changes to the version path prefix. All changes will be documented in the project's [CHANGELOG](https://gitlab.developers.cam.ac.uk/uis/devops/iam/card-database/card-api/-/blob/master/CHANGELOG.md).  The available versions of the API are listed at the API's root.  ### Domain  The Card API has been designed to only expose information about University Cards and the identifiers which link a Card to a person. The API does not expose information about cardholders or the institutions that a cardholder belongs to. This is in order to combat domain crossover and to ensure the Card API does not duplicate information which is held and managed within systems such as Lookup, CamSIS or CHRIS.  It is expected that the Card API should be used alongside APIs such as Lookup which allow personal and institutional membership information to be retrieved. A tool has been written in order to allow efficient querying of the Card API using information contained within, CamSIS or CHRIS. [Usage and installation instructions for this tool can be found here](https://gitlab.developers.cam.ac.uk/uis/devops/iam/card-database/card-client).  ### Data source  The data exposed in the Card API is currently a mirror of data contained within the [Card Database](https://webservices.admin.cam.ac.uk/uc/). With data being synced from the Card Database to the Card API hourly.  In future, card data will be updated and created directly using the Card API so changes will be reflected in the Card API 'live' without this hourly sync.  ## Core entities  ### The `Card` Entity  The `Card` entity is a representation of a physical University Card. The entity contains fields indicating the status of the card and when the card has moved between different statuses. Cards held by individuals (such as students or staff) and temporary cards managed by institutions are both represented by the `Card` entity, with the former having a `cardType` of `MIFARE_PERSONAL` and the latter having a `cardType` of `MIFARE_TEMPORARY`.  Each card should have a set of `CardIdentifiers` which allow the card to be linked to an entity in another system (e.g. a person in Lookup), or record information about identifiers held within the card, such as Mifare ID.  The full `Card` entity contains a `cardNotes` field which holds a set of notes made by administrator users related to the card, as well as an `attributes` field which holds the data that is present on the physical presentation of a card. Operations which list many cards return `CardSummary` entities which omit these fields for brevity.  ### The `CardIdentifier` Entity  The `CardIdentifier` entity holds the `value` and `scheme` of a given identifier. The `value` field of a `CardIdentifier` is a simple ID string - e.g. `wgd23` or `000001`. The `scheme` field of a `CardIdentifier` indicates what system this identifier relates to or was issued by. This allows many identifiers which relate to different systems to be recorded against a single `Card`.  The supported schemes are: * `v1.person.identifiers.cam.ac.uk`: The CRSid of the person who holds this card * `person.v1.student-records.university.identifiers.cam.ac.uk`: The CamSIS identifier (USN) of the person who holds this card * `person.v1.human-resources.university.identifiers.cam.ac.uk`: The CHRIS identifier (staff number) of the person who holds this card * `person.v1.board-of-graduate-studies.university.identifiers.cam.ac.uk`: The Board of Graduate Studies identifier of the person who holds this card * `person.v1.legacy-card.university.identifiers.cam.ac.uk`: The legacy card holder ID for the person who holds this card * `mifare-identifier.v1.card.university.identifiers.cam.ac.uk`: The Mifare ID which is embedded in this card (this     identifier uniquely identifies a single card) * `mifare-number.v1.card.university.identifiers.cam.ac.uk`: The Mifare Number which is embedded in this card     (this identifier is a digest of card's legacy cardholder ID and issue number, so is not     guaranteed to be unique) * `card.v1.legacy-card.university.identifiers.cam.ac.uk`: The legacy card ID from the card database * `temporary-card.v1.card.university.identifiers.cam.ac.uk`: The temporary card ID from the card database * `photo.v1.photo.university.identifiers.cam.ac.uk`: The ID of the photo printed on this card * `barcode.v1.card.university.identifiers.cam.ac.uk`: The barcode printed on this card * `institution.v1.legacy-card.university.identifiers.cam.ac.uk`: The legacy institution ID from the card database (only populated on temporary cards)   ## Using the API  ### Auth  To authenticate against the Card API, an application must be registered within the API Service and granted access to the `University Card` product. Details of how to register an application and grant access to products can be found in the [API Service Getting Started Guide](https://developer.api.apps.cam.ac.uk/start-using-an-api).  #### Principal  Throughout this specification the term `principal` is used to describe the user or service who is making use of the API. When authenticating using the OAuth2 client credentials flow the principal shall be the application registered within the API Gateway. When authenticating using the authorization code flow, e.g. via a Single Page Application, the principal shall be the user who has authenticated and consented to give the application access to the data contained within this API - identified by their CRSid.  This specification references permissions which can be granted to any principal - please contact the API maintainers to grant a principal a specific permission.  ### Content Type  The Card API responds with JSON data. The `Content-Type` request header should be omitted or set to `application/json`. If an invalid `Content-Type` header is sent the API will respond with `415 Unsupported Media Type`.  ### Pagination  For all operations where multiple entities will be returned, the API will return a paginated result. This is to account for too many entities needing to be returned within a single response. A Paginated response has the structure:  ```json {   \"next\": \"https://<gateway_host>/card/v1beta1/cards/?cursor=cD0yMDIxLTAxL   \"previous\": null,   \"results\": [       ... the data for the current page   ] }  ```  The `next` field holds the url of the next page of results, containing a cursor which indicates to the API which page of results to return. If the `next` field is `null` no further results are available. The `previous` field can be used to navigate backwards through pages of results.  The `page_size` query parameter can be used to control the number of results to return. This defaults to 200 but can be set to a maximum of 500, if set to greater than this no error will be returned but only 500 results will be given in the response.    # noqa: E501

    The version of the OpenAPI document: v1beta1
    Contact: devops+cardapi@uis.cam.ac.uk
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from identitylib.card_client.api_client import ApiClient, Endpoint as _Endpoint
from identitylib.card_client.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from identitylib.card_client.model.api_exception import APIException
from identitylib.card_client.model.available_barcode import AvailableBarcode
from identitylib.card_client.model.card import Card
from identitylib.card_client.model.card_logo import CardLogo
from identitylib.card_client.model.card_request import CardRequest
from identitylib.card_client.model.inline_object import InlineObject
from identitylib.card_client.model.inline_object1 import InlineObject1
from identitylib.card_client.model.inline_response200 import InlineResponse200
from identitylib.card_client.model.inline_response2003 import InlineResponse2003
from identitylib.card_client.model.inline_response2004 import InlineResponse2004
from identitylib.card_client.model.inline_response2005 import InlineResponse2005
from identitylib.card_client.model.inline_response2006 import InlineResponse2006
from identitylib.card_client.model.validation_error import ValidationError


class V1beta1Api(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.v1beta1_available_barcodes_list_endpoint = _Endpoint(
            settings={
                'response_type': (InlineResponse2003,),
                'auth': [
                    'API Service OAuth2 Access Code',
                    'API Service OAuth2 Client Credentials'
                ],
                'endpoint_path': '/v1beta1/available-barcodes',
                'operation_id': 'v1beta1_available_barcodes_list',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'cursor',
                    'page_size',
                ],
                'required': [],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'cursor':
                        (str,),
                    'page_size':
                        (int,),
                },
                'attribute_map': {
                    'cursor': 'cursor',
                    'page_size': 'page_size',
                },
                'location_map': {
                    'cursor': 'query',
                    'page_size': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.v1beta1_available_barcodes_read_endpoint = _Endpoint(
            settings={
                'response_type': (AvailableBarcode,),
                'auth': [
                    'API Service OAuth2 Access Code',
                    'API Service OAuth2 Client Credentials'
                ],
                'endpoint_path': '/v1beta1/available-barcodes/{barcode}',
                'operation_id': 'v1beta1_available_barcodes_read',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'barcode',
                ],
                'required': [
                    'barcode',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'barcode':
                        (str,),
                },
                'attribute_map': {
                    'barcode': 'barcode',
                },
                'location_map': {
                    'barcode': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.v1beta1_card_logos_content_endpoint = _Endpoint(
            settings={
                'response_type': None,
                'auth': [
                    'API Service OAuth2 Access Code',
                    'API Service OAuth2 Client Credentials'
                ],
                'endpoint_path': '/v1beta1/card-logos/{id}/content',
                'operation_id': 'v1beta1_card_logos_content',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'id',
                ],
                'required': [
                    'id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'id':
                        (str,),
                },
                'attribute_map': {
                    'id': 'id',
                },
                'location_map': {
                    'id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.v1beta1_card_logos_list_endpoint = _Endpoint(
            settings={
                'response_type': (InlineResponse2004,),
                'auth': [
                    'API Service OAuth2 Access Code',
                    'API Service OAuth2 Client Credentials'
                ],
                'endpoint_path': '/v1beta1/card-logos',
                'operation_id': 'v1beta1_card_logos_list',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'cursor',
                    'page_size',
                ],
                'required': [],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'cursor':
                        (str,),
                    'page_size':
                        (int,),
                },
                'attribute_map': {
                    'cursor': 'cursor',
                    'page_size': 'page_size',
                },
                'location_map': {
                    'cursor': 'query',
                    'page_size': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.v1beta1_card_logos_read_endpoint = _Endpoint(
            settings={
                'response_type': (CardLogo,),
                'auth': [
                    'API Service OAuth2 Access Code',
                    'API Service OAuth2 Client Credentials'
                ],
                'endpoint_path': '/v1beta1/card-logos/{id}',
                'operation_id': 'v1beta1_card_logos_read',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'id',
                ],
                'required': [
                    'id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'id':
                        (str,),
                },
                'attribute_map': {
                    'id': 'id',
                },
                'location_map': {
                    'id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.v1beta1_card_requests_back_visualization_endpoint = _Endpoint(
            settings={
                'response_type': (file_type,),
                'auth': [
                    'API Service OAuth2 Access Code',
                    'API Service OAuth2 Client Credentials'
                ],
                'endpoint_path': '/v1beta1/card-requests/{id}/back-visualization',
                'operation_id': 'v1beta1_card_requests_back_visualization',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'id',
                ],
                'required': [
                    'id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'id':
                        (str,),
                },
                'attribute_map': {
                    'id': 'id',
                },
                'location_map': {
                    'id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'image/svg+xml',
                    'image/png',
                    'image/bmp'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.v1beta1_card_requests_front_visualization_endpoint = _Endpoint(
            settings={
                'response_type': (file_type,),
                'auth': [
                    'API Service OAuth2 Access Code',
                    'API Service OAuth2 Client Credentials'
                ],
                'endpoint_path': '/v1beta1/card-requests/{id}/front-visualization',
                'operation_id': 'v1beta1_card_requests_front_visualization',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'id',
                ],
                'required': [
                    'id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'id':
                        (str,),
                },
                'attribute_map': {
                    'id': 'id',
                },
                'location_map': {
                    'id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'image/svg+xml',
                    'image/png',
                    'image/bmp'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.v1beta1_card_requests_list_endpoint = _Endpoint(
            settings={
                'response_type': (InlineResponse2005,),
                'auth': [
                    'API Service OAuth2 Access Code',
                    'API Service OAuth2 Client Credentials'
                ],
                'endpoint_path': '/v1beta1/card-requests',
                'operation_id': 'v1beta1_card_requests_list',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'updated_at__lte',
                    'updated_at__gte',
                    'workflow_state',
                    'card_type',
                    'cursor',
                    'page_size',
                ],
                'required': [],
                'nullable': [
                ],
                'enum': [
                    'workflow_state',
                    'card_type',
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                    ('workflow_state',): {

                        "PENDING": "PENDING",
                        "HOLD": "HOLD",
                        "CANCELLED": "CANCELLED",
                        "CREATING_TODO": "CREATING_TODO",
                        "CREATING_INPROGRESS": "CREATING_INPROGRESS",
                        "CREATING_DONE": "CREATING_DONE"
                    },
                    ('card_type',): {

                        "PERSONAL": "MIFARE_PERSONAL",
                        "TEMPORARY": "MIFARE_TEMPORARY"
                    },
                },
                'openapi_types': {
                    'updated_at__lte':
                        (str,),
                    'updated_at__gte':
                        (str,),
                    'workflow_state':
                        (str,),
                    'card_type':
                        (str,),
                    'cursor':
                        (str,),
                    'page_size':
                        (int,),
                },
                'attribute_map': {
                    'updated_at__lte': 'updated_at__lte',
                    'updated_at__gte': 'updated_at__gte',
                    'workflow_state': 'workflow_state',
                    'card_type': 'card_type',
                    'cursor': 'cursor',
                    'page_size': 'page_size',
                },
                'location_map': {
                    'updated_at__lte': 'query',
                    'updated_at__gte': 'query',
                    'workflow_state': 'query',
                    'card_type': 'query',
                    'cursor': 'query',
                    'page_size': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.v1beta1_card_requests_read_endpoint = _Endpoint(
            settings={
                'response_type': (CardRequest,),
                'auth': [
                    'API Service OAuth2 Access Code',
                    'API Service OAuth2 Client Credentials'
                ],
                'endpoint_path': '/v1beta1/card-requests/{id}',
                'operation_id': 'v1beta1_card_requests_read',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'id',
                ],
                'required': [
                    'id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'id':
                        (str,),
                },
                'attribute_map': {
                    'id': 'id',
                },
                'location_map': {
                    'id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.v1beta1_card_requests_update_endpoint = _Endpoint(
            settings={
                'response_type': (InlineResponse2006,),
                'auth': [
                    'API Service OAuth2 Access Code',
                    'API Service OAuth2 Client Credentials'
                ],
                'endpoint_path': '/v1beta1/card-requests/{id}',
                'operation_id': 'v1beta1_card_requests_update',
                'http_method': 'PUT',
                'servers': None,
            },
            params_map={
                'all': [
                    'id',
                    'data',
                ],
                'required': [
                    'id',
                    'data',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'id':
                        (str,),
                    'data':
                        (InlineObject1,),
                },
                'attribute_map': {
                    'id': 'id',
                },
                'location_map': {
                    'id': 'path',
                    'data': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client
        )
        self.v1beta1_cards_back_visualization_endpoint = _Endpoint(
            settings={
                'response_type': (file_type,),
                'auth': [
                    'API Service OAuth2 Access Code',
                    'API Service OAuth2 Client Credentials'
                ],
                'endpoint_path': '/v1beta1/cards/{id}/back-visualization',
                'operation_id': 'v1beta1_cards_back_visualization',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'id',
                ],
                'required': [
                    'id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'id':
                        (str,),
                },
                'attribute_map': {
                    'id': 'id',
                },
                'location_map': {
                    'id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'image/png',
                    'image/svg+xml'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.v1beta1_cards_filter_endpoint = _Endpoint(
            settings={
                'response_type': (InlineResponse200,),
                'auth': [
                    'API Service OAuth2 Access Code',
                    'API Service OAuth2 Client Credentials'
                ],
                'endpoint_path': '/v1beta1/cards/filter',
                'operation_id': 'v1beta1_cards_filter',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'data',
                    'status',
                    'updated_at__lte',
                    'updated_at__gte',
                ],
                'required': [
                    'data',
                ],
                'nullable': [
                ],
                'enum': [
                    'status',
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                    ('status',): {

                        "ISSUED": "ISSUED",
                        "REVOKED": "REVOKED",
                        "RETURNED": "RETURNED",
                        "EXPIRED": "EXPIRED"
                    },
                },
                'openapi_types': {
                    'data':
                        (InlineObject,),
                    'status':
                        (str,),
                    'updated_at__lte':
                        (datetime,),
                    'updated_at__gte':
                        (datetime,),
                },
                'attribute_map': {
                    'status': 'status',
                    'updated_at__lte': 'updated_at__lte',
                    'updated_at__gte': 'updated_at__gte',
                },
                'location_map': {
                    'data': 'body',
                    'status': 'query',
                    'updated_at__lte': 'query',
                    'updated_at__gte': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client
        )
        self.v1beta1_cards_front_visualization_endpoint = _Endpoint(
            settings={
                'response_type': (file_type,),
                'auth': [
                    'API Service OAuth2 Access Code',
                    'API Service OAuth2 Client Credentials'
                ],
                'endpoint_path': '/v1beta1/cards/{id}/front-visualization',
                'operation_id': 'v1beta1_cards_front_visualization',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'id',
                ],
                'required': [
                    'id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'id':
                        (str,),
                },
                'attribute_map': {
                    'id': 'id',
                },
                'location_map': {
                    'id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'image/png',
                    'image/svg+xml'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.v1beta1_cards_list_endpoint = _Endpoint(
            settings={
                'response_type': (InlineResponse200,),
                'auth': [
                    'API Service OAuth2 Access Code',
                    'API Service OAuth2 Client Credentials'
                ],
                'endpoint_path': '/v1beta1/cards',
                'operation_id': 'v1beta1_cards_list',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'search',
                    'updated_at__lte',
                    'updated_at__gte',
                    'identifier',
                    'status',
                    'card_type',
                    'cursor',
                    'page_size',
                ],
                'required': [],
                'nullable': [
                ],
                'enum': [
                    'status',
                    'card_type',
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                    ('status',): {

                        "ISSUED": "ISSUED",
                        "REVOKED": "REVOKED",
                        "RETURNED": "RETURNED",
                        "EXPIRED": "EXPIRED"
                    },
                    ('card_type',): {

                        "PERSONAL": "MIFARE_PERSONAL",
                        "TEMPORARY": "MIFARE_TEMPORARY"
                    },
                },
                'openapi_types': {
                    'search':
                        (str,),
                    'updated_at__lte':
                        (str,),
                    'updated_at__gte':
                        (str,),
                    'identifier':
                        (str,),
                    'status':
                        (str,),
                    'card_type':
                        (str,),
                    'cursor':
                        (str,),
                    'page_size':
                        (int,),
                },
                'attribute_map': {
                    'search': 'search',
                    'updated_at__lte': 'updated_at__lte',
                    'updated_at__gte': 'updated_at__gte',
                    'identifier': 'identifier',
                    'status': 'status',
                    'card_type': 'card_type',
                    'cursor': 'cursor',
                    'page_size': 'page_size',
                },
                'location_map': {
                    'search': 'query',
                    'updated_at__lte': 'query',
                    'updated_at__gte': 'query',
                    'identifier': 'query',
                    'status': 'query',
                    'card_type': 'query',
                    'cursor': 'query',
                    'page_size': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.v1beta1_cards_read_endpoint = _Endpoint(
            settings={
                'response_type': (Card,),
                'auth': [
                    'API Service OAuth2 Access Code',
                    'API Service OAuth2 Client Credentials'
                ],
                'endpoint_path': '/v1beta1/cards/{id}',
                'operation_id': 'v1beta1_cards_read',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'id',
                ],
                'required': [
                    'id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'id':
                        (str,),
                },
                'attribute_map': {
                    'id': 'id',
                },
                'location_map': {
                    'id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )

    def v1beta1_available_barcodes_list(
        self,
        **kwargs
    ):
        """List available barcodes  # noqa: E501

          ## List Available Barcodes  Returns a list of barcodes which are available to be used by a new University Card.  ### Permissions  Only principals with the `CARD_DATA_READERS` permission are able to list available barcodes.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_available_barcodes_list(async_req=True)
        >>> result = thread.get()


        Keyword Args:
            cursor (str): The pagination cursor value.. [optional]
            page_size (int): Number of results to return per page.. [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            InlineResponse2003
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        return self.v1beta1_available_barcodes_list_endpoint.call_with_http_info(**kwargs)

    def v1beta1_available_barcodes_read(
        self,
        barcode,
        **kwargs
    ):
        """Get available barcode detail  # noqa: E501

        Returns a single Available Barcode by ID  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_available_barcodes_read(barcode, async_req=True)
        >>> result = thread.get()

        Args:
            barcode (str): A unique value identifying this available barcode.

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            AvailableBarcode
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['barcode'] = \
            barcode
        return self.v1beta1_available_barcodes_read_endpoint.call_with_http_info(**kwargs)

    def v1beta1_card_logos_content(
        self,
        id,
        **kwargs
    ):
        """Get card logo image content  # noqa: E501

          ## Get Card Logo Image Content  Redirects to the image content for a given card logo. Note that this endpoint will redirect to a temporary URL provided by the storage provider. This URL will timeout after a short period of time and therefore should not be persisted.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_logos_content(id, async_req=True)
        >>> result = thread.get()

        Args:
            id (str): A UUID string identifying this card logo.

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            None
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['id'] = \
            id
        return self.v1beta1_card_logos_content_endpoint.call_with_http_info(**kwargs)

    def v1beta1_card_logos_list(
        self,
        **kwargs
    ):
        """List card logos  # noqa: E501

          ## List Card Logos  Returns a list of card logo objects - representing logos which can be displayed on cards.  Each logo contains a `contentLink` which links to the image content for this logo. The rest of the object represents metadata about a logo.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_logos_list(async_req=True)
        >>> result = thread.get()


        Keyword Args:
            cursor (str): The pagination cursor value.. [optional]
            page_size (int): Number of results to return per page.. [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            InlineResponse2004
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        return self.v1beta1_card_logos_list_endpoint.call_with_http_info(**kwargs)

    def v1beta1_card_logos_read(
        self,
        id,
        **kwargs
    ):
        """Get card logo detail  # noqa: E501

          ## Get Card Logo  Returns a single card logo by UUID - containing metadata about a logo that can be present on a card.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_logos_read(id, async_req=True)
        >>> result = thread.get()

        Args:
            id (str): A UUID string identifying this card logo.

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            CardLogo
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['id'] = \
            id
        return self.v1beta1_card_logos_read_endpoint.call_with_http_info(**kwargs)

    def v1beta1_card_requests_back_visualization(
        self,
        id,
        **kwargs
    ):
        """Returns a representation of the back of the card request  # noqa: E501

          ## Get card back visualization  Returns a visualization of the back of this card in png or svg format.  Currently a placeholder is used to represent the barcode printed on the back of the card, this will be replaced with a valid barcode as a piece of follow-up work.  Temporary cards cannot be visualized, and will simply return a blank image.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view visualization of any card contained within the card system. Principals without this permission are only able to view the visualization for a card that they own. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_back_visualization(id, async_req=True)
        >>> result = thread.get()

        Args:
            id (str): A UUID string identifying this card request.

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            file_type
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['id'] = \
            id
        return self.v1beta1_card_requests_back_visualization_endpoint.call_with_http_info(**kwargs)

    def v1beta1_card_requests_front_visualization(
        self,
        id,
        **kwargs
    ):
        """Returns a representation of the front of this card request  # noqa: E501

          ## Get card front visualization  Returns a visualization of the front of this card in png or svg format. Makes use of the Photo API to fetch the photo of the cardholder used on this card. In cases where this card makes use of an out-of-date photo of the cardholder imported from the legacy card system, the Photo may not be available, in which case a placeholder is displayed.  Temporary cards cannot be visualized, and will simply return a blank image.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view visualization of any card contained within the card system. Principals without this permission are only able to view the visualization for a card that they own. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_front_visualization(id, async_req=True)
        >>> result = thread.get()

        Args:
            id (str): A UUID string identifying this card request.

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            file_type
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['id'] = \
            id
        return self.v1beta1_card_requests_front_visualization_endpoint.call_with_http_info(**kwargs)

    def v1beta1_card_requests_list(
        self,
        **kwargs
    ):
        """List card requests  # noqa: E501

          ## List Card Requests  Returns a list of card request objects - representing requests for card creation.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view all card requests contained within the card system. Without this permission only card requests owned by the authenticated principal will be returned. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_list(async_req=True)
        >>> result = thread.get()


        Keyword Args:
            updated_at__lte (str): [optional]
            updated_at__gte (str): [optional]
            workflow_state (str): Filter card requests by their current workflow state. [optional]
            card_type (str): Filter by the type of card. [optional]
            cursor (str): The pagination cursor value.. [optional]
            page_size (int): Number of results to return per page.. [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            InlineResponse2005
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        return self.v1beta1_card_requests_list_endpoint.call_with_http_info(**kwargs)

    def v1beta1_card_requests_read(
        self,
        id,
        **kwargs
    ):
        """Get card request detail  # noqa: E501

          ## Get Card Request  Returns a single card request by UUID - containing metadata about a request for card creation.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view all card requests contained within the card system. Without this permission only card requests owned by the authenticated principal are visible. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_read(id, async_req=True)
        >>> result = thread.get()

        Args:
            id (str): A UUID string identifying this card request.

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            CardRequest
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['id'] = \
            id
        return self.v1beta1_card_requests_read_endpoint.call_with_http_info(**kwargs)

    def v1beta1_card_requests_update(
        self,
        id,
        data,
        **kwargs
    ):
        """Updates the card request  # noqa: E501

          ## Update the card request  This method allows a client to submit an action in the request body and optional identifier for a given card request. The available actions are `add`, `start`, `abandon` and `complete`.   For the `complete` action, the client can also append identifiers which associates the physically created cards to the card record - for example the card UID which is  pre-encoded into the card by the manufacturer.  The `complete` action returns the UUID of the created `card` entity.  ### Permissions  Principals with the `CARD_CREATOR` permission will be able to affect this endpoint.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_card_requests_update(id, data, async_req=True)
        >>> result = thread.get()

        Args:
            id (str): A UUID string identifying this card request.
            data (InlineObject1):

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            InlineResponse2006
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['id'] = \
            id
        kwargs['data'] = \
            data
        return self.v1beta1_card_requests_update_endpoint.call_with_http_info(**kwargs)

    def v1beta1_cards_back_visualization(
        self,
        id,
        **kwargs
    ):
        """Returns a representation of the back of the card  # noqa: E501

          ## Get card back visualization  Returns a visualization of the back of this card in png or svg format.  Currently a placeholder is used to represent the barcode printed on the back of the card, this will be replaced with a valid barcode as a piece of follow-up work.  Temporary cards cannot be visualized, and will simply return a blank image.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view visualization of any card contained within the card system. Principals without this permission are only able to view the visualization for a card that they own. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_back_visualization(id, async_req=True)
        >>> result = thread.get()

        Args:
            id (str): A UUID string identifying this card.

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            file_type
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['id'] = \
            id
        return self.v1beta1_cards_back_visualization_endpoint.call_with_http_info(**kwargs)

    def v1beta1_cards_filter(
        self,
        data,
        **kwargs
    ):
        """Filter cards by identifiers  # noqa: E501

          ## Filter cards by Identifiers  Returns the cards related to the given batch of identifiers. This is useful for finding a set of cards based on a batch of entities from another system. For example, finding cards for members of a group in Lookup can be achieved by first fetching all members of the group and their crsids from Lookup and then using this endpoint to find all cards based on those crsids.  Identifiers should be provided in the format `<value>@<scheme>`, but if the scheme is not provided the scheme shall be assumed to be `person.crs.identifiers.uis.cam.ac.uk`. See above for the list of supported schemes.  __Note__: the number of identifiers which can be sent in each request is limited to 50, if more that 50 unique identifiers are sent in a single request a `400` error response will be returned. If cards need to be filtered by more than 50 identifiers, multiple request should be made with the identifiers split into batches of 50.  A `status` to filter cards can optionally be included in the body or as a query param. If not included cards of all statuses are returned.  Although this endpoint uses the `POST` method, no data is created. `POST` is used to allow the set of identifiers to be provided in the body and therefore avoid problems caused by query-string length limits.  This endpoint returns a paginated response object (as described above), but will not actually perform pagination due to the overall limit on the number of identifiers that can be queried by. Therefore the `next` and `previous` fields will always be `null` and the `page_size` and `cursor` query parameters will not be honoured.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to filter all cards contained within the card system. Without this permission only cards owned by the authenticated principal will be returned. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_filter(data, async_req=True)
        >>> result = thread.get()

        Args:
            data (InlineObject):

        Keyword Args:
            status (str): Filter cards by their current status (status in the body takes precedence over this query parameter). [optional]
            updated_at__lte (datetime): Filter updatedAt by IsoDateTime less than. [optional]
            updated_at__gte (datetime): Filter updatedAt by IsoDateTime greater than. [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            InlineResponse200
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['data'] = \
            data
        return self.v1beta1_cards_filter_endpoint.call_with_http_info(**kwargs)

    def v1beta1_cards_front_visualization(
        self,
        id,
        **kwargs
    ):
        """Returns a representation of the front of this card  # noqa: E501

          ## Get card front visualization  Returns a visualization of the front of this card in png or svg format. Makes use of the Photo API to fetch the photo of the cardholder used on this card. In cases where this card makes use of an out-of-date photo of the cardholder imported from the legacy card system, the Photo may not be available, in which case a placeholder is displayed.  Temporary cards cannot be visualized, and will simply return a blank image.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view visualization of any card contained within the card system. Principals without this permission are only able to view the visualization for a card that they own. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_front_visualization(id, async_req=True)
        >>> result = thread.get()

        Args:
            id (str): A UUID string identifying this card.

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            file_type
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['id'] = \
            id
        return self.v1beta1_cards_front_visualization_endpoint.call_with_http_info(**kwargs)

    def v1beta1_cards_list(
        self,
        **kwargs
    ):
        """List cards  # noqa: E501

         ## List Cards  Allows current and historic University Cards to be listed.  By default (without any URL parameters included) this method will return all cards, including temporary cards and cards that have expired / been revoked.  Query parameters can be used to refine the cards that are returned. For example, to fetch cards which have been issued and are therefore currently active we can add the query parameter: `status=ISSUED`.  If we want to find Cards with a specific identifier we can specify that identifier as a query parameter as well. For example, adding the following to the query string will return all revoked cards with the mifare ID '123':  `status=REVOKED&identifier=123@<mifare id scheme>`. Identifiers should be provided in the format `<value>@<scheme>`, but if the scheme is not provided the scheme shall be assumed to be the CRSid. See above for the list of supported schemes.  In the case of querying by mifare identifier, any leading zeros within the identifier value included in the query will be ignored - so querying with `identifier=0000000123@<mifare id scheme>` and `identifier=123@<mifare id scheme>` will return the same result.  Alternately the `search` query parameter can be used to search all cards by a single identifier value regardless of the scheme of that identifier.  If cards for multiple identifiers need to be fetched, use the `/cards/filter/` endpoint documented below.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view all cards contained within the card system. Without this permission only cards owned by the authenticated principal will be returned. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_list(async_req=True)
        >>> result = thread.get()


        Keyword Args:
            search (str): A search term.. [optional]
            updated_at__lte (str): [optional]
            updated_at__gte (str): [optional]
            identifier (str): Filter cards by an identifier in the format {value}@{scheme}. [optional]
            status (str): Filter cards by their current status. [optional]
            card_type (str): Filter by the type of card. [optional]
            cursor (str): The pagination cursor value.. [optional]
            page_size (int): Number of results to return per page.. [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            InlineResponse200
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        return self.v1beta1_cards_list_endpoint.call_with_http_info(**kwargs)

    def v1beta1_cards_read(
        self,
        id,
        **kwargs
    ):
        """Get card detail  # noqa: E501

          ## Get Card Detail  Allows the detail of a single Card to be retrieved by ID. The Card entity returned contains the same information as presented in the filter and list card operations above, but also contains an array of `cardNotes` containing notes made by administrator users related to the current card.  ### Permissions  Principals with the `CARD_DATA_READERS` permission are able to view the card detail of any card contained within the card system. Principals without this permission are only able to view the card detail for a card that they own. Ownership is determined based on the principal's identifier matching an identifier contained within a given card record.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.v1beta1_cards_read(id, async_req=True)
        >>> result = thread.get()

        Args:
            id (str): A UUID string identifying this card.

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            Card
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['id'] = \
            id
        return self.v1beta1_cards_read_endpoint.call_with_http_info(**kwargs)

