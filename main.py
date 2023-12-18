from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from connenct_db import engine
from schema import BaseAPIResponse, ClockInSchema, CardRegisterSchema, CardRemoveSchema

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 打卡
@app.post("/clock_in", description="打卡", response_model=BaseAPIResponse)
def clock_in(
    params: ClockInSchema
):
    try:
        with engine.connect() as connection:
            #檢查卡號是否為空
            if(params.CardNo == "" or params.CardNo == None):
                raise Exception("卡號不可為空！")
            
            # 檢查卡號是否已註冊
            checked_card_no_sql = """
            SELECT * FROM tb_card_list WHERE CardNo = %s
            """
            result = connection.execute(checked_card_no_sql, (params.CardNo,))
            rows = result.fetchall()
            
            print(rows)

            if len(rows) > 0:
                # 卡號已註冊，進行打卡
                clock_in_sql = """
                INSERT INTO tb_clock_in_record (CardNo, UserName) VALUES (%s, %s)
                """
                connection.execute(clock_in_sql, (rows[0][0], rows[0][2]))

                return BaseAPIResponse(success=True, message="打卡成功")
            else:
                # 卡號未註冊，資料寫進打卡失敗Table
                clock_in_error_sql = """
                INSERT INTO tb_clock_in_error_record (CardNo) VALUES (%s)
                """
                connection.execute(clock_in_error_sql, (params.CardNo,))

                raise Exception("該卡號未註冊")
    except Exception as ex:
        return BaseAPIResponse.parse_obj({"success": False, "message": str(ex)})

# 註冊卡號
@app.post("/card_register", description="註冊卡號", response_model=BaseAPIResponse)
def card_register(
    params: CardRegisterSchema
):
    try:
        with engine.connect() as connection:
            #檢查卡號是否為空
            if(params.CardNo == "" or params.CardNo == None):
                raise Exception("卡號不可為空！")
            
            #檢查使用者名稱是否為空
            if(params.UserName == "" or params.UserName == None):
                raise Exception("使用者名稱不可為空！")

            # 檢查卡號是否已註冊
            checked_card_no_sql = """
            SELECT * FROM tb_card_list WHERE CardNo = %s
            """
            result = connection.execute(checked_card_no_sql, (params.CardNo,))
            rows = result.fetchall()

            if len(rows) > 0:
                # 卡號已註冊，回傳錯誤訊息
                raise Exception("該卡號已被使用")
            else:
                # 註冊卡號
                card_register_sql = """
                INSERT INTO tb_card_list (CardNo, UserName) VALUES (%s, %s)
                """
                connection.execute(card_register_sql, (params.CardNo, params.UserName))

                return BaseAPIResponse(success=True, message="卡號註冊成功")
    except Exception as ex:
        return BaseAPIResponse.parse_obj({"success": False, "message": str(ex)})
    
# 移除卡號
@app.post("/card_remove", description="移除卡號", response_model=BaseAPIResponse)
def card_remove(
    params: CardRemoveSchema
):
    try:
        with engine.connect() as connection:
            # 檢查卡號是否存在
            checked_card_no_sql = """
            SELECT * FROM tb_card_list WHERE CardNo = %s
            """
            result = connection.execute(checked_card_no_sql, (params.CardNo,))
            rows = result.fetchall()

            if len(rows) == 0:
                # 卡號不存在，回傳錯誤訊息
                raise Exception("該卡號不存在")
            else:
                # 移除卡號
                card_remove_sql = """
                DELETE FROM tb_card_list WHERE CardNo = %s
                """
                connection.execute(card_remove_sql, (params.CardNo,))

                return BaseAPIResponse(success=True, message="卡號移除成功")
    except Exception as ex:
        return BaseAPIResponse.parse_obj({"success": False, "message": str(ex)})


# 取得打卡紀錄
@app.get("/get_clock_in_list", description="取得打卡紀錄", response_model=BaseAPIResponse)
def get_card_list():
    try:
        with engine.connect() as connection:
            sql="""
            select Seqno, ClockInTime, UserName from tb_clock_in_record 
            """
            result = connection.execute(sql).fetchall()
            return BaseAPIResponse(success=True, data=result, total=len(result))
    except Exception as ex:
        return BaseAPIResponse.parse_obj({"success": False, "message": str(ex)})
    
# 取得打卡失敗紀錄
@app.get("/get_clock_in_error_list", description="取得打卡失敗紀錄", response_model=BaseAPIResponse)
def get_clock_in_error_list():
    try:
        with engine.connect() as connection:
            sql="""
            select * from tb_clock_in_error_record 
            """
            result = connection.execute(sql).fetchall()
            return BaseAPIResponse(success=True, data=result, total=len(result))
    except Exception as ex:
        return BaseAPIResponse.parse_obj({"success": False, "message": str(ex)})

