from django.urls import path
from .views import (VisitsByAccountView,   # /api/History/Account/{id}
                    VisitByIdView,         # /api/Hostory/{id}
                    VisitPostPutView)      # /api/History/{id} /api/History

app_name = "api"

urlpatterns = [
    path("History/Account/<int:id>", VisitsByAccountView.as_view(), name="visits_by_account"),
    path("History/<int:id>", VisitByIdView.as_view(), name="visit_by_id"),
    path("History", VisitPostPutView.as_view(), name="post_visit"),
    path("History/<int:id>", VisitPostPutView.as_view(), name="put_visit")
]
