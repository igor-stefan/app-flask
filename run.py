import os
from app import app, socketio

        
if __name__=="__main__":
    port = int(os.environ.get("PORT", 8080))
    socketio.run(app,port=port)