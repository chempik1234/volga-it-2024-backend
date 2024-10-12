from django.urls import path
from .views import (VisitsByAccountView,   # /api/History/Account/{id}
                    GetPutVisitByIdView,    # /api/History/{id}
                    VisitCreateView)       # /api/History/

app_name = "api"

urlpatterns = [
    path("History/Account/<int:id>", VisitsByAccountView.as_view(), name="visits_by_account"),
    path("History/<int:id>", GetPutVisitByIdView.as_view(), name="get_update_visit_by_id"),
    path("History", VisitCreateView.as_view(), name="post_visit"),
]
