import boto3
import lib.constants as const

dynamodb = boto3.client(
    'dynamodb',
    region_name='us-west-2'
)

def upload_to_poke_table(p_info):
    is_variant =  p_info.variant != ''
    name = p_info.name
    if is_variant:
        name = f'{p_info.variant} {p_info.name}'

    response = dynamodb.put_item(
        TableName = const.DYNAMO_POKE_HASH_TABLE_NAME,
        Item = {
            const.DYNAMO_IMG_HASH_KEY: { 
                'S': p_info.img_hash
            },
            const.DYNAMO_DEX_NUM_KEY: { 
                'N': str(p_info.dex_num)
            },
            const.DYNAMO_NAME_KEY: { 
                'S': name
            },
            const.DYNAMO_URL_KEY: { 
                'S': p_info.url 
            },
            const.DYNAMO_SHINY_KEY: { 
                'BOOL': p_info.is_shiny
            },
            const.DYNAMO_VARIANT_KEY: { 
                'BOOL': is_variant
            }
        }
    )
    print(response)
    if response[const.DYNAMO_METADATA_KEY][const.DYNAMO_STATUS_KEY] == 200:
        return True
    else:
        return False

def try_retrieve_pokemon(img_hash):
    response = dynamodb.get_item(
        TableName = const.DYNAMO_POKE_HASH_TABLE_NAME,
        Key = {
            const.DYNAMO_IMG_HASH_KEY: { 
                'S': img_hash
            }
        }
    )
    print(response)
    if const.DYNAMO_ITEM_KEY in response.keys():
        return True, response[const.DYNAMO_ITEM_KEY][const.DYNAMO_NAME_KEY]['S']
    else:
        return False, None