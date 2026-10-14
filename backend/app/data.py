from __future__ import annotations

import random
from typing import List, Tuple


def generate_training_examples(count: int = 200) -> List[Tuple[List[float], List[float]]]:
    samples = []
    for _ in range(count):
        # Simulated user preference profile
        tone = random.uniform(0, 1)
        length = random.uniform(0, 1)
        technicality = random.uniform(0, 1)
        urgency = random.uniform(0, 1)
        clarity = random.uniform(0, 1)

        target = [
            tone,
            length,
            technicality,
            urgency,
            clarity,
        ]
        samples.append((target, target))
    return samples
