from fastapi import APIRouter, status

from src.speechassistant.api.logic.moduleLogic import ModuleLogic
from src.speechassistant.models.module import Module

router: APIRouter = APIRouter()


@router.post("/", response_model=Module, status_code=status.HTTP_201_CREATED)
async def create_module(response: dict):
    return None


@router.get("/", response_model=list[Module], status_code=status.HTTP_200_OK)
async def read_all_modules():
    return ModuleLogic.read_all_modules()


@router.get("/{module_name", response_model=Module, status_code=status.HTTP_200_OK)
async def read_module_by_name(module_name: str):
    return ModuleLogic.read_module_by_name(module_name)


@router.get("/names", response_model=list[str], status_code=status.HTTP_200_OK)
async def read_all_module_names():
    return ModuleLogic.read_all_module_names()


@router.put("/{module_name}", response_model=Module, status_code=status.HTTP_200_OK)
async def update_module(module_name: str, module: Module):
    return ModuleLogic.update_module(module_name, module)


@router.delete(
    "/{module_name}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_module(module_name: str):
    return ModuleLogic.delete_module(module_name)
