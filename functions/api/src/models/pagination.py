from enum import Enum

from pydantic import BaseModel


class PaginationSortType(str, Enum):
    """
    The pagination sort type enum.
    """

    ASC = "ASC"
    DESC = "DESC"


class PaginatedEntityDto(BaseModel):
    """
    The paginated entity dto
    """

    entities: list[object]
    page: int
    items: int
    total_pages: int
    total_items: int
    previous_page: str = None
    next_page: str = None

    def generate_pagination_url(
        page_number: int,
        total_pages: int,
        service_url: str,
        page_size: int,
        sort_order: PaginationSortType,
    ) -> str:
        """
        Generates the pagination url.

        Args:
            page_number (int): The page number to be mapped.
            total_pages (int): The total pages.
            service_url (str): The service URL.

        Returns:
            str: The page url path.
        """
        previous_page = None
        next_page = None

        if page_number - 1 != 0:
            previous_page = f"{service_url}?page={page_number - 1}&page_size={page_size}&sort={sort_order}"
        if page_number + 1 <= total_pages:
            next_page = f"{service_url}?page={page_number + 1}&page_size={page_size}&sort={sort_order}"

        return previous_page, next_page
