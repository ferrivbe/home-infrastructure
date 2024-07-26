import pytest
from src.middleware.request_logger import AsyncIteratorWrapper


@pytest.mark.asyncio
async def test_async_iterator_wrapper_iterates_correctly():
    items = [1, 2, 3]
    async_wrapper = AsyncIteratorWrapper(items)
    collected = [item async for item in async_wrapper]
    assert collected == items, "AsyncIteratorWrapper did not iterate correctly"


@pytest.mark.asyncio
async def test_async_iterator_wrapper_stops_iteration():
    async_wrapper = AsyncIteratorWrapper([])
    with pytest.raises(StopAsyncIteration):
        await async_wrapper.__anext__()
