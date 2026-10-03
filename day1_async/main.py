import asyncio
import time


async def call_expert(name: str) -> str:
    print(f"  -> Calling {name}...")
    await asyncio.sleep(1)
    print(f"  <- {name} replied")
    return f"{name} says hello"


async def sequential():
    print("\n=== SEQUENTIAL ===")
    start = time.time()

    r1 = await call_expert("GPT-4")
    r2 = await call_expert("Claude")
    r3 = await call_expert("Gemini")

    elapsed = time.time() - start
    print(f"Results: {r1}, {r2}, {r3}")
    print(f"Total time: {elapsed:.2f} seconds")


async def concurrent():
    print("\n=== CONCURRENT ===")
    start = time.time()

    results = await asyncio.gather(
        call_expert("GPT-4"),
        call_expert("Claude"),
        call_expert("Gemini"),
    )

    elapsed = time.time() - start
    print(f"Results: {results}")
    print(f"Total time: {elapsed:.2f} seconds")


async def main():
    await sequential()
    await concurrent()


if __name__ == "__main__":
    asyncio.run(main())