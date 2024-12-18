class CinemaDatabaseRouter:
    """
    Маршрутизатор для визначення бази даних для кожної моделі.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'mongoapp':  
            return 'mongo'
        return 'default'  # PostgreSQL 

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'mongoapp':  
            return 'mongo'
        return 'default'  

    def allow_relation(self, obj1, obj2, **hints):
        # Дозволити зв’язки між об'єктами, якщо вони з однієї бази даних
        db_set = {'default', 'mongo'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'mongoapp':  
            return db == 'mongo'
        return db == 'default'  