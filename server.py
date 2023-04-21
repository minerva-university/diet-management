from web import app
from logger import info_logger, error_logger


if __name__ == '__main__':
    app.run(debug=True)
    info_logger.info("Server Running") 


    