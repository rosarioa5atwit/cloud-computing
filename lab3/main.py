
import subprocess
import sys
import time
import threading

def start_fastapi():
    try:
        process = subprocess.Popen([
            sys.executable,"-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000",]
        
        )
        return process
    except Exception as e:
        print(f"Failed to start FastAPI: {e}")
        return None
    
def stop_fastapi(process):
    if process:
        process.terminate()
        process.wait()
        print("FastAPI server stopped.")


def maindriver():

    continueLoop = True
    while continueLoop:
        print("Main Menu")
        print("1. Execute FastAPI Routes")
        print("2. Execute Express Routes")
        print("3. Exit")

        choice = input("Enter your choice (1, 2 or 3): ")
        if choice == '1':
            print("Executing FastAPI Routes...")

        elif choice == '2':
            print("Executing Express Routes...")
            fastapi_process = start_fastapi()
            if fastapi_process:
                print("FastAPI server started. You can now access routes from app.py at http://localhost:8000")
                input("Press Enter to stop the FastAPI server and return to the menu...")
                stop_fastapi(fastapi_process)
            else:
                print("Could not start FastAPI server.") 
        elif choice == '3':
            print("Exiting the program.")
            continueLoop = False
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    maindriver()
