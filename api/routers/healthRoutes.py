from fastapi import APIRouter, status, Body, HTTPException, Depends

router = APIRouter(
    tags=['health']
)

@router.get(
    '/health',
    summary='Health check for the API.',
    description='Returns a list of users in JSON format.',
    )
async def get_health_check():
    return { 'message': 'ok' }