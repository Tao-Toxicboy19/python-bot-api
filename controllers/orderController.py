from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

@app.post("/createPosition")
async def createPosition(request: Request):
    try:
        # Access the request body
        request_body = await request.json()
        
        # Your logic to process the request body goes here
        # For example, you can access data using request_body["key"]

        return {"message": request_body}

    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
