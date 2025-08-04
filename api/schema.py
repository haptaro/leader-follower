import strawberry
from api.queries import Query
from api.mutations import Mutation
from api.subscriptions import Subscription

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)
