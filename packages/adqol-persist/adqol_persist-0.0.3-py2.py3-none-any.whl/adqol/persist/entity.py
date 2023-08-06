
import boto3
import botocore
import os
import logging

from botocore.config import Config
from boto3.dynamodb.conditions import Key, Attr

import functools

from adqol.persist.decoratorutil import getFieldInfos, getEntityInfos
from adqol.persist.fielduse import FieldUse

class Entity():
    config_dydb = Config(connect_timeout=1,
                        read_timeout=1,
                        retries={'max_attempts': 1})

    dynamodb = boto3.resource('dynamodb',
                            region_name='us-east-1',
                            endpoint_url=os.environ.get('DYNAMODB_URL'),
                            config=config_dydb)

    def __init__(self, table=None, obj=None, keys=None, uses=None):
        self.table=self.dynamodb.Table( table )
        self.obj=obj.from_dict( {} )
        self.fields = getFieldInfos(obj, 'field')
        logging.info(self.fields)
#        logging.info(self.uses)

    def create(self, nobj):
        newObj={}
        for f in list( self.obj.from_dict( {} ).attribute_map.keys() ):
            v=getattr(nobj, f)
            nf=self.obj.from_dict( {} ).attribute_map[f]

            newObj[nf] = getattr(nobj, f)
        logging.debug(newObj)

        self.table.put_item(
            Item=newObj
        )

    def scan(self, filters=None, fields=None):
        keys = self.fields['keys']
        filterExpression = Entity.createFilterExpression(filters)

        fields = Entity.normalizeFields(self.obj, fields, keys)

        projectionExpression=Entity.createProjectionExpression(self.obj, fields, keys)
        expressionAttributeNames=Entity.createExpressionAttributeNames(self.obj, fields, keys)

        if filterExpression == None:
            item = self.table.scan(
                ProjectionExpression=projectionExpression,
                ExpressionAttributeNames=expressionAttributeNames
            )
        else:     
            item = self.table.scan(
                FilterExpression=filterExpression, 
                ProjectionExpression=projectionExpression,
                ExpressionAttributeNames=expressionAttributeNames
            )
        return item

    def get(self, key):        
        uobj=self.obj.from_dict({ self.fields['keys'][0]: key} )
        keys=Entity.createKeys(uobj, self.fields['keys'])
        return self.table.get_item(
            Key=keys
        )

    def delete(self, key):
        uobj=self.obj.from_dict({ self.fields['keys'][0]: key} )
        keys=Entity.createKeys(uobj, self.fields['keys'])
        return self.table.delete_item(
            Key=keys
        )

    def update(self, uobj, fields=None, keys=None):
        if keys == None:
            keys = self.fields['keys']

        fields = Entity.normalizeFields(uobj, fields, keys)
        keys=Entity.createKeys(uobj, keys)

        updateExpression=Entity.createUpdateExpression(uobj, fields, keys)
        expressionAttributeNames=Entity.createExpressionAttributeNames(uobj, fields, keys)
        expressionAttributeValues=Entity.createExpressionAttributeValues(uobj, fields, keys)

        self.table.update_item(
            Key=keys,
            UpdateExpression=updateExpression,
            ExpressionAttributeValues=expressionAttributeValues,
            ExpressionAttributeNames=expressionAttributeNames,
            ReturnValues="NONE"
        )

    @staticmethod
    def createKeys(obj, keyNames=None):
        keys={}
        for f in keyNames:
            keys[f] = getattr(obj, f)
        return keys

    @staticmethod
    def createFilterExpression(filters={}):
        filterExpression=None

        for f in filters.keys():
            v = filters[f]
            if v != None:
                if isinstance(v, list):
                    for lv in v:
                        filterExpression=Entity.appendFilterExpressionItem(filterExpression, f, lv)    
                else:
                    filterExpression=Entity.appendFilterExpressionItem(filterExpression, f, v)    

        return filterExpression

    @staticmethod
    def appendFilterExpressionItem(filterExpression=None, name=None, value=None):
        if filterExpression == None:
            filterExpression = Attr(name).eq(value)    
        else:
            filterExpression = filterExpression | Attr(name).eq(value)
        return filterExpression

    @staticmethod
    def createUpdateExpression(obj=None, fields=None, keys=['id']):
        updateExpression='set '
        for f in Entity.normalizeFields(obj, fields, keys):
            updateExpression = updateExpression +'#' + f + '=:' + f + ','

        return updateExpression.rstrip(',')

    @staticmethod
    def normalizeFields(obj=None, fields=None, keys=None):
        if fields == None:
            fields = list( obj.from_dict( {} ).attribute_map.values() )
            fields.remove( keys[0] )
            logging.info(fields)
        
        return fields

    @staticmethod
    def createProjectionExpression(obj=None, fields=None, keys=None):
        projectionExpression=keys[0]
        for f in Entity.normalizeFields(obj, fields, keys):
            projectionExpression = projectionExpression + ",#" +f

        return projectionExpression

    @staticmethod
    def createExpressionAttributeNames(obj=None, fields=None, keys=None):
        expressionAttributeNames={}
        for f in Entity.normalizeFields(obj, fields, keys):
            ff = '#' + f
            expressionAttributeNames[ff] = f

        return expressionAttributeNames
    
    @staticmethod
    def createExpressionAttributeValues(obj=None, fields=None, keys=None):
        expressionAttributeValues={}
        for f in Entity.normalizeFields(obj, fields, keys):
            ff = ':' + f
            expressionAttributeValues[ff] = getattr(obj, f)

        return expressionAttributeValues

    @staticmethod
    def field(func=None, *, name=None, key=None, uses=None):
        if func is None:
            return functools.partial(field, name=name, key=key, uses=uses)

        uses = uses if uses else FieldUse.ALL

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result
            return wrapper


def field(func=None, *, name=None, key=None, uses=None):
    if func is None:
        return functools.partial(field, name=name, key=key, uses=uses)

    uses = uses if uses else FieldUse.ALL

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
        return wrapper

def entity(cls):
    def wrapper(*args, **kwargs):
        return cls(*args, **kwargs)
    return wrapper