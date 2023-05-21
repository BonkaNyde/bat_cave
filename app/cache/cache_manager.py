# from..config import Config
# from app.cache.redis_cache import Redis



# static_file_cache
# db_cache

class ModelCache:
    """
    """

    def __init__(self, model:object, cache_schema:object):
        """
        """
        model_name =  model.__name__
        model_data = {}
        for model_row in model.query.all():
            model_data.update({
                str(model_row.id): model_row.to_json()
            })
        self.model = {
            model_name: model_data
        }
        print(self.model)
