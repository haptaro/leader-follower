import random

REPLICAS = ["replica1", "replica2", "replica3"]

class LeaderFollowerRouter:
    def db_for_read(self, model, **hints):
        return random.choice(REPLICAS)

    def db_for_write(self, model, **hints):
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == "default"
