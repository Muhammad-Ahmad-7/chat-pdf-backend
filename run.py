import uvicorn

if __name__ == "__main__":
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) DEV 
    uvicorn.run("main:app", host="0.0.0.0", port=10000)  # PRODUCTION

# --- DEV COMMAND ---
# uvicorn index:app --reload 
