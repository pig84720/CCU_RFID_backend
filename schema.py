from pydantic import BaseModel, Field
from typing import Optional, Union, Any

class BaseAPIResponse(BaseModel):
    """
    回傳資料結構(固定以此資料結構作為回傳, 接收端可以很明顯知道每次所回傳的資料結構)
    """

    success: bool = False  # 成功 or 失敗
    message: str = ""  # 回傳訊息
    data: Optional[
        Union[list[tuple[Any]], list[Any], Any, None]
    ] = None  # 回傳的結構, 可能為單筆資料, 多筆資料, 甚至是不需回傳資料
    total: int = 0

    class Config:
        orm_mode = True

class ClockInSchema(BaseModel):
    """ClockInSchema

    Args:
        BaseModel (_type_): _description_
    """

    CardNo: str = Field(..., example="777777777777", description="NFC Tag的序列號")

class CardRegisterSchema(BaseModel):
    """CardRegisterSchema

    Args:
        BaseModel (_type_): _description_ 
    """

    CardNo: str = Field(..., example="777777777777", description="NFC Tag的序列號")
    UserName: str = Field(..., example="蟹老闆", description="持卡人姓名")

class CardRemoveSchema(BaseModel):
    """CardRemoveSchema

    Args:
        BaseModel (_type_): _description_ 
    """

    CardNo: str = Field(..., example="777777777777", description="NFC Tag的序列號")