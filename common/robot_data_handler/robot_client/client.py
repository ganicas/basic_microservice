import csv
from common.logging.setup import logger


def get_data_from_robot():
    """This is basic robot data simulator"""
    file = ''
    if file:
        reader = csv.DictReader(open(file))
        data = []
        for row in reader:
            data.append([row])
        return data
