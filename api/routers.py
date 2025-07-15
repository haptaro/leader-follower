import random, logging

log = logging.getLogger("db.router")

REPLICAS = ["replica1", "replica2", "replica3"]

class LeaderFollowerRouter:
    def db_for_read(self, model, **hints):
        alias = random.choice(REPLICAS)
        log.info(">>> READ  → %s", alias)
        return alias

    def db_for_write(self, model, **hints):
        log.info(">>> WRITE → default")
        return "default"

    def allow_relation(self, *args, **kwargs):
        return True

    def allow_migrate(self, db, *args, **kwargs):
        return db == "default"
