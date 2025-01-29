#!/bin/bash
curl -L -o ./sephora-products-and-skincare-reviews.zip\
  https://www.kaggle.com/api/v1/datasets/download/nadyinky/sephora-products-and-skincare-reviews

unzip sephora-products-and-skincare-reviews.zip -d raw 
rm sephora-products-and-skincare-reviews.zip
echo "Data fetched and unzipped"