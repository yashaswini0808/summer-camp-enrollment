import uvicorn

if __name__ == "__main__":
    print("==================================================")
    print("SUMMER CAMP SPORTS ENROLLMENT SYSTEM")
    print("==================================================")
    print("Local Computer UI:  http://127.0.0.1:8000")
    print("Mobile Phone UI:    http://192.168.29.165:8000")
    print("API Documentation:  http://127.0.0.1:8000/docs")
    print("==================================================")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
