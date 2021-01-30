import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE","weeeating_project.settings")
django.setup()

from store.models import *

CSV_PATH_INFO = './weeeating_store.csv'


with open(CSV_PATH_INFO) as in_file :

    data_reader = csv.reader(in_file)

    for row in data_reader :

        #store 정보 입력

        if row[0] :
            name = row[0]
            description = row[1]
            #delivery = row[2]
            address = row[3]
            tags = row[4].split('+')
            image = row[5]

            if row[2] :
                store = Store.objects.create(
                    name = name,
                    description = description,
                    delivery = True,
                    address = address
                )

            else :
                store = Store.objects.create(
                    name = name,
                    description = description,
                    delivery = False,
                    address = address
                )

            store_id = store.id

            for tag in tags :
                StoreTag.objects.create(store_id = store_id, tag = tag)

            StoreImage.objects.create(store_id = store_id, image=image)




"""
        if row[0] :
            name = row[0]
            description = row[1]

        if row[2] :
            delivery = True

        delivery = False
        address = row[3]
        tags = row[4].split('+')
        image = row[5]

        store = Store.objects.create(
            name = name,
            description = description,
            delivery = delivery,
            address = address
        )

        store_id = store.id

        for tag in tags :
            StoreTag.objects.create(store_id = store_id, tag = tag)

        StoreImage.objects.create(store_id = store_id, image=image)

"""

"""
        for image in images :
            StoreImage.objects.create(store_id = store_id, image= image)

"""


"""
        if row[0] :
            name = row[0]

        if row[1] :
            description = row[1]

        if row[2] == "TRUE" :
            delivery = True

        if row[3] :
            address = row[3]

        if row[4] :
            tags = row[4].split(',')

        if row[5] :
            image = row[5]

        store ,created = Store.objects.get_or_create(
            name = name,
            description = description,
            delivery = True, 
            address = address
        )

        for tag in tags :
            StoreTag.objects.get_or_create(store_id = store.id, tag = tag)

        for image in images:
            StoreImage.objects.get_or_create(store_id = store.id, image = image)

"""
