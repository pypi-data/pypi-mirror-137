import json
import typing
from typing import Optional, Union, List, Dict
from . import root
from abc import ABC


class Bucket(root.AbstractDesktopObject, ABC):
    """
    Abstract base class for user accounts.
    """
    pass


class AWSBucket(Bucket):
    """
    Represents an AWS Bucket in the HEA desktop. Contains functions that allow access and setting of the value.
    """
    def __init__(self):
        super().__init__()
        self.__arn: Optional[str] = None
        self.__s3_uri: Optional[str] = None
        self.__is_encrypted: Optional[bool] = None
        self.__is_versioned: Optional[bool] = None
        self.__region: Optional[str] = None
        self.__size: Optional[float] = None
        self.__object_count: Optional[int] = None
        self.__tags: List[Dict[str, str]] = []
        self.__permission_policy: Optional[Dict] = None

    @property
    def arn(self) -> Optional[str]:
        """Returns the aws arn str for identifying resources on aws"""
        return self.__arn

    @arn.setter
    def arn(self, arn: Optional[str]) -> None:
        """Sets the numerical account identifier"""
        self.__arn = str(arn) if arn is not None else None

    @property
    def s3_uri(self) -> Optional[str]:
        """the aws arn str for identifying resources on aws"""
        return self.__s3_uri

    @s3_uri.setter
    def s3_uri(self, s3_uri: Optional[str]) -> None:
        """Sets the aws s3 uri str"""
        self.__s3_uri = str(s3_uri) if s3_uri is not None else None

    @property
    def is_encrypted(self) -> Optional[bool]:
        """Returns the is encrypted flag for bucket"""
        return self.__is_encrypted

    @is_encrypted.setter
    def is_encrypted(self, is_encrypted: Optional[bool]) -> None:
        """Sets the is encrypted flag for bucket"""
        if type(is_encrypted) is not None and type(is_encrypted) is not bool:
            raise TypeError("is_encrypted is a boolean")
        self.__is_encrypted = is_encrypted

    @property
    def is_versioned(self) -> Optional[bool]:
        """Returns the is versioned flag for bucket"""
        return self.__is_versioned

    @is_versioned.setter
    def is_versioned(self, is_versioned: Optional[bool]) -> None:
        """Sets the is versioned flag for bucket"""
        if type(is_versioned) is not None and type(is_versioned) is not bool:
            raise TypeError("is_version is a boolean")
        self.__is_versioned = is_versioned

    @property
    def region(self) -> Optional[str]:
        """Returns the bucket region"""
        return self.__region

    @region.setter
    def region(self, region: Optional[str]) -> None:
        """Sets the bucket region"""
        self.__region = str(region) if region is not None else None

    @property
    def size(self) -> Optional[float]:
        """Returns the bucket size"""
        return self.__size

    @size.setter
    def size(self, size: float) -> None:
        """Sets the bucket size"""
        self.__size = float(size) if size is not None else None

    @property
    def object_count(self) -> Optional[int]:
        """Returns the number of objects in the bucket"""
        return self.__object_count

    @object_count.setter
    def object_count(self, object_count: int) -> None:
        """Sets the number of objects in the bucket"""
        self.__object_count = int(object_count) if object_count is not None else None

    @property
    def tags(self) -> Optional[List[Dict]]:
        """Returns the bucket tags"""
        return self.__tags

    @tags.setter
    def tags(self, tag_set: Union[Dict[str, List], List[Dict[str, str]] ]) -> None:
        """Sets the bucket tags"""
        if type(tag_set) is list:
            tags = tag_set
        elif tag_set is not None and type(tag_set["TagSet"]) is list:
            tags = tag_set["TagSet"]
        elif tag_set is not None:
            raise Exception("This format is not correct for tags")
        self.__tags = tags if tags is not None else []

    @property
    def permission_policy(self) -> typing.Dict:
        """Returns the permission policy as dict representation of json"""
        return self.__permission_policy

    @permission_policy.setter
    def permission_policy(self, permission_policy: Dict) -> None:
        """Sets the permission policy as dict representation of json"""
        if type(permission_policy) is dict and "Policy" in permission_policy:
            perm_pol = permission_policy["Policy"]
        else:
            perm_pol = permission_policy if type(permission_policy) is dict else permission_policy
        if perm_pol is not None and type(perm_pol) is not dict:
            """testing if valid json"""
            raise ValueError("not valid permission policy json")

        self.__permission_policy = perm_pol if perm_pol is not None else None
