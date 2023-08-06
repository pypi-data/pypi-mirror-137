"""
Type annotations for alexaforbusiness service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_alexaforbusiness.client import AlexaForBusinessClient
    from types_aiobotocore_alexaforbusiness.paginator import (
        ListBusinessReportSchedulesPaginator,
        ListConferenceProvidersPaginator,
        ListDeviceEventsPaginator,
        ListSkillsPaginator,
        ListSkillsStoreCategoriesPaginator,
        ListSkillsStoreSkillsByCategoryPaginator,
        ListSmartHomeAppliancesPaginator,
        ListTagsPaginator,
        SearchDevicesPaginator,
        SearchProfilesPaginator,
        SearchRoomsPaginator,
        SearchSkillGroupsPaginator,
        SearchUsersPaginator,
    )

    session = get_session()
    with session.create_client("alexaforbusiness") as client:
        client: AlexaForBusinessClient

        list_business_report_schedules_paginator: ListBusinessReportSchedulesPaginator = client.get_paginator("list_business_report_schedules")
        list_conference_providers_paginator: ListConferenceProvidersPaginator = client.get_paginator("list_conference_providers")
        list_device_events_paginator: ListDeviceEventsPaginator = client.get_paginator("list_device_events")
        list_skills_paginator: ListSkillsPaginator = client.get_paginator("list_skills")
        list_skills_store_categories_paginator: ListSkillsStoreCategoriesPaginator = client.get_paginator("list_skills_store_categories")
        list_skills_store_skills_by_category_paginator: ListSkillsStoreSkillsByCategoryPaginator = client.get_paginator("list_skills_store_skills_by_category")
        list_smart_home_appliances_paginator: ListSmartHomeAppliancesPaginator = client.get_paginator("list_smart_home_appliances")
        list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
        search_devices_paginator: SearchDevicesPaginator = client.get_paginator("search_devices")
        search_profiles_paginator: SearchProfilesPaginator = client.get_paginator("search_profiles")
        search_rooms_paginator: SearchRoomsPaginator = client.get_paginator("search_rooms")
        search_skill_groups_paginator: SearchSkillGroupsPaginator = client.get_paginator("search_skill_groups")
        search_users_paginator: SearchUsersPaginator = client.get_paginator("search_users")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import DeviceEventTypeType, EnablementTypeFilterType, SkillTypeFilterType
from .type_defs import (
    FilterTypeDef,
    ListBusinessReportSchedulesResponseTypeDef,
    ListConferenceProvidersResponseTypeDef,
    ListDeviceEventsResponseTypeDef,
    ListSkillsResponseTypeDef,
    ListSkillsStoreCategoriesResponseTypeDef,
    ListSkillsStoreSkillsByCategoryResponseTypeDef,
    ListSmartHomeAppliancesResponseTypeDef,
    ListTagsResponseTypeDef,
    PaginatorConfigTypeDef,
    SearchDevicesResponseTypeDef,
    SearchProfilesResponseTypeDef,
    SearchRoomsResponseTypeDef,
    SearchSkillGroupsResponseTypeDef,
    SearchUsersResponseTypeDef,
    SortTypeDef,
)

__all__ = (
    "ListBusinessReportSchedulesPaginator",
    "ListConferenceProvidersPaginator",
    "ListDeviceEventsPaginator",
    "ListSkillsPaginator",
    "ListSkillsStoreCategoriesPaginator",
    "ListSkillsStoreSkillsByCategoryPaginator",
    "ListSmartHomeAppliancesPaginator",
    "ListTagsPaginator",
    "SearchDevicesPaginator",
    "SearchProfilesPaginator",
    "SearchRoomsPaginator",
    "SearchSkillGroupsPaginator",
    "SearchUsersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListBusinessReportSchedulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListBusinessReportSchedules)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#listbusinessreportschedulespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBusinessReportSchedulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListBusinessReportSchedules.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#listbusinessreportschedulespaginator)
        """


class ListConferenceProvidersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListConferenceProviders)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#listconferenceproviderspaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListConferenceProvidersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListConferenceProviders.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#listconferenceproviderspaginator)
        """


class ListDeviceEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListDeviceEvents)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#listdeviceeventspaginator)
    """

    async def paginate(
        self,
        *,
        DeviceArn: str,
        EventType: DeviceEventTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeviceEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListDeviceEvents.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#listdeviceeventspaginator)
        """


class ListSkillsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListSkills)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#listskillspaginator)
    """

    async def paginate(
        self,
        *,
        SkillGroupArn: str = ...,
        EnablementType: EnablementTypeFilterType = ...,
        SkillType: SkillTypeFilterType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSkillsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListSkills.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#listskillspaginator)
        """


class ListSkillsStoreCategoriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListSkillsStoreCategories)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#listskillsstorecategoriespaginator)
    """

    async def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSkillsStoreCategoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListSkillsStoreCategories.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#listskillsstorecategoriespaginator)
        """


class ListSkillsStoreSkillsByCategoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListSkillsStoreSkillsByCategory)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#listskillsstoreskillsbycategorypaginator)
    """

    async def paginate(
        self, *, CategoryId: int, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSkillsStoreSkillsByCategoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListSkillsStoreSkillsByCategory.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#listskillsstoreskillsbycategorypaginator)
        """


class ListSmartHomeAppliancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListSmartHomeAppliances)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#listsmarthomeappliancespaginator)
    """

    async def paginate(
        self, *, RoomArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSmartHomeAppliancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListSmartHomeAppliances.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#listsmarthomeappliancespaginator)
        """


class ListTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListTags)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#listtagspaginator)
    """

    async def paginate(
        self, *, Arn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.ListTags.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#listtagspaginator)
        """


class SearchDevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.SearchDevices)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#searchdevicespaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        SortCriteria: Sequence["SortTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.SearchDevices.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#searchdevicespaginator)
        """


class SearchProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.SearchProfiles)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#searchprofilespaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        SortCriteria: Sequence["SortTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.SearchProfiles.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#searchprofilespaginator)
        """


class SearchRoomsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.SearchRooms)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#searchroomspaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        SortCriteria: Sequence["SortTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchRoomsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.SearchRooms.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#searchroomspaginator)
        """


class SearchSkillGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.SearchSkillGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#searchskillgroupspaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        SortCriteria: Sequence["SortTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchSkillGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.SearchSkillGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#searchskillgroupspaginator)
        """


class SearchUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.SearchUsers)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#searchuserspaginator)
    """

    async def paginate(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        SortCriteria: Sequence["SortTypeDef"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Paginator.SearchUsers.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/paginators.html#searchuserspaginator)
        """
