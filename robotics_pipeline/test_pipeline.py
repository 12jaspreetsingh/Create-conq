import asyncio
import json
from httpx import AsyncClient, ASGITransport
from main import app

async def run_tests():
    # 1. Clear memory file for a clean test
    with open("data/memory.json", "w") as f:
        json.dump([], f)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        print("=== Test 1: First Video Processing (No Memory Yet) ===")
        # Sending dummy request to process-video
        response = await ac.post("/process-video/")
        data1 = response.json()
        print(json.dumps(data1, indent=2))
        print(f"\nTask 1 ID: {data1['task_id']}")
        print(f"Similar Past Tasks Found: {len(data1['similar_past_tasks'])}")
        assert len(data1['similar_past_tasks']) == 0, "Should be no past tasks initially."

        print("\n\n=== Test 2: Second Video Processing (Continuous Learning) ===")
        # Another request, the system should learn from the first
        response = await ac.post("/process-video/")
        data2 = response.json()
        print(json.dumps(data2, indent=2))
        print(f"\nTask 2 ID: {data2['task_id']}")
        print(f"Similar Past Tasks Found: {len(data2['similar_past_tasks'])}")
        
        # It's highly probable it will find a similarity since actions are randomly chosen from a small set
        
        print("\n\n=== Test 3: Querying the Memory System ===")
        actions_to_query = [data1['actions'][0]['action_name']]
        query_payload = {"actions": actions_to_query}
        response = await ac.post("/memory/query", json=query_payload)
        query_data = response.json()
        
        print(f"Querying for action: {actions_to_query}")
        print(f"Tasks retrieved from memory: {len(query_data['similar_tasks'])}")
        print(json.dumps(query_data, indent=2))

        print("\n\n=== Test 4: Verify Full Memory Storage ===")
        response = await ac.get("/memory/")
        memory_data = response.json()
        print(f"Total tasks stored in memory: {len(memory_data)}")
        assert len(memory_data) == 2, "Should have 2 tasks in memory."

if __name__ == "__main__":
    asyncio.run(run_tests())
