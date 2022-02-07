import pandas as pd


# rinomina una colonna specificata come itemId per renderla più generale
def itemIdAdapter(items, nameLabel):
    return items.rename(columns={nameLabel: 'itemId'}, inplace=True)
