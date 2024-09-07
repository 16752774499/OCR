import os
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()
import ddddocr

ocr = ddddocr.DdddOcr(beta=True)  # 切换为第二套ocr模型
# 确保PIC目录存在
os.makedirs("pic", exist_ok=True)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # 判断文件后缀是否为图片
    if not file.filename.endswith(
            ("png", "jpg")):
        return JSONResponse(status_code=200, content={"message": "图片格式错误"})
    else:
        # 生成唯一的文件名
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        # 定义文件的保存路径
        file_location = f"./pic/{unique_filename}"

        # 异步写入文件
        with open(file_location, "wb+") as file_object:
            while content := await file.read(1024):  # 使用异步读取
                file_object.write(content)
        # 返回响应
        return JSONResponse(status_code=200, content={"message": "识别结果为：{0}".format(picORC(file_location))})


@app.get("/")
async def main():
    return FileResponse("index.html")


def picORC(file_path: str) -> str:
    print(file_path)
    image = open(file_path, "rb").read()
    result = ocr.classification(image)
    print(result)
    # 删除文件
    os.remove(file_path)
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
