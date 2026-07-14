# Parallele Evaluation mit asyncio
# Quelle: chapters/10_evaluation.tex (Zeile 585)
import asyncio
import aiohttp

async def evaluate_single(session, example, prompt_fn):
    """Einzelnen Testfall evaluieren (parallelisierbar)."""
    try:
        output = await prompt_fn(example["input"])
        return evaluate_output(example, output)
    except Exception as e:
        return {"input": example["input"], "error": str(e)}

async def evaluate_parallel(dataset, prompt_fn, max_concurrent=20):
    """Evaluierung parallelisiert mit Semaphore."""
    sem = asyncio.Semaphore(max_concurrent)
    async with aiohttp.ClientSession() as session:

        async def bounded_eval(example):
            async with sem:
                return await evaluate_single(session, example, prompt_fn)

        tasks = [bounded_eval(ex) for ex in dataset]
        return await asyncio.gather(*tasks)

# Nutzung
results = asyncio.run(evaluate_parallel(GOLDEN_DATASET, my_prompt_fn))
pass_rate = sum(1 for r in results if r.get("passed")) / len(results) * 100
print(f"Pass Rate: {pass_rate:.1f}% ({len(results)} Tests)")

