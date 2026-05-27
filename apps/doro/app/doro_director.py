from fastapi import FastAPI


app = FastAPI(title="Doro Data")


class DoroDirector:
    def __init__(self):
        pass

    def get_data(self):
        raise RuntimeError("Doro internal file data source has been removed.")