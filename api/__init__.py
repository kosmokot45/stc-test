from fastapi import APIRouter

from .tasks.views import router as task_router
from .workers.views import router as worker_router


router = APIRouter()
router.include_router(router=task_router, prefix="/tasks")
router.include_router(router=worker_router, prefix="/workers")
