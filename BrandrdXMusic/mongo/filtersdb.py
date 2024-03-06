from BrandrdXMusic.utils.mongo import db

filters = db.filters["filters"] 

async def add_filter_db(chat_id: int, filter_name: str, content: str, text: str, data_type: int):
   filter_data = await filters.find_one(
      {
         'chat_id': chat_id
      }
   )

   if filter_data is None:
      _id = await filters.count_documents({}) + 1
      await filters.insert_one(
         {
            '_id': _id,
            'chat_id': chat_id,
            'filters': [
               {
                  'filter_name': filter_name,
                  'content': content,
                  'text': text,
                  'data_type': data_type
               }
            ]
         }
      )
   
   else:
         FILTERS_NAME = await get_filters_list(chat_id)
         if filter_name not in FILTERS_NAME:
            await filters.update_one(
               {
                  'chat_id': chat_id
               },
               {
                  '$addToSet': {
                     'filters': {
                        'filter_name': filter_name,
                        'content': content,
                        'text': text,
                        'data_type': data_type
                     }
                  }
               },
               upsert=True
            )
         else:
            await filters.update_one(
               {
                  'chat_id': chat_id,
                  'filters.filter_name': filter_name
               },
               {
                  '$set': {
                     'filters.$.filter_name': filter_name,
                     'filters.$.content': content,
                     'filters.$.text': text,
                     'filters.$.data_type': data_type
                  }
               }
            )

async def stop_db(chat_id: int, filter_name:str):
   await filters.update_one(
      {
         'chat_id': chat_id
      },
      {
         '$pull': {
            'filters': {
               'filter_name': filter_name
            }
         }
      }
   )

async def stop_all_db(chat_id: id):
   await filters.update_one(
      {
         'chat_id': chat_id
      },
      {
         '$set': {
            'filters': []
         }
      },
      upsert=True
   )
   
async def get_filter(chat_id: int, filter_name: str):
   filter_data = await filters.find_one(
      {
         'chat_id': chat_id
      }
   )
   if filter_data is not None:
      filters_ = filter_data['filters']
      for filter_ in filters_:
         if filter_['filter_name'] == filter_name:
            content = filter_['content']
            text = filter_['text']
            data_type = filter_['data_type']
            return (
               filter_name,
               content,
               text,
               data_type
            )

async def get_filters_list(chat_id: int):
   filter_data = await filters.find_one(
      {
         'chat_id': chat_id
      }
   )
   if filter_data is not None:
      FILTERS_NAME = list()
      for filter_name in filter_data['filters']:
         FILTERS_NAME.append(filter_name['filter_name'])
      return FILTERS_NAME
   else:
      return []
