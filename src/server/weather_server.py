from fastapi import FastAPI, Request
import json
import argparse
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
import uvicorn
import re
import requests
import pandas as pd

paraser_arg = argparse.ArgumentParser()
paraser_arg.add_argument("--port", type = int, default=5000)
paraser_arg.add_argument("--listen_IP", type = str, default="0.0.0.0")

args = paraser_arg.parse_args()


TIMEOUT_KEEP_ALIVE = 50  # seconds.
TIMEOUT_TO_PREVENT_DEADLOCK = 1  # seconds.
app = FastAPI()

key = "557c4c84c1275af20f12515f3165cdc7"
remote_url = "https://restapi.amap.com/v3/weather/weatherInfo?city={citycode}&key={key}"

def get_city_code(city: str):
    city_df = pd.read_excel(
            'https://modelscope.oss-cn-beijing.aliyuncs.com/resource/agent/AMap_adcode_citycode.xlsx'
        ) 
    search_pattern = re.compile(city)
    table = city_df['中文名']
    search_result = []
    for i in range(len(table)):
        if re.search(search_pattern, table[i]):
            search_result.append([i, table[i]])
    ## find same length
    diff_min = 100
    diff_min_index = 0
    if len(search_result) == 1:
        return city_df['adcode'][search_result[0][0]]
    else:
        for i in range(len(search_result)):
            diff = abs(len(search_result[i][1]) - len(city))
            if diff < diff_min:
                diff_min = diff
                diff_min_index = i
        return city_df['adcode'][search_result[diff_min_index][0]]


@app.get("/health")
async def health() -> Response:
    """Health check."""
    return Response(status_code=200)


@app.post("/weather")
async def generate(request: Request) -> Response:

    request_dict = await request.json()
    city = request_dict["city"]
    citycode = get_city_code(city)
    res = requests.get(remote_url.format(citycode=citycode, key=key))
    print(json.loads(res.text))

    return JSONResponse(json.loads(res.text))


if __name__ == "__main__":
    # print(get_city_code("北京"))
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default=None)
    parser.add_argument("--port", type=int, default=5004)
    args = parser.parse_args()

    uvicorn.run(app,
                host=args.host,
                port=args.port,
                log_level="debug",
                timeout_keep_alive=TIMEOUT_KEEP_ALIVE)

