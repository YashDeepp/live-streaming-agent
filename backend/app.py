import redis
import json
from fastapi import FastAPI, Query

app = FastAPI()
r = redis.Redis(host="redis", port=6381)

@app.get("/search")
def search(objects: str = Query(...)):
    query_objects = [obj.strip() for obj in objects.split(",")]
    entries = r.lrange("detections", 0, -1)
    results = []
    for e in entries:
        data = json.loads(e)
        if all(obj in data["objects"] for obj in query_objects):
            results.append(data)
    return {"results": results}
