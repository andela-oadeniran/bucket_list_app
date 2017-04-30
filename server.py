import os

from bucketlist_api.app import app

PORT = int(os.getenv('PORT', 5000))


app.run()
