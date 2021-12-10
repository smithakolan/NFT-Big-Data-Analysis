#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: swaathi
"""
import getDataFromDB as getNFT
import json
import pandas as pd
from scipy.stats import pearsonr
import sys
assert sys.version_info >= (3, 5)  # make sure we have Python 3.5+


def main():
    # get data from DB
    nft_from_db = getNFT.scan_dynamodb('NFTs')

    # convert it to a pandas dataframe
    nft_df = pd.DataFrame(nft_from_db)

    # selecting required json fields for use case
    nft_selected = nft_df[['id', 'slug', 'num_sales', 'last_sale_total_price']]

    # group by slug and calculate correlation between price and number of sales
    nft_slugs = nft_selected['slug'].unique()
    corr_list = []
    for slug in nft_slugs:
        nft_of_slug = nft_selected[nft_selected['slug'] == slug]
        corr, _ = pearsonr(
            nft_of_slug['num_sales'], nft_of_slug['last_sale_total_price'])
        corr_list.append(corr)

    nft_corr = pd.DataFrame({
        'Collections': nft_slugs,
        'Correlation factor between price and number of sales': corr_list
    })
    nft_corr.to_csv('nft_corr.csv')


if __name__ == '__main__':
    main()
