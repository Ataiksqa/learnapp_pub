from starlette.middleware.cors import CORSMiddleware
from main import app

origins = [
    "http://localhost"
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["GET","POST","PUT"],#,"DELETE"],
                   allow_headers =["*"])