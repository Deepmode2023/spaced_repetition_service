from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..models import RepetitionAggragetion
from ..models.type import DateType


@dataclass(eq=False, frozen=True)
class RepetitionRepository(ABC):
    @abstractmethod
    async def get_all_repetitions(
        start_date: DateType,
        end_date: DateType,
        limit: int,
        offset: int,
    ) -> List[RepetitionAggragetion]:
        """
        Retrieves all repetitions within the specified date range.

        Args:
            start_date (DateType): The start of the date range.
            end_date (DateType): The end of the date range.
            limit (int): Maximum number of repetitions to return.
            offset (int): Number of repetitions to skip.

        Returns:
            List[RepetitionAggragetion]: A list of repetitions.

        Raises:
            RepetitionAlreadyExistsError: If a repetition with the same title already exists.
            SomeOtherError: If another error occurs.
        """
        ...

    @abstractmethod
    async def update_repetition(
        repetition_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        document_link: Optional[str] = None,
        slugs: Optional[list[str]] = [],
    ) -> bool:
        """
        Updates an existing repetition with the provided data.

        Args:
            repetition_id (str): The ID of the user who owns the repetition.
            title (Optional[str], optional): The new title for the repetition. Defaults to None.
            description (Optional[str], optional): The new description for the repetition. Defaults to None.
            document_link (Optional[str], optional): The new document link for the repetition. Defaults to None.
            slug (Optional[list[str]], optional): The new slug for the repetition. Defaults to None.

        Returns:
            bool: True if the update was successful, False otherwise.

        Raises:
            RepetitionNotFoundError: If the repetition to be updated does not exist.
            RepetitionAlreadyExistsError: If the new title or slug conflicts with an existing repetition.
            ValidationError: If the provided data is invalid.
            DatabaseError: If there is an issue interacting with the database.
        """
        ...

    @abstractmethod
    async def create_repetition(
        title: str,
        user_id: str,
        description: Optional[str] = None,
        document_link: Optional[str] = None,
        slugs: Optional[list[str]] = [],
    ) -> RepetitionAggragetion:
        """
        Creates a new repetition.

        Args:
            title (str): The title of the repetition.
            user_id (str): The ID of the user creating the repetition.
            description (Optional[str], optional): A description of the repetition. Defaults to None.
            document_link (Optional[str], optional): A link to a related document. Defaults to None.
            slug (Optional[list[str]], optional): A unique slug for the repetition. Defaults to None.

        Returns:
            RepetitionAggragetion: The created repetition object.

        Raises:
            RepetitionAlreadyExistsError: If a repetition with the same title or slug already exists.
            DatabaseError: If there is an issue interacting with the database.
            ValidationError: If the input data does not meet the required criteria.
        """
        ...

    @abstractmethod
    async def successful_repetition(repetition_id: str) -> bool:
        """
        Marks a repetition as successful.

        Args:
            repetition_id (str): The unique identifier of the repetition to mark as successful.

        Returns:
            bool: True if the operation was successful, False otherwise.

        Raises:
            RepetitionNotFoundError: If the repetition with the given ID does not exist.
            DatabaseError: If there is an issue interacting with the database.
        """
        ...

    @abstractmethod
    async def unsuccessful_repetition(repetition_id: str) -> bool:
        """
        Marks a repetition as unsuccessful.

        Args:
            repetition_id (str): The unique identifier of the repetition to mark as unsuccessful.

        Returns:
            bool: True if the operation was successful, False otherwise.

        Raises:
            RepetitionNotFoundError: If the repetition with the given ID does not exist.
            DatabaseError: If there is an issue interacting with the database.
        """
        ...
