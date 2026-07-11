from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def func1():
    return {"message" : "Hello world"}

@app.get("/health")
def func2():
    return {"Status" : "Healthy"}